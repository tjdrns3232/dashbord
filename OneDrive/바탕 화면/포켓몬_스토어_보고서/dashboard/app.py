import streamlit as st
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.metrics import MarketingMetrics
from src.data_loader import load_daily_sales, load_campaign_data, load_hourly_sales, load_product_sales
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

st.set_page_config(
    page_title="마케팅 대시보드",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 스타일 설정
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    .improvement-alert {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 10px;
        border-radius: 4px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# 페이지 타이틀
st.title("📊 마케팅 성과 대시보드")
st.markdown("---")

# 데이터 로드
daily_sales = load_daily_sales()
start_date = daily_sales['date'].min()
end_date = daily_sales['date'].max()

# 사이드바 필터
st.sidebar.title("🎯 필터 설정")

date_range = st.sidebar.radio(
    "📅 기간 선택",
    ["전체", "최근 30일", "최근 7일"]
)

# 상품 필터
product_sales = load_product_sales()
all_products = product_sales['product'].unique().tolist()
selected_products = st.sidebar.multiselect(
    "🛍️ 상품 선택",
    all_products,
    default=all_products
)

# 카테고리 필터
all_categories = product_sales['category'].unique().tolist()
selected_categories = st.sidebar.multiselect(
    "📦 카테고리 선택",
    all_categories,
    default=all_categories
)

# 기간에 따른 필터링
if date_range == "최근 7일":
    filter_start_date = end_date - pd.Timedelta(days=7)
    comparison_start = end_date - pd.Timedelta(days=14)
    comparison_end = end_date - pd.Timedelta(days=7)
elif date_range == "최근 30일":
    filter_start_date = end_date - pd.Timedelta(days=30)
    comparison_start = end_date - pd.Timedelta(days=60)
    comparison_end = end_date - pd.Timedelta(days=30)
else:  # 전체
    filter_start_date = start_date
    comparison_start = start_date
    comparison_end = start_date

filtered_daily_sales = daily_sales[daily_sales['date'] >= filter_start_date]
comparison_sales = daily_sales[(daily_sales['date'] >= comparison_start) & (daily_sales['date'] < comparison_end)]

# 메트릭 계산
def calculate_metrics(data):
    if len(data) == 0:
        return {
            'total_revenue': 0,
            'total_transactions': 0,
            'total_customers': 0,
            'avg_transaction': 0,
            'daily_growth': 0,
        }
    total_revenue = data['sales'].sum()
    total_transactions = data['transactions'].sum()
    total_customers = data['customers'].sum()
    avg_transaction = total_revenue / total_transactions if total_transactions > 0 else 0

    if len(data) < 2:
        daily_growth = 0
    else:
        recent = data['sales'].iloc[-7:].mean() if len(data) >= 7 else data['sales'].mean()
        previous = data['sales'].iloc[-14:-7].mean() if len(data) >= 14 else data['sales'].mean()
        daily_growth = ((recent - previous) / previous * 100) if previous > 0 else 0

    return {
        'total_revenue': total_revenue,
        'total_transactions': total_transactions,
        'total_customers': total_customers,
        'avg_transaction': avg_transaction,
        'daily_growth': daily_growth,
    }

metrics = calculate_metrics(filtered_daily_sales)
comparison_metrics = calculate_metrics(comparison_sales)

# 성장률 계산
revenue_growth = ((metrics['total_revenue'] - comparison_metrics['total_revenue']) / comparison_metrics['total_revenue'] * 100) if comparison_metrics['total_revenue'] > 0 else 0

# KPI 지표
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "총 매출",
        f"₩{metrics['total_revenue']:,.0f}",
        delta=f"{revenue_growth:.1f}% vs 전기간" if date_range != "전체" else None
    )

with col2:
    st.metric(
        "총 거래건수",
        f"{metrics['total_transactions']:,}",
        delta=f"{metrics['total_transactions'] - comparison_metrics['total_transactions']:+,}" if date_range != "전체" else None
    )

with col3:
    st.metric(
        "총 고객수",
        f"{metrics['total_customers']:,}",
        delta="누적"
    )

with col4:
    st.metric(
        "평균거래액",
        f"₩{metrics['avg_transaction']:,.0f}",
        delta="거래당"
    )

with col5:
    campaign_data = load_campaign_data()
    total_roi = ((campaign_data['revenue'].sum() - campaign_data['budget'].sum()) / campaign_data['budget'].sum() * 100)
    st.metric(
        "전체 ROI",
        f"{total_roi:.1f}%",
        delta="캠페인 기준"
    )

st.markdown("---")

# 일일 판매 추이
st.subheader("📈 일일 판매 추이")

fig_daily = go.Figure()
fig_daily.add_trace(go.Scatter(
    x=filtered_daily_sales['date'],
    y=filtered_daily_sales['sales'],
    mode='lines',
    name='판매액',
    line=dict(color='#1f77b4', width=2),
    fill='tozeroy',
    fillcolor='rgba(31, 119, 180, 0.1)'
))

fig_daily.update_layout(
    title="",
    xaxis_title="날짜",
    yaxis_title="판매액 (₩)",
    height=400,
    hovermode='x unified',
    template='plotly_white'
)
st.plotly_chart(fig_daily, use_container_width=True)

# 두 개의 컬럼
col_left, col_right = st.columns(2)

# 캠페인별 ROI
with col_left:
    st.subheader("🎯 캠페인별 ROI")
    campaign_roi = MarketingMetrics.get_campaign_roi()

    fig_roi = px.bar(
        campaign_roi,
        x='campaign_name',
        y='roi',
        color='roi',
        color_continuous_scale='RdYlGn',
        title=""
    )
    fig_roi.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_roi, use_container_width=True)

# 채널별 성과
with col_right:
    st.subheader("💰 채널별 수익")
    channel_perf = MarketingMetrics.get_channel_performance()

    fig_channel = px.pie(
        channel_perf,
        values='revenue',
        names='channel',
        title=""
    )
    fig_channel.update_layout(height=400)
    st.plotly_chart(fig_channel, use_container_width=True)

# 캠페인 상세 정보
st.markdown("---")
st.subheader("📋 캠페인 성과 상세")

col1, col2 = st.columns(2)

with col1:
    campaign_ctr = MarketingMetrics.get_campaign_ctr()
    st.dataframe(campaign_ctr, use_container_width=True, hide_index=True)

with col2:
    conversion_rate = MarketingMetrics.get_campaign_conversion_rate()
    st.dataframe(conversion_rate, use_container_width=True, hide_index=True)

# 고객 인사이트
st.markdown("---")
st.subheader("👥 고객 인사이트")

col1, col2, col3 = st.columns(3)

rfm = MarketingMetrics.get_customer_rfm()

with col1:
    st.metric("평균 구매 간격 (일)", f"{rfm['avg_recency']:.0f}일", delta="최근 구매")

with col2:
    st.metric("평균 구매 빈도", f"{rfm['avg_frequency']:.1f}회", delta="누적")

with col3:
    st.metric("평균 구매액", f"₩{rfm['avg_monetary']:,.0f}", delta="고객당")

# 상품별 판매
st.markdown("---")
st.subheader("🛍️ 상위 상품 (매출 기준)")

filtered_products = product_sales[
    (product_sales['product'].isin(selected_products)) &
    (product_sales['category'].isin(selected_categories))
]

top_products = filtered_products.groupby('product').agg({
    'revenue': 'sum',
    'quantity_sold': 'sum'
}).sort_values('revenue', ascending=False).head(10)

fig_products = px.bar(
    top_products.reset_index(),
    x='revenue',
    y='product',
    orientation='h',
    color='revenue',
    color_continuous_scale='Viridis'
)
fig_products.update_layout(height=400, xaxis_title="매출액 (₩)", yaxis_title="")
st.plotly_chart(fig_products, use_container_width=True)

# 성과 히트맵 - 시간대별 × 요일별
st.markdown("---")
st.subheader("🔥 성과 히트맵 - 시간대별 × 요일별 판매")

hourly_sales_data = load_hourly_sales()
heatmap_data = hourly_sales_data.pivot_table(
    index='hour',
    columns='day_of_week',
    values='sales',
    aggfunc='sum'
)

# 요일 순서 정렬
day_order = ['월', '화', '수', '목', '금', '토', '일']
heatmap_data = heatmap_data[[col for col in day_order if col in heatmap_data.columns]]

# 평균값 계산 (기준선)
avg_sales = heatmap_data.values.mean()
std_sales = heatmap_data.values.std()

# 정규화된 색상 스케일 (평균 대비 편차)
normalized_data = (heatmap_data.values - avg_sales) / std_sales if std_sales > 0 else heatmap_data.values

# 히트맵 생성
fig_heatmap = go.Figure(data=go.Heatmap(
    z=heatmap_data.values,
    x=heatmap_data.columns,
    y=heatmap_data.index,
    colorscale=[
        [0, '#d73027'],
        [0.5, '#fee08b'],
        [1, '#1a9850']
    ],
    colorbar=dict(title="판매액 (₩)", thickness=15),
    text=heatmap_data.values.astype(int),
    texttemplate='₩%{text:,}',
    textfont={"size": 10},
    hovertemplate='시간: %{y}시<br>요일: %{x}<br>판매액: ₩%{z:,}<br>기준대비: %{customdata:.1f}σ<extra></extra>',
    customdata=normalized_data
))

fig_heatmap.update_layout(
    height=500,
    xaxis_title="요일",
    yaxis_title="시간대",
    title="",
    font=dict(size=11)
)
st.plotly_chart(fig_heatmap, use_container_width=True)

# 개선 포인트 분석
col1, col2 = st.columns([2, 1])

with col1:
    st.info("""
    📊 **히트맵 해석 방법:**
    - 🟢 초록색: 판매가 잘되는 구간 (평균 이상)
    - 🟡 노란색: 보통 판매 구간
    - 🔴 빨간색: 판매가 낮은 구간 ⚠️ 개선 필요
    """)

with col2:
    low_performance = (heatmap_data.values < avg_sales - std_sales).sum()
    high_performance = (heatmap_data.values > avg_sales + std_sales).sum()

    st.metric("개선 필요 구간", f"{low_performance}곳")
    st.metric("우수 성과 구간", f"{high_performance}곳")

# 상세 개선 권고사항
st.subheader("💡 개선 권고사항")

flat_heatmap = heatmap_data.stack().reset_index()
flat_heatmap.columns = ['hour', 'day', 'sales']
worst_performers = flat_heatmap.nsmallest(3, 'sales')
best_performers = flat_heatmap.nlargest(3, 'sales')

col1, col2 = st.columns(2)

with col1:
    st.write("**⚠️ 개선이 필요한 구간 (하위 3):**")
    for idx, row in worst_performers.iterrows():
        st.markdown(f"""
        <div class='improvement-alert'>
        📍 <b>{row['day']} {int(row['hour'])}시</b> - ₩{int(row['sales']):,}
        <br>💡 프로모션/광고 강화 필요
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.write("**✅ 우수 성과 구간 (상위 3):**")
    for idx, row in best_performers.iterrows():
        st.success(f"🏆 {row['day']} {int(row['hour'])}시 - ₩{int(row['sales']):,} (우수 사례)")

# 상품별 성과 히트맵
st.markdown("---")
st.subheader("📦 상품별 성과 히트맵")

product_summary = filtered_products.groupby(['product', 'category']).agg({
    'revenue': 'sum',
    'quantity_sold': 'sum'
}).reset_index()

product_summary = product_summary.sort_values('revenue', ascending=False).head(10)

fig_product_heatmap = px.bar(
    product_summary,
    x='product',
    y='revenue',
    color='revenue',
    color_continuous_scale='RdYlGn',
    title="",
    labels={'revenue': '매출액 (₩)', 'product': '상품명'},
    text='revenue',
    hover_data={'quantity_sold': True, 'category': True}
)

fig_product_heatmap.update_traces(texttemplate='₩%{y:,.0f}', textposition='outside')
fig_product_heatmap.update_layout(height=400, showlegend=False)
st.plotly_chart(fig_product_heatmap, use_container_width=True)

# 동적 인사이트
st.markdown("---")
st.subheader("🤖 AI 인사이트")

col1, col2 = st.columns(2)

with col1:
    if revenue_growth > 0:
        st.success(f"📈 **긍정적 신호**: 매출이 {revenue_growth:.1f}% 증가했습니다!")
    else:
        st.error(f"📉 **주의**: 매출이 {abs(revenue_growth):.1f}% 감소했습니다.")

with col2:
    best_product = product_summary.iloc[0] if len(product_summary) > 0 else None
    if best_product is not None:
        st.info(f"🌟 **Best Performer**: '{best_product['product']}'이(가) ₩{int(best_product['revenue']):,}로 최고 실적입니다!")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #999; font-size: 12px;'>마케팅 성과 대시보드 | 실시간 분석 | 기간별 비교 활성화</p>",
    unsafe_allow_html=True
)
