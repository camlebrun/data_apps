from script.rfm import RfmAnalysis
import streamlit as st

st.set_page_config(page_title='RFM Analysis', layout='wide')

# Create an instance of RfmAnalysis
analysis = RfmAnalysis()

# Load and clean the payment data
payment_data = analysis.payments

# Call the calculate_rfm method with the payment data
rfm_data = analysis.calculate_rfm(payment_data)
st.dataframe(rfm_data)
e