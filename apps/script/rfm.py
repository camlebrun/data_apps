from .payments import CleanPayments  # Assurez-vous que le chemin d'importation est correct
import pandas as pd
class RfmAnalysis:
    def __init__(self):
        self.clean_payments = CleanPayments()  # Créez une instance de CleanPayments
        
        # Chargez les données de paiement et nettoyez-les
        df_payments = pd.read_csv('data/olist_order_payments_dataset.csv')
        self.payments = self.clean_payments.clean(df_payments)
    def calculate_rfm(self, df):  # Modify the method signature to accept a DataFrame
        df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

        # Calculate Recency, Frequency, and Monetary Value
        rfm = df.groupby('customer_id').agg({
            'order_purchase_timestamp': lambda date: (date.max() - date.max()).days,
            'order_id': 'count',
            'payment_value': 'sum'
        }).reset_index()
        rfm.rename(columns={'order_purchase_timestamp': 'recency',
                            'order_id': 'frequency',
                            'payment_value': 'monetary_value'}, inplace=True)

        return rfm


    
    def rfm_segmentation(self, rfm):
        # Create labels for Recency and Frequency
        r_labels = range(5, 0, -1)
        f_labels = range(1, 6)
        m_labels = range(1, 6)
        r_quartiles = pd.qcut(rfm['recency'], q=5, labels=r_labels)
        f_quartiles = pd.qcut(rfm['frequency'], q=5, labels=f_labels)
        m_quartiles = pd.qcut(rfm['monetary_value'], q=5, labels=m_labels)
        rfm_segmented = rfm.assign(R=r_quartiles, F=f_quartiles, M=m_quartiles)
        return rfm_segmented
    
    def rfm_score(self, rfm):
        # Calculate RFM Score
        rfm['RFM_Score'] = rfm[['R', 'F', 'M']].sum(axis=1)
        return rfm
    
    def rfm_table(self):
        df = self.payments  # Assuming payments is the DataFrame you want to pass
        rfm = self.calculate_rfm(df)
        rfm_segmented = self.rfm_segmentation(rfm)
        rfm_scored = self.rfm_score(rfm_segmented)
        return rfm_scored

