# 🛡️ Phishing Detection Web App

A Flask-based web application that detects phishing websites using a trained machine learning model and handcrafted URL-based features.

---

## 📌 Features

- 🔍 **Real-Time Prediction**: Enter a URL and detect phishing in real-time using handcrafted features.
- 📄 **CSV File Upload**: Upload a batch of URLs via a CSV file for bulk predictions.
- 🧠 **Manual Feature Input**: Manually input 30 features for fine-grained control.
- 🧾 **Prediction Results**: View results with prediction labels and confidence scores.
- 📘 **API Documentation**: Swagger-style documentation for programmatic interaction.
- 🌗 **Dark Mode**: Clean professional UI with light/dark mode support.
- 🖱️ **Custom File Upload UI**: Aesthetic and responsive "Browse" button.
- 📁 **Modular Architecture**: Designed with a scalable and maintainable code structure.

---

## 🗂️ Project Structure

```bash
├── app.py                   # Main Flask app
├── main.py                  # Entry point
├── network/                 # Core ML modules (pipeline, utils, logging, etc.)
│   ├── components/
│   ├── constants/
│   ├── entity/
│   ├── exception/
│   ├── logging/
│   ├── pipeline/
│   └── utils/
├── final_model/             # Trained model and artifacts
├── prediction_output/       # Output predictions from CSV
├── notebook/                # Jupyter notebooks for experimentation
├── static/
│   └── style.css            # Custom styles (optional)
├── templates/               # HTML templates
│   ├── index.html
│   ├── manual_form.html
│   ├── results.html
│   └── table.html
├── uploads/                 # Uploaded CSVs
├── requirements.txt         # Python dependencies
├── dockerfile               # Docker container setup
└── README.md                # Project overview

```

## Getting Started
1️⃣ Clone the Repository

git clone https://github.com/your-username/phishing-detection-app.git
cd phishing-detection-app

2️⃣ Create Virtual Environment

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3️⃣ Install Dependencies

pip install -r requirements.txt

4️⃣ Run the App

python app.py

Open your browser and go to: http://127.0.0.1:5000/
## How to Use
📤 CSV Upload

    Go to the home page.

    Upload a .csv file containing URLs or feature values.

    Click Predict to view results.

🧠 Manual Feature Input

    Navigate to Manual Input.

    Input values for 30 features (e.g., IP presence, URL length).

    Submit to get predictions and confidence scores(in future update)

📘 API Documentation

    Go to /docs for Swagger/OpenAPI documentation.

📦 Docker Support

To build and run using Docker:

docker build -t phishing-detector .
docker run -p -d 5000:5000 phishing-detector

## Technologies Used

    Python

    Flask

    Scikit-learn / XGBoost (or your ML library)

    HTML/CSS

    TailwindCSS (via CDN)

    Docker (optional)

🤖 Machine Learning Info

This app uses a trained model built on handcrafted URL-based features such as:

    Presence of IP address

    Length of URL

    Use of shortening services

    Suspicious symbols or patterns

Model training code is located in the network/pipeline/ directory.
✨ Future Improvements

    Add OAuth login

    Log user prediction history

    Deploy to cloud (Render/Heroku/AWS)

    Add interactive feature explanation

📜 License

MIT License © 2025 Phishing Detection Web App Team