# 🌍 Urban Air Quality Forecasting  
A machine-learning based project that predicts *Air Quality Index (AQI)* using historical pollution, weather, and environmental data.  
This project includes data preprocessing, model training & evaluation, and an interactive *Streamlit dashboard* for visualizing and forecasting AQI levels.

---

## 📌 Features
- 📊 *Interactive Streamlit Dashboard*
- 🔥 *AQI Forecasting* using trained ML models
- 🌡 Real-time weather & pollution API integration
- 🎨 Heatmap visualization that changes color based on AQI level
- 🧹 Automated data preprocessing (imputation, scaling)
- 📁 Modular project structure with clean code

---

## 📂 Project Structure


Urban-Air-Quality-Forecasting/
│
├── app/
│   ├── app.py                # Main Streamlit app
│   ├── pollution_api.py      # Pollution API helper
│   ├── weather_api.py        # Weather API helper
│   └── location_utils.py     # Location utilities
│
├── data/
│   └── city_day.csv          # Dataset used for training
│
├── models/
│   ├── final_random_forest_model.pkl   # Final trained model
│   ├── scaler.pkl                       # Saved MinMax scaler
│   └── imputer.pkl                      # Saved imputer
│
├── notebooks/
│   ├── 01_preprocessing.ipynb
│   └── 02_model_comparison.ipynb
│
├── requirements.txt
└── README.md


---

## 🤖 Machine Learning Models Used

Three ML models were trained and compared:

| Model              | Description |
|--------------------|-------------|
| *Bayesian Ridge Regression* | Linear model with probabilistic approach |
| *Random Forest Regressor* | Ensemble model — performed best |
| *Linear Regression* | Simple baseline model |

### ✅ Final Selected Model  
The project automatically compares models based on *RMSE*, and the best model is selected.

✔ *Random Forest Regressor* achieved the lowest RMSE → *Best Performing Model*  
That model was retrained on the full training dataset and saved as:


models/final_random_forest_model.pkl


Scaling and imputation transformations were also saved:


models/scaler.pkl
models/imputer.pkl

## 🚀 Running the App

### *1️⃣ Install dependencies*

pip install -r requirements.txt


### *2️⃣ Run the Streamlit App*

streamlit run app/app.py


---

## 📦 Requirements
All dependencies are listed in:


requirements.txt


---

## 📈 Visualizations (Heatmap, AQI Indicators)
The dashboard includes:
- AQI heatmap with dynamic color scale  
- AQI category indicators  
- Prediction graphs  
- Parameter-wise AQI plots  

---

## 🧑‍💻 Technologies Used
- Python  
- Scikit-learn  
- Pandas  
- NumPy  
- Streamlit  
- Matplotlib / Plotly  
- REST APIs (Weather + Pollution)

---

## 📜 License
This project is open-source and free to use.

---

## ✨ Author
*Priya Shukla*  
Urban Air Quality Forecasting Project
