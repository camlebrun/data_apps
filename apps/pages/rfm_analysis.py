import streamlit as st
import pandas as pd
import plotly.express as px
from apps.script.gold.rfm import RFMAnalysis

# Load the data
df = pd.read_csv('data/cleaned_payments.csv')

# Introduction
st.title('RFM Analysis Dashboard')
st.write('Welcome to the RFM Analysis Dashboard! This dashboard provides insights into customer behavior based on Recency, Frequency, and Monetary (RFM) analysis.')

# Sidebar
st.sidebar.title('Options')
export_button = st.sidebar.button('Export RFM data to CSV')

# Use the RFMAnalysis class to perform RFM analysis
rfm_analysis = RFMAnalysis(df)  
rfm_result = rfm_analysis.calculate_rfm()

# Recency distribution (R)
st.header('Recency Distribution (R)')
st.write('Recency refers to the number of days since the customer\'s last purchase.')
fig_recency = px.histogram(rfm_result, x='Recency', nbins=20, title='Recency Distribution (R)')
st.plotly_chart(fig_recency)

# Frequency distribution (F)
st.header('Frequency Distribution (F)')
st.write('Frequency represents the number of purchases made by each customer.')
fig_frequency = px.histogram(rfm_result, x='Frequency', nbins=20, title='Frequency Distribution (F)')
st.plotly_chart(fig_frequency)

# Monetary value distribution (M)
st.header('Monetary Value Distribution (M)')
st.write('Monetary value reflects the total amount spent by each customer.')
fig_monetary = px.histogram(rfm_result, x='Monetary', nbins=20, title='Monetary Value Distribution (M)')
st.plotly_chart(fig_monetary, use_container_width=True)

# Summary statistics for RFM
st.header('Summary Statistics for RFM')
st.write('Here are the summary statistics for Recency, Frequency, and Monetary.')
st.dataframe(rfm_result.describe(), use_container_width=True)

# Top 10 customers for each RFM
st.header('Top 10 Customers for each RFM')
st.write('Here are the top 10 customers based on Recency, Frequency, and Monetary.')
top_recency = rfm_result.sort_values(by='Recency').head(10)
top_frequency = rfm_result.sort_values(by='Frequency', ascending=False).head(10)
top_monetary = rfm_result.sort_values(by='Monetary', ascending=False).head(10)
st.subheader('Top 10 by Recency')
st.dataframe(top_recency,use_container_width=True)
st.subheader('Top 10 by Frequency')
st.dataframe(top_frequency,use_container_width=True)
st.subheader('Top 10 by Monetary Value')
st.dataframe(top_monetary,use_container_width=True)

# RFM Segmentation visualization
st.header('RFM Segmentation')
st.write('RFM Segmentation divides customers into four segments based on their RFM scores.')
rfm_result['RFM_Score'] = rfm_result[['Recency', 'Frequency', 'Monetary']].sum(axis=1)
rfm_result['RFM_Segment'] = pd.qcut(rfm_result['RFM_Score'], q=4, labels=['Low', 'Medium', 'High', 'Very High'])
rfm_counts = rfm_result['RFM_Segment'].value_counts().reset_index()
rfm_counts.columns = ['RFM_Segment', 'Number of customers']
fig_segmentation = px.bar(rfm_counts, x='RFM_Segment', y='Number of customers', title='RFM Segmentation')
st.plotly_chart(fig_segmentation)

# Export RFM data
if export_button:
    rfm_result.to_csv('rfm_analysis_result.csv', index=False)
    st.success('RFM data exported successfully to CSV format.')
