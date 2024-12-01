import pandas as pd
import streamlit as st
import joblib

class EnergyConsumptionApp:
    def __init__(self):
        st.set_page_config(
            page_title="Energy Consumption Prediction App",
            page_icon="⚡",
            layout="wide"
        )
        self.setup_page()
        self.load_resources()

    def setup_page(self):
        st.markdown("""
        <style>
        .stApp {
            background-color: #F7F9FC;
        }
        .main-header {
            background: linear-gradient(135deg, #2196F3 0%, #64B5F6 100%);
            color: white;
            padding: 15px;
            text-align: center;
            border-radius: 10px;
        }
        .input-card, .prediction-card {
            background: #FFFFFF;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        </style>
        """, unsafe_allow_html=True)

    def load_resources(self):
        try:
            # Load models and feature names
            self.linear_model = joblib.load("linear_model.pkl")
            self.feature_names = joblib.load("feature_names.pkl")
            st.success("Resources loaded successfully!")
        except Exception as e:
            st.error(f"Error loading resources: {e}")

    def run(self):
        st.markdown("<div class='main-header'><h1>⚡ Energy Consumption Prediction</h1></div>", unsafe_allow_html=True)

        # Input section
        st.markdown('<div class="input-card">', unsafe_allow_html=True)
        st.subheader("🔧 Enter Input Values")

        # Input fields
        col1, col2, col3 = st.columns(3)

        with col1:
            voltage = st.number_input("Voltage (V)", min_value=220.0, max_value=255.0, value=240.0, step=0.1)
            sub_metering_1 = st.number_input("Sub Metering 1 (Wh)", min_value=0.0, max_value=50.0, value=1.12, step=0.1)
            date = st.date_input("Select Date", value=pd.Timestamp("2024-11-28"))

        with col2:
            global_intensity = st.number_input("Global Intensity (A)", min_value=0.0, max_value=20.0, value=4.63, step=0.1)
            sub_metering_2 = st.number_input("Sub Metering 2 (Wh)", min_value=0.0, max_value=50.0, value=1.30, step=0.1)
            hour = st.number_input("Hour", min_value=0, max_value=23, value=12)

        with col3:
            sub_metering_3 = st.number_input("Sub Metering 3 (Wh)", min_value=0.0, max_value=50.0, value=6.46, step=0.1)
            minute = st.number_input("Minute", min_value=0, max_value=59, value=0)
            is_holiday = st.selectbox("Is it a Holiday?", ["No", "Yes"])

        # Additional features
        light = st.selectbox("Daylight?", ["Day", "Night"])
        weekday = date.weekday()
        year = date.year
        month = date.month
        day = date.day
        is_holiday = 1 if is_holiday == "Yes" else 0
        light = 1 if light == "Day" else 0

        st.markdown('</div>', unsafe_allow_html=True)

        # Prepare input data
        input_data = pd.DataFrame({
            "Global_reactive_power": [0.0],  # Default or user-provided
            "Voltage": [voltage],
            "Global_intensity": [global_intensity],
            "Sub_metering_1": [sub_metering_1],
            "Sub_metering_2": [sub_metering_2],
            "Sub_metering_3": [sub_metering_3],
            "Year": [year],
            "Month": [month],
            "Day": [day],
            "Hour": [hour],
            "Minute": [minute],
            "Is_holiday": [is_holiday],
            "Light": [light],
            "Weekday": [weekday]
        })[self.feature_names]  # Ensure correct feature order

        # Prediction section
        try:
            prediction = self.linear_model.predict(input_data)[0]

            st.markdown('<div class="prediction-card">', unsafe_allow_html=True)
            st.subheader("🔮 Prediction")
            st.metric(label="Predicted Energy Consumption", value=f"{prediction:.2f} kW")
            st.markdown('</div>', unsafe_allow_html=True)

        except ValueError as e:
            st.error(f"Prediction error: {e}")

        st.markdown("---")
        st.markdown("### 📜 Disclaimer")
        st.warning("""
        **Important Notice:**
        - This tool provides energy consumption predictions based on historical data.
        - It is intended for informational purposes only.
        - For critical energy planning, consult a certified energy expert.
        """)

# Main function to run the app
def main():
    app = EnergyConsumptionApp()
    app.run()

if __name__ == "__main__":
    main()
