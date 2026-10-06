
# Smart Crop Recommendation System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white" alt="Python 3.12" />
  <img src="https://img.shields.io/badge/Flask-3.0-000000?logo=flask&logoColor=white" alt="Flask" />
  <img src="https://img.shields.io/badge/ML-Scikit%20Learn-F7931E?logo=scikitlearn&logoColor=white" alt="Scikit-learn" />
</p>

A Flask-based web application that recommends the most suitable crop and estimates expected yield based on soil type, temperature, rainfall, and soil pH.

## Overview
This project helps farmers and agricultural planners decide which crop is most suitable for given field conditions. The app uses a trained machine learning model and provides user-friendly recommendations through a responsive web interface.

## How It Works
1. The user enters field parameters such as temperature, rainfall, soil type, and pH.
2. The application preprocesses the input and passes it to a trained model.
3. The model predicts the best crop and estimated yield.
4. Results are displayed with basic recommendations and downloadable history logs.

## Features
- Crop recommendation based on soil and climate parameters
- Yield prediction for the selected crop
- Clean, responsive Bootstrap-based UI
- Session-based prediction history
- CSV export for recent recommendations
- Lightweight local deployment suitable for demos and learning projects

## Tech Stack
- Python 3.12
- Flask
- scikit-learn
- Pandas and NumPy
- Bootstrap 5

## Project Structure
```text
Smart_Crop_Recommendation_System/
├── app.py
├── README.md
├── requirements.txt
├── dataset/
│   └── crop_data.csv
├── models/
├── static/
├── templates/
├── training/
│   └── train_model.py
└── latest_prediction.csv
```

## Setup
1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Train the model if needed:
   ```bash
   python training/train_model.py
   ```
4. Start the app:
   ```bash
   python app.py
   ```
5. Open in browser:
   - Local: http://127.0.0.1:5000
   - LAN: http://<your-lan-ip>:5000

## Usage
Enter values such as soil type, temperature, rainfall, and pH. The system predicts the best crop and estimated yield, then displays actionable recommendations.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Notes
- This project is designed as a practical agriculture ML demo.
- It can be extended with weather API integration, model improvements, or farmer-specific dashboards.
- The current repository includes the project documentation and source code needed to run the application locally.

