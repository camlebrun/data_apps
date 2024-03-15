import streamlit as st
import pandas as pd
import plotly.express as px
from script.gold.rfm import RFMAnalysis

st.set_page_config(page_title='RFM Analysis', layout='wide')

# Load the data
df = pd.read_csv('data/cleaned_payments.csv')

# Introduction
st.title('RFM Analysis Dashboard')
st.write('Welcome to the RFM Analysis Dashboard! This dashboard provides insights into customer behavior based on Recency, Frequency, and Monetary (RFM) analysis.')
st.info('RFM analysis is a marketing technique used to determine quantitatively which customers are the best ones by examining how recently a customer has purchased (Recency), how often they purchase (Frequency), and how much the customer spends (Monetary).')

# Sidebar
st.sidebar.title('Options')
export_button = st.sidebar.button('Export RFM data to CSV')

# Use the RFMAnalysis class to perform RFM analysis
rfm_analysis = RFMAnalysis(df)
rfm_result = rfm_analysis.calculate_rfm()
col1, col2, col3 = st.columns(3)

# Recency distribution (R)
fig_recency = px.histogram(
    rfm_result,
    x='Recency',
    nbins=20,
    title='Recency Distribution (R)')

# Frequency distribution (F)
fig_frequency = px.histogram(
    rfm_result,
    x='Frequency',
    nbins=20,
    title='Frequency Distribution (F)')

# Monetary value distribution (M)
st.header('Monetary Value Distribution (M)')
st.write('Monetary value reflects the total amount spent by each customer.')
fig_monetary = px.histogram(
    rfm_result,
    x='Monetary',
    nbins=20,
    title='Monetary Value Distribution (M)')

# Summary statistics for RFM
st.dataframe(rfm_result.describe(), use_container_width=True)

# boxplot for each RFM
st.header('RFM Boxplot')
st.write('The boxplots below show the distribution of Recency, Frequency, and Monetary values.')

# Creating individual boxplots for Recency, Frequency, and Monetary
fig_recency_box = px.box(rfm_result, y='Recency', title='Recency Boxplot')
fig_frequency_box = px.box(
    rfm_result,
    y='Frequency',
    title='Frequency Boxplot')
fig_monetary_box = px.box(rfm_result, y='Monetary', title='Monetary Boxplot')

# Displaying the boxplots on 3 columns
col1_box, col2_box, col3_box = st.columns(3)
with col1_box:
    st.plotly_chart(fig_recency_box, use_container_width=True)
with col2_box:
    st.plotly_chart(fig_frequency_box, use_container_width=True)
with col3_box:
    st.plotly_chart(fig_monetary_box, use_container_width=True)

# Top 10 customers for each RFM
st.header('Top 10 Customers for each RFM')
st.write('Here are the top 10 customers based on Recency, Frequency, and Monetary.')

top_recency = rfm_result.sort_values(by='Recency').head(10)
top_frequency = rfm_result.sort_values(
    by='Frequency', ascending=False).head(10)
top_monetary = rfm_result.sort_values(by='Monetary', ascending=False).head(10)

with col1:
    st.write('### Recency Distribution (R)')
    st.write(
        'Recency refers to the number of days since the customer\'s last purchase.')
    st.plotly_chart(fig_recency, use_container_width=True)

with col2:
    st.write('### Frequency Distribution (F)')
    st.write('Frequency represents the number of purchases made by each customer.')
    st.plotly_chart(fig_frequency, use_container_width=True)

with col3:
    st.write('### Monetary Value Distribution (M)')
    st.write('Monetary value reflects the total amount spent by each customer.')
    st.plotly_chart(fig_monetary, use_container_width=True)

colr, colf, colm = st.columns(3)
with colr:
    st.subheader('Top 10 by Recency')
    st.dataframe(top_recency, use_container_width=True)
with colf:
    st.subheader('Top 10 by Frequency')
    st.dataframe(top_frequency, use_container_width=True)
with colm:
    st.subheader('Top 10 by Monetary Value')
    st.dataframe(top_monetary, use_container_width=True)

st.header('RFM Segmentation')
rfm_data_with_labels = rfm_analysis.calculate_labels(rfm_result)

# Further processing and visualization
rfm_data_with_labels['RFM_Segment'] = rfm_data_with_labels['recency_label'].astype(
    str) + rfm_data_with_labels['frequency_label'].astype(str) + rfm_data_with_labels['monetary_label'].astype(str)
rfm_data_with_labels['RFM_Score'] = rfm_data_with_labels[[
    'recency_label', 'frequency_label', 'monetary_label']].sum(axis=1)
rfm_data_with_labels['RFM_Score'] = rfm_data_with_labels['RFM_Score'].astype(
    int)
rfm_data_with_labels['RFM_Segment'] = rfm_data_with_labels['RFM_Segment'].astype(
    int)

# Displaying the results
st.dataframe(rfm_data_with_labels, use_container_width=True)
with st.expander("RFM Label Calculation", expanded=False):
    st.markdown("""
    This function computes RFM labels for each customer based on their Recency, Frequency, and Monetary (RFM) values.
    Here's how it works:

    - **Recency Labels:** Customers are categorized into four groups based on their recency of purchase.
      The recency labels are determined by dividing the range of recency values into quartiles:
      - *Label 1:* Least recent customers
      - *Label 2:* Moderately recent customers
      - *Label 3:* Fairly recent customers
      - *Label 4:* Most recent customers

    - **Monetary Labels:** Customers are categorized into four groups based on their monetary value of purchases.
      The monetary labels are determined by dividing the range of monetary values into quartiles:
      - *Label 4:* High-spending customers
      - *Label 3:* Moderate-spending customers
      - *Label 2:* Low-spending customers
      - *Label 1:* Minimal-spending customers

    - **Frequency Labels:** Customers are categorized into four groups based on the frequency of their purchases:
      - *Label 4:* Most frequent customers
      - *Label 3:* Moderately frequent customers
      - *Label 2:* Infrequent customers
      - *Label 1:* Least frequent customers

    - **RFM Rank and RFM Rank RM:** These columns combine the Recency, Frequency, and Monetary labels to create a comprehensive RFM ranking for each customer. RFM Rank RM excludes Frequency from the ranking.

    The resulting DataFrame includes these RFM labels and rankings for further analysis and segmentation of customers.
    """)

# Export RFM data
if export_button:
    rfm_result.to_csv('rfm_analysis_result.csv', index=False)
    st.success('RFM data exported successfully to CSV format.')

# vizualization of RFM segments using a treemap
st.header('RFM Segmentation')
st.write('Cluster analysis is a type of data classification carried out by separating the data into groups. In this case, we are segmenting customers into different groups based on their RFM values.')
fig =px.scatter(rfm_data_with_labels, x='Recency', y='Frequency', color='RFM_Segment', title='RFM Segments')
st.plotly_chart(fig, use_container_width=True)


# Search functionality to find the best customers according to RFM criteria
st.header('Search for the best customers')
selected_params = st.multiselect(
    'Select RFM parameters:', [
        'Recency', 'Frequency', 'Monetary'])

if selected_params:
    search_results = rfm_data_with_labels.copy()
    for param in selected_params:
        if param == 'Recency':
            recency_labels = st.multiselect(
                'Select Recency labels:', [
                    '1', '2', '3', '4'], default=['4'])
            search_results = search_results[search_results['recency_label'].astype(
                str).isin(recency_labels)]
        elif param == 'Frequency':
            frequency_labels = st.multiselect(
                'Select Frequency labels:', [
                    '1', '2', '3', '4'], default=['4'])
            search_results = search_results[search_results['frequency_label'].astype(
                str).isin(frequency_labels)]
        elif param == 'Monetary':
            monetary_labels = st.multiselect(
                'Select Monetary labels:', [
                    '1', '2', '3', '4'], default=['4'])
            search_results = search_results[search_results['monetary_label'].astype(
                str).isin(monetary_labels)]

    st.subheader("Search Results:")
    st.dataframe(search_results)
