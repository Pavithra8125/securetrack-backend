from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import pandas as pd
from werkzeug.utils import secure_filename

# Flask app
app = Flask(__name__, static_folder='static', static_url_path='/')
CORS(app, origins=["http://localhost:3000", "https://securetrack-backend.onrender.com"], supports_credentials=True)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Serve React frontend
@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

# Catch all other routes and serve React (important for routing)
@app.errorhandler(404)
def not_found(e):
    return send_from_directory(app.static_folder, 'index.html')

# Upload CSV and process
@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded."}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file."}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file format. Only CSV allowed."}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        df = pd.read_csv(filepath)

        required_columns = ['timestamp', 'mobile_number', 'location', 'event_type', 'duration', 'latitude', 'longitude']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return jsonify({"error": f"Missing columns: {', '.join(missing_columns)}"}), 400

        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        df['duration'] = pd.to_numeric(df['duration'], errors='coerce')

        location_counts = df.groupby('mobile_number')['location'].nunique()
        frequent_events = df['mobile_number'].value_counts()
        long_calls = df[(df['event_type'] == 'call') & (df['duration'] > 5)]

        suspicious_numbers = set(location_counts[location_counts >= 2].index) | \
                             set(frequent_events[frequent_events > 3].index) | \
                             set(long_calls['mobile_number'])

        suspicious_info = []
        for num in suspicious_numbers:
            user_data = df[df['mobile_number'] == num]
            locations = user_data[['location', 'latitude', 'longitude']].drop_duplicates()

            locations_with_number = []
            for _, row in locations.iterrows():
                locations_with_number.append({
                    'location': row['location'],
                    'latitude': row['latitude'],
                    'longitude': row['longitude'],
                    'mobile_number': num
                })

            reasons = []
            if num in location_counts[location_counts >= 2]:
                reasons.append('Multiple locations')
            if num in frequent_events[frequent_events > 3]:
                reasons.append('Frequent events')
            if num in long_calls['mobile_number'].values:
                reasons.append('Long calls')

            suspicious_info.append({
                "mobile_number": num,
                "reason": ', '.join(reasons),
                "locations": locations_with_number
            })

        return jsonify({"suspicious_numbers": suspicious_info})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred processing the CSV file."}), 500

# Run app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
