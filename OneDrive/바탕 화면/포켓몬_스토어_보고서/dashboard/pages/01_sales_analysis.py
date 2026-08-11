import streamlit as st
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.data_loader import load_daily_sales, load_product_sales, load_hourly_sales
from src.metrics import MarketingMetrics
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="판매 분석", page_icon="📈")

st.title("📈 판매 분석")
st.markdown("---")

# 탭 구성
tab1, tab2, tab3 = st.tabs(["일일 추이", "상품별 분석", "시간대별 분석"])

# 탭 1: 일일 판매 추이
with tab1:
    st.subheader("일일 판매액 추이")

    daily_sales = load_daily_sales()

    # 기간 선택
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("시작 날짜", daily_sales['date'].min())
    with col2:
        end_date = st.date_input("종료 날짜", daily_sales['date'].max())

    # 데이터 필터링
    filtered_daily = daily_sales[
        (daily_sales['date'].dt.date >= start_date) &
        (daily_sales['date'].dt.date <= end_date)
    ]

    # 통계
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("기간 총매출", f"₩{filtered_daily['sales'].sum():,.0f}")
    with col2:
        st.metric("평균 일매출", f"₩{filtered_daily['sales'].mean():,.0f}")
    with col3:
        st.metric("최고 일매출", f"₩{filtered_daily['sales'].max():,.0f}")
    with col4:
        st.metric("최저 일매출", f"₩{filtered_daily['sales'].min():,.0f}")

    # 라인 차트
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=filtered_daily['date'],
        y=filtered_daily['sales'],
        mode='lines',
        name='판매액',
        line=dict(color='#1f77b4', width=2),
        fill='tozeroy'
    ))

    fig.add_trace(go.Scatter(
        x=filtered_daily['date'],
        y=filtered_daily['sales'].rolling(7).mean(),
        mode='lines',
        name='7일 이동평균',
        line=dict(color='#ff7f0e', width=2, dash='dash')
    ))

    fig.update_layout(height=400, hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True)

    # 거래건수 및 고객수
    col1, col2 = st.columns(2)

    with col1:
        fig_trans = px.bar(
            filtered_daily,
            x='date',
            y='transactions',
            title="거래건수",
            labels={'transactions': '거래건수', 'date': '날짜'}
        )
        fig_trans.update_layout(height=350)
        st.plotly_chart(fig_trans, use_container_width=True)

    with col2:
        fig_cust = px.bar(
            filtered_daily,
            x='date',
            y='customers',
            title="고객수",
            labels={'customers': '고객수', 'date': '날짜'},
            color_discrete_sequence=['#2ca02c']
        )
        fig_cust.update_layout(height=350)
        st.plotly_chart(fig_cust, use_container_width=True)

# 탭 2: 상품별 분석
with tab2:
    st.subheader("상품별 판매 분석")

    product_sales = load_product_sales()

    # 상위 N개 상품 선택
    n_products = st.slider("상위 상품 개수", 5, 20, 10)

    top_products = product_sales.groupby('product').agg({
        'revenue': 'sum',
        'quantity_sold': 'sum',
        'sales_amount': 'count'
    }).sort_values('revenue', ascending=False).head(n_products)

    # 통계
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("평균 상품가격", f"₩{product_sales['sales_amount'].mean():,.0f}")
    with col2:
        st.metric("총 판매량", f"{product_sales['quantity_sold'].sum():,}개")
    with col3:
        st.metric("상품 종류", f"{product_sales['product'].nunique()}개")

    # 상품별 매출
    fig_revenue = px.bar(
        top_products.reset_index(),
        x='revenue',
        y='product',
        orientation='h',
        color='revenue',
        color_continuous_scale='Blues',
        title="상품별 매출액"
    )
    fig_revenue.update_layout(height=400, yaxis_title="")
    st.plotly_chart(fig_revenue, use_container_width=True)

    # 카테고리별 분석
    col1, col2 = st.columns(2)

    with col1:
        category_revenue = product_sales.groupby('category')['revenue'].sum().sort_values(ascending=False)
        fig_cat = px.pie(
            values=category_revenue.values,
            names=category_revenue.index,
            title="카테고리별 매출 비중"
        )
        fig_cat.update_layout(height=400)
        st.plotly_chart(fig_cat, use_container_width=True)

    with col2:
        category_qty = product_sales.groupby('category')['quantity_sold'].sum().sort_values(ascending=False)
        fig_qty = px.pie(
            values=category_qty.values,
            names=category_qty.index,
            title="카테고리별 판매량 비중"
        )
        fig_qty.update_layout(height=400)
        st.plotly_chart(fig_qty, use_container_width=True)

    # 상품 상세 테이블
    st.subheader("상품 상세 정보")
    detail_table = product_sales.groupby('product').agg({
        'revenue': 'sum',
        'quantity_sold': 'sum',
        'sales_amount': ['mean', 'count']
    }).round(0)
    detail_table.columns = ['총매출', '판매량', '평균가격', '판매회수']
    st.dataframe(detail_table, use_container_width=True)

# 탭 3: 시간대별 분석
with tab3:
    st.subheader("시간대별 판매 분석")

    hourly_sales = load_hourly_sales()

    # 시간대별 판매
    hourly_summary = hourly_sales.groupby('hour')['sales'].sum().sort_index()

    fig_hourly = go.Figure()
    fig_hourly.add_trace(go.Bar(
        x=hourly_summary.index,
        y=hourly_summary.values,
        marker_color='lightblue'
    ))

    fig_hourly.update_layout(
        title="시간대별 판매액",
        xaxis_title="시간",
        yaxis_title="판매액 (₩)",
        height=400
    )
    st.plotly_chart(fig_hourly, use_container_width=True)

    # 요일별 판매
    col1, col2 = st.columns(2)

    with col1:
        day_summary = hourly_sales.groupby('day_of_week')['sales'].sum()
        fig_day = px.bar(
            x=day_summary.index,
            y=day_summary.values,
            labels={'x': '요일', 'y': '판매액 (₩)'},
            title="요일별 판매액",
            color=day_summary.values,
            color_continuous_scale='Viridis'
        )
        fig_day.update_layout(height=350)
        st.plotly_chart(fig_day, use_container_width=True)

    with col2:
        day_avg = hourly_sales.groupby('day_of_week')['sales'].mean()
        fig_day_avg = px.bar(
            x=day_avg.index,
            y=day_avg.values,
            labels={'x': '요일', 'y': '평균 판매액 (₩)'},
            title="요일별 평균 판매액",
            color_discrete_sequence=['#ff7f0e']
        )
        fig_day_avg.update_layout(height=350)
        st.plotly_chart(fig_day_avg, use_container_width=True)

    # 시간대 분석 표
    st.subheader("시간대별 상세")
    hourly_detail = hourly_sales.groupby('hour').agg({
        'sales': ['sum', 'mean', 'count']
    }).round(0)
    hourly_detail.columns = ['총판매액', '평균판매액', '거래회수']
    st.dataframe(hourly_detail, use_container_width=True)
