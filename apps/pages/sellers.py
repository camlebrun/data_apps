import streamlit as st
import pandas as pd
import plotly.express as px
from script.sellers import SellersTable

st.set_page_config(page_title='Sellers', layout='wide')

st.title('Sellers Table')
df_sellers = pd.read_csv('data/olist_order_items_dataset.csv')
df_info = SellersTable.clean(df_sellers)

col_1, col_2 = st.columns(2)
with col_1:
    st.metric('Total Sellers', SellersTable.kpi(df_info)['Total Sellers'])
    st.metric('Total Items', SellersTable.kpi(df_info)['Total Items'])
with col_2:
    st.metric('Average Items per Seller', SellersTable.kpi(df_info)['Average Items per Seller'])


fig = px.bar(SellersTable.kpi(df_info)['Count seller']
                , x=SellersTable.kpi(df_info)['Count seller'].index
                , y=SellersTable.kpi(df_info)['Count seller'].values
                , title='Top 10 Sellers'
                , labels={'x':'Seller ID', 'y':'Items'}
                )
st.plotly_chart(fig, use_container_width=True)

# fig state seller
fig = px.bar(SellersTable.kpi(df_info)['Count seller state']
                , x=SellersTable.kpi(df_info)['Count seller state'].index
                , y=SellersTable.kpi(df_info)['Count seller state'].values
                , title='Top 10 Cities'
                , labels={'x':'City', 'y':'Items'}
                )
st.plotly_chart(fig, use_container_width=True)