import pandas as pd
import os
import numpy as np
from datetime import datetime, timedelta

def _generate_sample_data_if_missing():
    """데이터 파일이 없으면 샘플 데이터 생성"""
    os.makedirs('data/raw', exist_ok=True)

    # daily_sales.csv가 없으면 생성
    if not os.path.exists('data/raw/daily_sales.csv'):
        np.random.seed(42)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=180)
        dates = pd.date_range(start_date, end_date, freq='D')

        daily_sales = pd.DataFrame({
            'date': dates,
            'sales': np.random.randint(5000, 25000, len(dates)) + np.sin(np.arange(len(dates))/30) * 3000,
            'transactions': np.random.randint(100, 500, len(dates)),
            'customers': np.random.randint(80, 400, len(dates))
        })
        daily_sales['sales'] = daily_sales['sales'].astype(int)
        daily_sales.to_csv('data/raw/daily_sales.csv', index=False)

    # product_sales.csv가 없으면 생성
    if not os.path.exists('data/raw/product_sales.csv'):
        products = ['포켓볼', '포켓몬 카드', '피규어', '의류', '가방', '액세서리', 'USB', '모자']
        categories = ['장난감', '장난감', '장난감', '의류', '의류', '액세서리', '액세서리', '액세서리']
        n_records = len(products) * 10

        product_sales = pd.DataFrame({
            'product': [p for p in products for _ in range(10)],
            'category': [c for c in categories for _ in range(10)],
            'sales_amount': np.random.randint(1000, 50000, n_records),
            'quantity_sold': np.random.randint(10, 500, n_records),
            'revenue': np.random.randint(10000, 200000, n_records)
        })
        product_sales.to_csv('data/raw/product_sales.csv', index=False)

    # campaign_data.csv가 없으면 생성
    if not os.path.exists('data/raw/campaign_data.csv'):
        campaigns = ['SNS 광고', '이메일 마케팅', '인플루언서 협업', '프모션', '컨텐츠 마케팅', '파트너쉽']
        campaign_data = pd.DataFrame({
            'campaign_name': campaigns,
            'channel': ['소셜미디어', '이메일', '인플루언서', '직접판매', '콘텐츠', '협력'],
            'budget': [50000, 30000, 80000, 40000, 25000, 60000],
            'clicks': [15000, 8000, 25000, 12000, 6000, 18000],
            'impressions': [500000, 200000, 800000, 100000, 300000, 400000],
            'conversions': [450, 200, 750, 400, 300, 550],
            'revenue': [45000, 20000, 150000, 40000, 30000, 55000]
        })
        campaign_data.to_csv('data/raw/campaign_data.csv', index=False)

    # customer_data.csv가 없으면 생성
    if not os.path.exists('data/raw/customer_data.csv'):
        n_customers = 500
        end_date = datetime.now()
        start_date = end_date - timedelta(days=180)

        customer_data = pd.DataFrame({
            'customer_id': range(1, n_customers + 1),
            'join_date': [start_date + timedelta(days=int(x)) for x in np.random.randint(0, 180, n_customers)],
            'total_purchase': np.random.randint(10000, 500000, n_customers),
            'purchase_frequency': np.random.randint(1, 50, n_customers),
            'last_purchase_days': np.random.randint(0, 180, n_customers),
            'customer_segment': np.random.choice(['VIP', 'Regular', 'At-risk'], n_customers)
        })
        customer_data.to_csv('data/raw/customer_data.csv', index=False)

    # hourly_sales.csv가 없으면 생성
    if not os.path.exists('data/raw/hourly_sales.csv'):
        hours = list(range(24)) * 7
        hourly_sales = pd.DataFrame({
            'hour': hours,
            'day_of_week': ['월', '화', '수', '목', '금', '토', '일'] * 24,
            'sales': np.random.randint(500, 3000, len(hours))
        })
        hourly_sales.to_csv('data/raw/hourly_sales.csv', index=False)

def load_daily_sales():
    _generate_sample_data_if_missing()
    df = pd.read_csv('data/raw/daily_sales.csv')
    df['date'] = pd.to_datetime(df['date'])
    return df

def load_product_sales():
    _generate_sample_data_if_missing()
    df = pd.read_csv('data/raw/product_sales.csv')
    return df

def load_campaign_data():
    _generate_sample_data_if_missing()
    df = pd.read_csv('data/raw/campaign_data.csv')
    return df

def load_customer_data():
    _generate_sample_data_if_missing()
    df = pd.read_csv('data/raw/customer_data.csv')
    df['join_date'] = pd.to_datetime(df['join_date'])
    return df

def load_hourly_sales():
    _generate_sample_data_if_missing()
    df = pd.read_csv('data/raw/hourly_sales.csv')
    return df

def get_date_range():
    """현재 데이터의 날짜 범위 반환"""
    daily_sales = load_daily_sales()
    return daily_sales['date'].min(), daily_sales['date'].max()
