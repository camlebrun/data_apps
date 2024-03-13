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
        paym_type=payment_type_rd

        # Displaying the payment type per payment mean
        print(paym_type)




        return {'Payment type usage ': paym_type}
