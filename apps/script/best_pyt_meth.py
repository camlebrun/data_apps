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
        
        paym_type=payment_type_rd.groupby('payment_type')['order_id'].count()
        paym_type=payment_type_rd.map("R${:,.0f}K".format)

        # Displaying the payment type per payment mean
        print(paym_type)




        return {'Sales per states': sales_per_state}
