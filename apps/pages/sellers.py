import streamlit as st
import pandas as pd
import plotly.express as px
from script.sellers import SellersTable

st.set_page_config(page_title='Sellers', layout='wide')

st.title('Sellers Table')
sellers_table = SellersTable()
cleaned_sellers_df = sellers_table.clean(sellers_table.df_items)
sellers_kpi = sellers_table.kpi(cleaned_sellers_df)

col_1, col_2 = st.columns(2)
with col_1:
    st.metric('Total Sellers', SellersTable.kpi(cleaned_sellers_df)['Total Sellers'])
    st.metric('Total Items', SellersTable.kpi(cleaned_sellers_df)['Total Items'])
with col_2:
    st.metric('Average Items per Seller', SellersTable.kpi(cleaned_sellers_df)['Average Items per Seller'])


fig = px.bar(SellersTable.kpi(cleaned_sellers_df)['Count seller']
                , x=SellersTable.kpi(cleaned_sellers_df)['Count seller'].index
                , y=SellersTable.kpi(cleaned_sellers_df)['Count seller'].values
                , title='Top 10 Sellers'
                , labels={'x':'Seller ID', 'y':'Items'}
                )
st.plotly_chart(fig, use_container_width=True)

# fig state seller
fig = px.bar(SellersTable.kpi(cleaned_sellers_df)['Count seller state']
                , x=SellersTable.kpi(cleaned_sellers_df)['Count seller state'].index
                , y=SellersTable.kpi(cleaned_sellers_df)['Count seller state'].values
                , title='Top 10 Cities'
                , labels={'x':'City', 'y':'Items'}
                )
fig.update_layout(xaxis={'categoryorder':'total descending'})
st.plotly_chart(fig, use_container_width=True)
 
# fig city seller
fig = px.bar(SellersTable.kpi(cleaned_sellers_df)['Count seller city']
                , x=SellersTable.kpi(cleaned_sellers_df)['Count seller city'].index
                , y=SellersTable.kpi(cleaned_sellers_df)['Count seller city'].values
                , title='Top 100 Cities'
                , labels={'x':'City', 'y':'Items'}
                )
fig.update_layout(xaxis={'categoryorder':'total descending'})
