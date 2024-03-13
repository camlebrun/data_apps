import pandas as pd

class RFMAnalysis:
    def __init__(self, df_data):
        self.df_data = df_data
        self.df_data['order_purchase_timestamp'] = pd.to_datetime(self.df_data['order_purchase_timestamp'])

    def calculate_recency(self):
        recency = self.df_data.groupby('customer_unique_id', as_index=False)['order_purchase_timestamp'].max()
        recency.rename(columns={'order_purchase_timestamp': 'LastPurchaseDate'}, inplace=True)
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
        rfm = rfm.merge(monetary, on='customer_unique_id')
        return rfm

    def calculate_labels(self, rfm):
        # Labels for Recency
        ll_r = rfm['Recency'].quantile(0.25)
        mid_r = rfm['Recency'].quantile(0.50)
        ul_r = rfm['Recency'].quantile(0.75)

        def recency_label(recent):
            if recent <= ll_r:
                return 1
            elif (recent > ll_r) and (recent <= mid_r):
                return 2
            elif (recent > mid_r) and (recent <= ul_r):
                return 3
            elif recent > ul_r:
                return 4

        rfm['recency_label'] = rfm['Recency'].apply(recency_label)

        # Labels for Monetary
        ll_m = rfm['Monetary'].quantile(0.25)
        mid_m = rfm['Monetary'].quantile(0.50)
        ul_m = rfm['Monetary'].quantile(0.75)

        def monetary_label(money):
            if money <= ll_m:
                return 4
            elif (money > ll_m) and (money <= mid_m):
                return 3
            elif (money > mid_m) and (money <= ul_m):
                return 2
            elif money > ul_m:
                return 1

        rfm['monetary_label'] = rfm['Monetary'].apply(monetary_label)

        # Labels for Frequency
        def frequency_label(frequent):
            if frequent == 1:
                return 4
            elif frequent == 2:
                return 3
            elif frequent == 3:
                return 2
            elif frequent > 3:
                return 1

        rfm['frequency_label'] = rfm['Frequency'].apply(frequency_label)

        # Create RFM rank and rank_rm columns
        rfm['Rank'] = list(zip(rfm['recency_label'], rfm['monetary_label'], rfm['frequency_label']))
        rfm['rank_rm'] = list(zip(rfm['recency_label'], rfm['monetary_label']))

        return rfm
