import pandas as pd
import os

class SellersTable:
    def __init__(self, items_path='data/olist_order_items_dataset.csv', sellers_path='data/olist_sellers_dataset.csv', geo_path='data/olist_geolocation_dataset.csv', last_index_file='last_index.txt'):
        self.df_items = pd.read_csv(items_path)
        self.df_sellers = pd.read_csv(sellers_path)
        self.df_geo = pd.read_csv(geo_path)
        self.last_index_file = last_index_file
        self.last_index = self.load_last_index()

    def load_last_index(self):
        if os.path.exists(self.last_index_file):
            with open(self.last_index_file, 'r') as file:
                return int(file.readline().strip())
        else:
            return 0

    def save_last_index(self, index):
        with open(self.last_index_file, 'w') as file:
            file.write(str(index))

    def get_last_index(self):
        return self.last_index

    def incremental_update(self):
        new_data = self.retrieve_new_data()  # Retrieve new data based on the last index
        if new_data.empty:
            print("No new data to process.")
            return
        cleaned_df = self.clean(new_data)  # Process the new data
        self.save_last_index(len(self.df_items))  # Update the last index
        print("Incremental update completed.")

    def retrieve_new_data(self):
        if self.last_index < len(self.df_items):
            new_data = self.df_items.iloc[self.last_index:]
        else:
            new_data = pd.DataFrame()
        return new_data

    def clean(self, df):
        cleaned_df = pd.merge(df, self.df_sellers, on="seller_id", how="left")
        cleaned_df.to_csv('data/cleaned_sellers.csv', index=False)
        return cleaned_df

    @staticmethod
    def kpi(df):
        df = pd.read_csv('data/cleaned_sellers.csv')
        total_sellers = len(df['seller_id'].unique())
        total_items = len(df)
        average_items_per_seller = df.groupby('seller_id').size().mean().astype(int)
        count_seller = df['seller_id'].value_counts().sort_values(ascending=False).head(10)
        sum_price = df.groupby('seller_state')['price'].sum()
        count_seller_state = df['seller_state'].value_counts().sort_values(ascending=False).head(1000)
        count_seller_city = df['seller_city'].value_counts().sort_values(ascending=False).head(1000)

        return {
            'Total Sellers': total_sellers,
            'Total Items': total_items,
            'Average Items per Seller': average_items_per_seller,
            'Count seller': count_seller,
            'Sum price': sum_price,
            'Count seller state': count_seller_state,
            'Count seller city': count_seller_city
        }

if __name__ == "__main__":
    sellers_table = SellersTable()
    print("Last Index:", sellers_table.get_last_index())
    sellers_table.incremental_update()
