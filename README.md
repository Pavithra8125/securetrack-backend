# SecureTrack Backend

Welcome to the backend of **SecureTrack**, a web-based Tower Dump Analysis Tool designed for digital forensic investigations. This backend is built using **Flask** and provides APIs to interact with the frontend, process CSV files, detect suspicious numbers, and generate reports.

The backend handles the business logic and data processing, while the frontend allows users to upload CSV files and view results in a user-friendly interface.

## 🌟 Key Features

- **CSV file upload API** to accept and process tower dump data
- **Suspicious number detection** to identify potential threats
- **Geographical data processing** for mapping call patterns
- **Report generation** in CSV and PDF formats
- Integrated with **React** frontend for seamless user experience

---

## 🔧 Installation

### 1. Clone the repository:

    git clone https://github.com/Pavithra8125/securetrack-backend.git
    cd securetrack-backend

### 2. Set up a Python virtual environment (recommended):
  
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    
### 3. Install dependencies:

    pip install -r requirements.txt

### 4. Run the server:
  
    python app.py

The backend will be running on [http://localhost:5000](http://localhost:5000)

---

## 📚 API Endpoints

-  POST /upload: Uploads a CSV file to be processed and analyzed.

-  GET /status: Checks the current status of the backend server.

-  GET /download-report: Downloads the generated report in CSV or PDF format.

---
## 🚀 Deployment

The backend is deployed on **Render** and accessible at [https://securetrack-backend.onrender.com](https://securetrack-backend.onrender.com).  
👉 **If the full interface doesn’t fit on your screen, try zooming out to 80% for better visibility.**

## 📝 Sample CSV for Testing:
Check it (File Name: Sample file.csv) in the frontend repository.

## 🔗 Frontend Repository
Access the frontend code here:[SecureTrack Frontend Repository](github.com/Pavithra8125/securetrack-frontend)

## 🤝 Contributing

Feel free to open issues or submit pull requests to improve the project.
Contributions are always welcome!

