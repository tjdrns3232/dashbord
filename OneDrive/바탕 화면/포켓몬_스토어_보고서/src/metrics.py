from src.data_loader import *
import pandas as pd
import numpy as np

class MarketingMetrics:

    @staticmethod
    def get_total_revenue():
        """총 매출"""
        daily_sales = load_daily_sales()
        return daily_sales['sales'].sum()

    @staticmethod
    def get_total_transactions():
        """총 거래 건수"""
        daily_sales = load_daily_sales()
        return daily_sales['transactions'].sum()

    @staticmethod
    def get_total_customers():
        """총 고객 수"""
        customer_data = load_customer_data()
        return len(customer_data)

    @staticmethod
    def get_avg_transaction_value():
        """평균 거래액"""
        daily_sales = load_daily_sales()
        total_revenue = daily_sales['sales'].sum()
        total_transactions = daily_sales['transactions'].sum()
        return total_revenue / total_transactions if total_transactions > 0 else 0

    @staticmethod
    def get_daily_growth_rate():
        """일일 성장률 (%)"""
        daily_sales = load_daily_sales()
        if len(daily_sales) < 2:
            return 0
        recent = daily_sales['sales'].iloc[-7:].mean()
        previous = daily_sales['sales'].iloc[-14:-7].mean()
        return ((recent - previous) / previous * 100) if previous > 0 else 0

    @staticmethod
    def get_campaign_roi():
        """캠페인별 ROI (%)"""
        campaign = load_campaign_data()
        campaign['roi'] = ((campaign['revenue'] - campaign['budget']) / campaign['budget'] * 100).round(2)
        return campaign[['campaign_name', 'budget', 'revenue', 'roi']].sort_values('roi', ascending=False)

    @staticmethod
    def get_campaign_ctr():
        """캠페인별 클릭율 (%) - CTR"""
        campaign = load_campaign_data()
        campaign['ctr'] = (campaign['clicks'] / campaign['impressions'] * 100).round(2)
        return campaign[['campaign_name', 'clicks', 'impressions', 'ctr']]

    @staticmethod
    def get_campaign_conversion_rate():
        """캠페인별 전환율 (%)"""
        campaign = load_campaign_data()
        campaign['conversion_rate'] = (campaign['conversions'] / campaign['clicks'] * 100).round(2)
        return campaign[['campaign_name', 'conversions', 'clicks', 'conversion_rate']]

    @staticmethod
    def get_top_products(n=5):
        """상위 상품 (매출 기준)"""
        products = load_product_sales()
        return products.groupby('product').agg({
            'revenue': 'sum',
            'quantity_sold': 'sum'
        }).sort_values('revenue', ascending=False).head(n)

    @staticmethod
    def get_customer_segmentation():
        """고객 세그먼트별 통계"""
        customer = load_customer_data()
        return customer.groupby('customer_segment').agg({
            'customer_id': 'count',
            'total_purchase': ['sum', 'mean']
        }).round(0)

    @staticmethod
    def get_customer_rfm():
        """RFM 분석 (Recency, Frequency, Monetary)"""
        customer = load_customer_data()

        rfm = pd.DataFrame({
            'Recency': 180 - customer['last_purchase_days'],
            'Frequency': customer['purchase_frequency'],
            'Monetary': customer['total_purchase']
        })

        return {
            'avg_recency': rfm['Recency'].mean().round(0),
            'avg_frequency': rfm['Frequency'].mean().round(1),
            'avg_monetary': rfm['Monetary'].mean().round(0)
        }

    @staticmethod
    def get_channel_performance():
        """채널별 성과"""
        campaign = load_campaign_data()
        return campaign[['channel', 'impressions', 'clicks', 'conversions', 'revenue']].sort_values('revenue', ascending=False)

    @staticmethod
    def get_weekly_sales():
        """주간 판매 추이"""
        daily_sales = load_daily_sales()
        daily_sales['week'] = daily_sales['date'].dt.isocalendar().week
        return daily_sales.groupby('week').agg({
            'sales': 'sum',
            'transactions': 'sum',
            'customers': 'sum'
        }).reset_index()
