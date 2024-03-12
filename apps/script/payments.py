import pandas as pd

class CleanPayments:
    @staticmethod
    def clean(df):
        # Filter DataFrame for voucher payments
        voucher_payments = df[df['payment_type'] == 'voucher']
        
        # Replace credit_card, debit_card, and boleto with card
        df['payment_type'] = df['payment_type'].replace(['credit_card', 'debit_card', 'boleto'], 'card')

        # Assuming 'have_voucher' column is based on the payment type
        df['have_voucher'] = df['payment_type'] == 'voucher'

        # Calculate voucher amount per order
        voucher_amounts = voucher_payments.groupby("order_id")["payment_value"].transform("sum")

        # Add voucher_amount column to the original DataFrame
        df["voucher_amount"] = voucher_amounts

        return df.head()

# Read the CSV file into a DataFrame
df_payments = pd.read_csv('data/olist_order_payments_dataset.csv')

# Clean the DataFrame
cleaned_df = CleanPayments.clean(df_payments)
