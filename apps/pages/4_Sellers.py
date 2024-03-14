import streamlit as st
import pandas as pd
import plotly.express as px
from script.sellers import SellersTable
from script.gold.gold_sellers import KpiSellers

st.set_page_config(page_title='Sellers', layout='wide')

st.title('Sellers Table')

# Create an instance of KpiSellers
kpi_sellers = KpiSellers('data/cleaned_sellers.csv')

# Get the cleaned sellers DataFrame
cleaned_sellers_df = kpi_sellers.data

# Calculate KPIs
sellers_kpi = kpi_sellers.kpi(cleaned_sellers_df)

# Display metrics
col_1, col_2 = st.columns(2)
with col_1:
    st.metric('Total Sellers', sellers_kpi['Total Sellers'])
    st.metric('Total Items', sellers_kpi['Total Items'])
with col_2:
    st.metric('Average Items per Seller',
              sellers_kpi['Average Items per Seller'])

# Plot top 10 sellers
fig_top_10_sellers = px.bar(x=sellers_kpi['Count seller'].index,
                            y=sellers_kpi['Count seller'].values,
                            title='Top 10 Sellers',
                            labels={'x': 'Seller ID', 'y': 'Items'})
st.plotly_chart(fig_top_10_sellers, use_container_width=True)

# Plot top 10 cities
fig_top_10_cities = px.bar(x=sellers_kpi['Count seller state'].index,
                           y=sellers_kpi['Count seller state'].values,
                           title='Top 10 State',
                           labels={'x': 'State', 'y': 'Items'})
fig_top_10_cities.update_layout(xaxis={'categoryorder': 'total descending'})
st.plotly_chart(fig_top_10_cities, use_container_width=True)
