import pandas as pd
import os

def load_daily_sales():
    df = pd.read_csv('data/raw/daily_sales.csv')
    df['date'] = pd.to_datetime(df['date'])
    return df

def load_product_sales():
    df = pd.read_csv('data/raw/product_sales.csv')
    return df

def load_campaign_data():
    df = pd.read_csv('data/raw/campaign_data.csv')
    return df

def load_customer_data():
    df = pd.read_csv('data/raw/customer_data.csv')
    df['join_date'] = pd.to_datetime(df['join_date'])
    return df

def load_hourly_sales():
    df = pd.read_csv('data/raw/hourly_sales.csv')
    return df

def get_date_range():
    """현재 데이터의 날짜 범위 반환"""
    daily_sales = load_daily_sales()
    return daily_sales['date'].min(), daily_sales['date'].max()
