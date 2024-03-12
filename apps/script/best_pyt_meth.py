class BestPayMeth:
    @staticmethod
    def clean(df):
        import pandas as pd
      
      # Read the payment dataframe
        payment = pd.read_csv('data/olist_order_payments_dataset.csv')


        return payment
    @staticmethod
    def kpi(df):

        
        # Group by to have the list of 
        
        paym_type=payment_type_rd.groupby('payment_type')['payment_value'].sum().reset_index()


        # Displaying the total sales per state
        print(paym_type)




        return {'Sales per states': sales_per_state}
