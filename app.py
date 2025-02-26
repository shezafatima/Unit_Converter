import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(page_title="Unit Converter",layout="wide")


st.markdown("""
<style>
    .reportview-container { background: #f0f2f6; }
    .stTextInput input { font-size: 16px; }
</style>
""", unsafe_allow_html=True)


if 'history' not in st.session_state:
    st.session_state.history = []


unit_conversions = {
    "Length": {
        "Meters": 1, "Kilometers": 1000, "Centimeters": 0.01, "Millimeters": 0.001,
        "Miles": 1609.34, "Yards": 0.9144, "Feet": 0.3048, "Inches": 0.0254
    },
    "Mass": {
        "Kilograms": 1, "Grams": 0.001, "Milligrams": 0.000001, "Pounds": 0.453592,
        "Ounces": 0.0283495
    },
    "Volume": {
        "Liters": 1, "Milliliters": 0.001, "Cubic Meters": 1000, "Cups": 0.236588,
        "Gallons": 3.78541
    },
    "Temperature": "temperature",  # Special handling below
    "Speed": {
        "Meters per second": 1, "Kilometers per hour": 0.277778, "Miles per hour": 0.44704,
        "Knots": 0.514444
    },
    "Time": {
        "Seconds": 1, "Minutes": 60, "Hours": 3600, "Days": 86400
    },
    "Digital": {
        "Bytes": 1, "Kilobytes": 1024, "Megabytes": 1024**2, "Gigabytes": 1024**3,
        "Terabytes": 1024**4
    },
    "Energy": {
        "Joules": 1, "Calories": 4.184, "Kilowatt-hours": 3600000
    }
}

def convert_units(value, from_unit, to_unit, category):
    if category == "Temperature":
        # Temperature 
        if from_unit == "Celsius" and to_unit == "Fahrenheit":
            return value * 9/5 + 32
        elif from_unit == "Fahrenheit" and to_unit == "Celsius":
            return (value - 32) * 5/9
        elif from_unit == "Celsius" and to_unit == "Kelvin":
            return value + 273.15
        elif from_unit == "Kelvin" and to_unit == "Celsius":
            return value - 273.15
        elif from_unit == "Fahrenheit" and to_unit == "Kelvin":
            return (value - 32) * 5/9 + 273.15
        elif from_unit == "Kelvin" and to_unit == "Fahrenheit":
            return (value - 273.15) * 9/5 + 273.15
        return value  
    else:
        base_value = value * unit_conversions[category][from_unit]
        return round(base_value / unit_conversions[category][to_unit], 4)


st.title("Unit Converter")
st.markdown("### Convert anything with ease!")


category = st.selectbox("Select Unit Category", list(unit_conversions.keys()), key="cat")


if category == "Temperature":
    temperature_units = ["Celsius", "Fahrenheit", "Kelvin"]
    from_unit = st.selectbox("From", temperature_units, key="from_unit")
    to_unit = st.selectbox("To", temperature_units, key="to_unit")
else:
    units = list(unit_conversions[category].keys())
    from_unit = st.selectbox("From", units, key="from_unit")
    to_unit = st.selectbox("To", units, key="to_unit")

value_input = st.text_input("Enter Value", "1", key="value")
try:
    value_float = float(value_input)
except ValueError:
    st.error("Please enter a valid number!")
    value_float = None


if st.button("Convert"):
    if value_float is not None:
        result = convert_units(value_float, from_unit, to_unit, category)
        st.success(f"**{value_float} {from_unit} = {result} {to_unit}**")
        st.session_state.history.append({
            "Category": category,
            "Input": f"{value_float} {from_unit}",
            "Output": f"{result} {to_unit}"
        })
        
        
        df = pd.DataFrame({"Unit": [from_unit, to_unit], "Value": [value_float, result]})
        fig = px.bar(df, x="Unit", y="Value", title="Conversion Comparison")
        st.plotly_chart(fig, use_container_width=True)


st.sidebar.markdown("## 📚 Conversion History")
if st.session_state.history:
    history_df = pd.DataFrame(st.session_state.history)
    history_df.index = history_df.index + 1
    st.sidebar.dataframe(history_df, use_container_width=True)
    if st.sidebar.button("Clear History"):
        st.session_state.history.clear()
        st.rerun()
else:
    st.sidebar.info("No conversions yet!")
