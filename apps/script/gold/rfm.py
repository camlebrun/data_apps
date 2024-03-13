import pandas as pd
class RFMAnalysis:
    def __init__(self, df_data):
        self.df_data = df_data
        self.df_data['order_purchase_timestamp'] = pd.to_datetime(self.df_data['order_purchase_timestamp'])

    def calculate_recency(self):
        recency = self.df_data.groupby('customer_unique_id', as_index=False)['order_purchase_timestamp'].max()
        recency.rename(columns={'order_purchase_timestamp': 'LastPurchaseDate'}, inplace=True)  # Renommer correctement la colonne
        recent_date = self.df_data['order_purchase_timestamp'].dt.date.max()
        recency['Recency'] = recency['LastPurchaseDate'].dt.date.apply(lambda x: (recent_date - x).days)
        return recency[['customer_unique_id', 'Recency']]

    def calculate_frequency(self):
        frequency = self.df_data.groupby(["customer_unique_id"]).agg({"order_id": "nunique"}).reset_index()
        frequency.rename(columns={'order_id': 'Frequency'}, inplace=True)
        return frequency

    def calculate_monetary(self):
        monetary = self.df_data.groupby('customer_unique_id', as_index=False)['payment_value'].sum()
        monetary.rename(columns={'payment_value': 'Monetary'}, inplace=True)
        return monetary

    def calculate_rfm(self):
        recency = self.calculate_recency()
        frequency = self.calculate_frequency()
        monetary = self.calculate_monetary()

        rfm = recency.merge(frequency, on='customer_unique_id')
        rfm = rfm.merge(monetary, on='customer_unique_id')  # Ne pas supprimer la colonne 'LastPurchaseDate' ici
        return rfm
