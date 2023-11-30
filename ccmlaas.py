# -*- coding: utf-8 -*-
"""CCMLaaS

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1plsUh2T6j3mX4Qn1TzCVuklHA6W9PYSw
"""

import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

# Sample Data
data = pd.read_csv('MLData.csv')

# Preprocess the data
label_encoder = LabelEncoder()
data['Mat_L'] = label_encoder.fit_transform(data['Mat_L'])

# Train a simple RandomForestClassifier
X = data[['AHT', 'NTT', 'Sentiment', 'Complaints', 'Repeats']]
y = data['Mat_L']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
clf = RandomForestClassifier()
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# Streamlit App
st.title("Maturity Level Prediction App")

# Model Accuracy in percentage
st.sidebar.text(f'Model Accuracy: {accuracy*100:.2f}%')

# Sliders for user input
aht = st.slider("Average Handling Time (AHT)", min_value=data['AHT'].min(), max_value=data['AHT'].max())
ntt = st.slider("Net Transfer Time (NTT)", min_value=data['NTT'].min(), max_value=data['NTT'].max())
sentiment = st.slider("Sentiment", min_value=data['Sentiment'].min(), max_value=data['Sentiment'].max())
complaints = st.slider("Complaints", min_value=data['Complaints'].min(), max_value=data['Complaints'].max())
repeats = st.slider("Repeats", min_value=data['Repeats'].min(), max_value=data['Repeats'].max())

# Predict Maturity Level
input_data = [[aht, ntt, sentiment, complaints, repeats]]
prediction = clf.predict(input_data)[0]
prediction_proba = clf.predict_proba(input_data)

# Display Prediction
st.write(f"Predicted Maturity Level: {label_encoder.inverse_transform([prediction])[0]}")

# Display Probability Distribution with Maturity Levels
fig, ax = plt.subplots()
probabilities = prediction_proba[0]
maturity_levels = label_encoder.classes_
sns.barplot(x=maturity_levels, y=probabilities, ax=ax)
ax.set(title='Maturity Level Probabilities', xlabel='Maturity Level', ylabel='Probability')
for i, value in enumerate(probabilities):
    ax.text(i, value + 0.01, f'{maturity_levels[i]}: {value:.2f}', ha='center', va='bottom')
st.pyplot(fig)

# Instructions section
st.sidebar.title("Instructions:")
st.sidebar.markdown("- Adjust the sliders to set your performance on key KPIs.")
st.sidebar.markdown("- The model will predict your Maturity Level.")
st.sidebar.markdown("- Model accuracy is displayed on the left.")
st.sidebar.markdown("- The graph shows the probability distribution for each Maturity Level.")
st.sidebar.markdown("- Send the prediction graph to your email using the button below.")

# Allow the user to send the graph via email
if st.button("Send Email"):
    # Email configuration (Gmail example)
    email_sender = 'your_email@gmail.com'
    email_receiver = 'user_email@example.com'
    email_password = 'your_email_password'

    # Create MIME object
    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email_receiver
    msg['Subject'] = 'Maturity Level Prediction'

    # Attach the graph
    plt.savefig('prediction_graph.png')
    msg.attach(MIMEText("Please find the Maturity Level Prediction graph attached."))
    with open("prediction_graph.png", "rb") as f:
        attachment = MIMEText(f.read())
        attachment.add_header('Content-Disposition', 'attachment', filename="prediction_graph.png")
        msg.attach(attachment)

    # Send email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(email_sender, email_password)
        server.sendmail(email_sender, email_receiver, msg.as_string())

    st.success("Email sent successfully!")

# Run the app with: streamlit run app.py