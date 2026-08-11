import streamlit as st
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.data_loader import load_customer_data
from src.metrics import MarketingMetrics
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="고객 인사이트", page_icon="👥")

st.title("👥 고객 인사이트")
st.markdown("---")

# 고객 데이터 로드
customer_data = load_customer_data()

# 탭 구성
tab1, tab2, tab3 = st.tabs(["세그먼트 분석", "RFM 분석", "고객 상세"])

# 탭 1: 세그먼트 분석
with tab1:
    st.subheader("고객 세그먼트 분석")

    # 세그먼트별 통계
    segment_stats = customer_data.groupby('customer_segment').agg({
        'customer_id': 'count',
        'total_purchase': ['sum', 'mean'],
        'purchase_frequency': 'mean',
        'last_purchase_days': 'mean'
    }).round(2)

    segment_stats.columns = ['고객수', '총매출', '평균구매액', '평균구매빈도', '평균마지막구매']

    # KPI
    col1, col2, col3 = st.columns(3)

    with col1:
        vip_count = len(customer_data[customer_data['customer_segment'] == 'VIP'])
        vip_revenue = customer_data[customer_data['customer_segment'] == 'VIP']['total_purchase'].sum()
        st.metric("VIP 고객", f"{vip_count}명", f"매출: ₩{vip_revenue:,.0f}")

    with col2:
        regular_count = len(customer_data[customer_data['customer_segment'] == 'Regular'])
        regular_revenue = customer_data[customer_data['customer_segment'] == 'Regular']['total_purchase'].sum()
        st.metric("일반 고객", f"{regular_count}명", f"매출: ₩{regular_revenue:,.0f}")

    with col3:
        atrisk_count = len(customer_data[customer_data['customer_segment'] == 'At-risk'])
        atrisk_revenue = customer_data[customer_data['customer_segment'] == 'At-risk']['total_purchase'].sum()
        st.metric("위험 고객", f"{atrisk_count}명", f"매출: ₩{atrisk_revenue:,.0f}")

    # 세그먼트별 분포
    col1, col2 = st.columns(2)

    with col1:
        segment_count = customer_data['customer_segment'].value_counts()
        fig_segment = px.pie(
            values=segment_count.values,
            names=segment_count.index,
            title="세그먼트별 고객 분포",
            color_discrete_map={'VIP': '#FFD700', 'Regular': '#87CEEB', 'At-risk': '#FF6B6B'}
        )
        st.plotly_chart(fig_segment, use_container_width=True)

    with col2:
        segment_revenue = customer_data.groupby('customer_segment')['total_purchase'].sum()
        fig_revenue = px.pie(
            values=segment_revenue.values,
            names=segment_revenue.index,
            title="세그먼트별 매출 비중",
            color_discrete_map={'VIP': '#FFD700', 'Regular': '#87CEEB', 'At-risk': '#FF6B6B'}
        )
        st.plotly_chart(fig_revenue, use_container_width=True)

    # 세그먼트 비교표
    st.subheader("세그먼트별 상세 지표")
    st.dataframe(segment_stats, use_container_width=True)

    # 세그먼트별 구매 패턴
    col1, col2 = st.columns(2)

    with col1:
        avg_purchase = customer_data.groupby('customer_segment')['total_purchase'].mean().sort_values(ascending=False)
        fig_avg = px.bar(
            x=avg_purchase.index,
            y=avg_purchase.values,
            title="세그먼트별 평균 구매액",
            labels={'x': '세그먼트', 'y': '평균 구매액 (₩)'},
            color=avg_purchase.values,
            color_continuous_scale='Viridis'
        )
        fig_avg.update_layout(height=350)
        st.plotly_chart(fig_avg, use_container_width=True)

    with col2:
        avg_freq = customer_data.groupby('customer_segment')['purchase_frequency'].mean().sort_values(ascending=False)
        fig_freq = px.bar(
            x=avg_freq.index,
            y=avg_freq.values,
            title="세그먼트별 평균 구매 빈도",
            labels={'x': '세그먼트', 'y': '평균 구매 빈도'},
            color_discrete_sequence=['#2ca02c']
        )
        fig_freq.update_layout(height=350)
        st.plotly_chart(fig_freq, use_container_width=True)

# 탭 2: RFM 분석
with tab2:
    st.subheader("RFM 분석")

    rfm = MarketingMetrics.get_customer_rfm()

    # RFM 메트릭
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("평균 Recency (최근성)", f"{rfm['avg_recency']:.0f}일", delta="최근 구매까지의 기간")

    with col2:
        st.metric("평균 Frequency (빈도)", f"{rfm['avg_frequency']:.1f}회", delta="누적 구매 횟수")

    with col3:
        st.metric("평균 Monetary (금액)", f"₩{rfm['avg_monetary']:,.0f}", delta="누적 구매 금액")

    # RFM 점수 계산
    customer_rfm = pd.DataFrame({
        'Recency': 180 - customer_data['last_purchase_days'],
        'Frequency': customer_data['purchase_frequency'],
        'Monetary': customer_data['total_purchase']
    })

    # 분포 차트
    col1, col2, col3 = st.columns(3)

    with col1:
        fig_r = px.histogram(
            customer_rfm,
            x='Recency',
            nbins=30,
            title='Recency 분포',
            labels={'Recency': '최근성 (일)'}
        )
        fig_r.update_layout(height=350)
        st.plotly_chart(fig_r, use_container_width=True)

    with col2:
        fig_f = px.histogram(
            customer_rfm,
            x='Frequency',
            nbins=30,
            title='Frequency 분포',
            labels={'Frequency': '구매 빈도'}
        )
        fig_f.update_layout(height=350)
        st.plotly_chart(fig_f, use_container_width=True)

    with col3:
        fig_m = px.histogram(
            customer_rfm,
            x='Monetary',
            nbins=30,
            title='Monetary 분포',
            labels={'Monetary': '구매액 (₩)'}
        )
        fig_m.update_layout(height=350)
        st.plotly_chart(fig_m, use_container_width=True)

    # RFM 산점도
    fig_scatter = px.scatter(
        customer_rfm,
        x='Recency',
        y='Monetary',
        size='Frequency',
        color='Monetary',
        color_continuous_scale='Viridis',
        title='RFM 산점도 (버블 크기 = 구매 빈도)',
        labels={'Recency': '최근성 (일)', 'Monetary': '구매액 (₩)', 'Frequency': '구매 빈도'}
    )
    fig_scatter.update_layout(height=500)
    st.plotly_chart(fig_scatter, use_container_width=True)

# 탭 3: 고객 상세
with tab3:
    st.subheader("고객 상세 정보")

    # 필터
    col1, col2, col3 = st.columns(3)

    with col1:
        segment_filter = st.multiselect(
            "세그먼트 필터",
            customer_data['customer_segment'].unique(),
            default=customer_data['customer_segment'].unique()
        )

    with col2:
        min_purchase = st.number_input("최소 구매액 (₩)", value=0, step=10000)

    with col3:
        max_purchase = st.number_input("최대 구매액 (₩)", value=int(customer_data['total_purchase'].max()), step=10000)

    # 데이터 필터링
    filtered_customers = customer_data[
        (customer_data['customer_segment'].isin(segment_filter)) &
        (customer_data['total_purchase'] >= min_purchase) &
        (customer_data['total_purchase'] <= max_purchase)
    ].copy()

    filtered_customers = filtered_customers.sort_values('total_purchase', ascending=False)

    # 통계
    st.metric("필터된 고객 수", f"{len(filtered_customers)}명")

    # 고객 테이블
    st.subheader("고객 목록")

    display_table = filtered_customers[[
        'customer_id',
        'customer_segment',
        'total_purchase',
        'purchase_frequency',
        'last_purchase_days',
        'join_date'
    ]].copy()

    display_table.columns = ['고객ID', '세그먼트', '총구매액(₩)', '구매횟수', '최근구매(일전)', '가입일']
    display_table['총구매액(₩)'] = display_table['총구매액(₩)'].apply(lambda x: f"₩{x:,.0f}")

    st.dataframe(display_table, use_container_width=True, hide_index=True)

    # 고객 분석 요약
    st.subheader("고객 분석 요약")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "평균 구매액",
            f"₩{filtered_customers['total_purchase'].mean():,.0f}"
        )

    with col2:
        st.metric(
            "중간값 구매액",
            f"₩{filtered_customers['total_purchase'].median():,.0f}"
        )

    with col3:
        st.metric(
            "최고 구매액",
            f"₩{filtered_customers['total_purchase'].max():,.0f}"
        )

    with col4:
        days_since_purchase = filtered_customers['last_purchase_days'].mean()
        st.metric(
            "평균 마지막 구매",
            f"{days_since_purchase:.0f}일 전"
        )
