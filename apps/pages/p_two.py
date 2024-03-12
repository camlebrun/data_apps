import streamlit as st
import pandas as pd
from script.payments import CleanPayments

df_payments = pd.read_csv('data/olist_order_payments_dataset.csv')

# Clean the DataFrame
cleaned_df = CleanPayments.clean(df_payments)

st.write(cleaned_df)
