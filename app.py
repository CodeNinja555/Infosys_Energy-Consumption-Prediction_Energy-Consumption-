import pandas as pd
import streamlit as st
import plotly.graph_objs as go
import joblib

class EnergyConsumptionApp:
    def __init__(self):
        st.set_page_config(
            page_title="Energy Consumption Prediction App",
            page_icon="⚡",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        self.setup_page()
        self.load_resources()

    def setup_page(self):
        # Option to change background color
        bg_color = st.sidebar.selectbox("Select Background Color", [
            "Grey", "White", "Light Blue", 
            "Light Green", "Light Yellow", 
            "Light Grey", "Light Pink"
        ])
        bg_color_code = {
            "Grey": "#F4F6F7",
            "White": "#FFFFFF",
            "Light Blue": "#E3F2FD",
            "Light Green": "#E8F5E9",
            "Light Yellow": "#FFFDE7",
            "Light Grey": "#F5F5F5",
            "Light Pink": "#FCE4EC"
        }.get(bg_color, "#FFFFFF")

        st.markdown(f"""
        <style>
        .stApp {{
            background-color: {bg_color_code};
        }}
        .main-header {{
            background: linear-gradient(135deg, #4CAF50 0%, #81C784 100%);
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 10px;
            margin-bottom: 20px;
        }}
        .prediction-card {{
            background: white;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        </style>
        """, unsafe_allow_html=True)

    def load_resources(self):
        try:
            # Load models and feature names
            self.linear_model = joblib.load("linear_model.pkl")
            self.ridge_model = joblib.load("ridge_model.pkl")
            self.feature_names = joblib.load("feature_names.pkl")
            st.success("Resources loaded successfully!")
        except Exception as e:
            st.error(f"Error loading resources: {e}")

    def run(self):
        st.markdown("<div class='main-header'><h1>⚡ Energy Consumption Prediction</h1></div>", unsafe_allow_html=True)

        st.sidebar.markdown("## ⚙️ Feature Input")

        # Feature inputs for the model
        voltage = st.sidebar.number_input("Voltage (V)", min_value=220.0, max_value=255.0, value=240.0, step=0.1)
        global_intensity = st.sidebar.number_input("Global Intensity (A)", min_value=0.0, max_value=20.0, value=4.63, step=0.01)
        sub_metering_1 = st.sidebar.number_input("Sub Metering 1 (Wh)", min_value=0.0, max_value=50.0, value=1.12, step=0.01)
        sub_metering_2 = st.sidebar.number_input("Sub Metering 2 (Wh)", min_value=0.0, max_value=50.0, value=1.30, step=0.01)
        sub_metering_3 = st.sidebar.number_input("Sub Metering 3 (Wh)", min_value=0.0, max_value=50.0, value=6.46, step=0.01)

        # DateTime inputs
        date = st.sidebar.date_input("Select Date", value=pd.Timestamp("2024-11-28"))
        time = st.sidebar.time_input("Select Time", value=pd.Timestamp("2024-11-28 12:00:00").time())

        # Convert Date and Time to derived features
        date_time = pd.Timestamp.combine(date, time)
        year = date_time.year
        month = date_time.month
        day = date_time.day
        hour = date_time.hour
        minute = date_time.minute

        # Assume default values for additional features
        is_holiday = 0  # Default: Not a holiday
        light = 1       # Default: Daylight
        weekday = date_time.weekday()  # Extract weekday (0=Monday, 6=Sunday)

        # Prepare input data with all features
        input_data = pd.DataFrame({
            "Global_reactive_power": [0.0],  # Default or user input (modify if needed)
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

        # Predictions
        try:
            linear_pred = self.linear_model.predict(input_data)[0]
            ridge_pred = self.ridge_model.predict(input_data)[0]

            # Display predictions
            st.markdown('<div class="prediction-card">', unsafe_allow_html=True)
            st.subheader("🔮 Predictions")
            st.write(f"**Predicted Energy:** {linear_pred:.2f} kW")
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
