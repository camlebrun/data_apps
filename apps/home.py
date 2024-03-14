import streamlit as st
st.set_page_config(page_title='Monitoring Dashboard', layout='wide')
st.markdown(
    "<h1 style='text-align: center;'> Welcome to the Monitoring Dashboard of Olist</h1>",
    unsafe_allow_html=True)
st.write("This dashboard provides insights into the performance of Olist's business operations. The dashboard is divided into four sections: **RFM Analysis**, **Payments Method**, **Revenues**, and **Orders**. You can navigate to each section using the sidebar on the left.")
st.write("The dashboard is designed to help Olist's management team to monitor the company's performance and make data-driven decisions.")
st.write("To get started, select a section from the sidebar.")
