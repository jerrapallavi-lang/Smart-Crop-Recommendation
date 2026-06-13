
# Smart Crop Recommendation & Yield Prediction System

A polished Flask web app that predicts the best crop and expected yield based on soil type, temperature, rainfall, and soil pH.

## Features
- Responsive Bootstrap UI with clean modern design
- Crop recommendation and yield prediction using trained machine learning models
- Personalized insights based on user input
- Prediction history tracking during each session
- Download the latest recommendation as a CSV file
- Mobile-accessible when the Flask app is served on a LAN address

## Technologies
- Python 3.12
- Flask
- scikit-learn / machine learning model serialization
- Bootstrap 5 for UI

## How to Run
1. Create and activate a virtual environment (recommended)
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Train the model once if not already available:
   ```bash
   python training/train_model.py
   ```
4. Run the application:
   ```bash
   python app.py
   ```
5. Open the app in your browser:
   - On this machine: `http://127.0.0.1:5000`
   - On another device on your local network: `http://<your-lan-ip>:5000`

## Notes for Resume or Demo
- This project demonstrates full-stack development with a Flask backend and Bootstrap frontend.
- The app now includes a one-click CSV export for the most recent crop recommendation, making it easier to share results.
- It also captures session prediction history and generates actionable insights for farmers.

## Deployment Tips
- Use a production WSGI server like `gunicorn` for deployment.
- Host on a cloud VM or container and map port `5000`.
- Ensure `FLASK_ENV` is set to `production` and session secret is secure.

