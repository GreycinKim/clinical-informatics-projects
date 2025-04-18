import streamlit as st
import pandas as pd

st.title('Patient Vitals Dashboard')

uploaded_file = st.file_uploader('Upload patient data', type='csv')
def highlight_alerts(row):
    if "Fever" in row['Alerts']:
        return ['background-color: #FFDCDC'] * len(row)  # light red
    elif "Low Oxygen" in row['Alerts']:
        return ['background-color: #FFF2CC'] * len(row)  # light yellow
    elif "High Heart Rate" in row['Alerts']:
        return ['background-color: #FFE5B4'] * len(row)  # orange tint
    elif "High Systolic" in row['Alerts'] or "High Diastolic" in row['Alerts']:
        return ['background-color: #E0F7FA'] * len(row)  # light blue
    else:
        return [''] * len(row)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    for index, row in df.iterrows():
        alerts = []

        heart_rate = row['Heart Rate (bpm)']
        oxygen = row['Oxygen Saturation (%)']
        temp = row['Temperature (F)']

        bp = row['Blood Pressure']
        systolic, diastolic = bp.split("/")
        systolic = int(systolic)
        diastolic = int(diastolic)

        if heart_rate > 100:
            alerts.append("High Heart Rate")
        if systolic > 140:
            alerts.append("High Systolic")
        if diastolic > 90:
            alerts.append("High Diastolic")
        if oxygen < 92:
            alerts.append("Low Oxygen")
        if temp > 99.5:
            alerts.append("Fever")
        alert_string = ", ".join(alerts)
        df.at[index, 'Alerts'] = alert_string
    only_alerts = df[df['Alerts'] != ""]
    total_patients = len(df)
    total_alerts = len(only_alerts)
    high_hr_count = df['Alerts'].str.contains("High Heart Rate").sum()
    fever_count = df['Alerts'].str.contains("Fever").sum()
    high_bp = df['Alerts'].str.contains("High Systolic|High Diastolic").sum()
    low_oxygen = df['Alerts'].str.contains("Low Oxygen").sum()

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Patients", total_patients)
    with col2:
        st.metric("Patients with Alerts", total_alerts)

    col3, col4, col5, col6 = st.columns(4)
    with col3:
        st.metric("High Heart Rate", high_hr_count)
    with col4:
        st.metric("Fever", fever_count)
    with col5:
        st.metric("High BP", high_bp)
    with col6:
        st.metric("Low Oxygen", low_oxygen)

    alert_options = ["All", "Fever", "High Heart Rate", "High Systolic", "High Diastolic", "Low Oxygen"]
    selected_alert = st.selectbox("Filter by Alert Type", alert_options)

    if selected_alert == "All":
        filtered_df = df
    else:
        filtered_df = df[df['Alerts'].str.contains(selected_alert)]

    st.dataframe(filtered_df.style.apply(highlight_alerts, axis=1))


