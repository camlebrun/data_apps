class SellersTable:
    @staticmethod
    def clean(df):
        import pandas as pd
        df_items = pd.read_csv('data/olist_order_items_dataset.csv')
        # Add seller information
        df_sellers = pd.read_csv('data/olist_sellers_dataset.csv')
        cleaned_df = pd.merge(df_items, df_sellers, on="seller_id", how="left")
        print(cleaned_df.head())
        return cleaned_df
    @staticmethod
    def kpi(df):
      """
      
      """