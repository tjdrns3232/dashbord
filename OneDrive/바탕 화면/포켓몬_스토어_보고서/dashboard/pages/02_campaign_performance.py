import streamlit as st
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.data_loader import load_campaign_data
from src.metrics import MarketingMetrics
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="캠페인 성과", page_icon="🎯")

st.title("🎯 캠페인 성과 분석")
st.markdown("---")

# 캠페인 데이터 로드
campaign_data = load_campaign_data()

# 탭 구성
tab1, tab2, tab3 = st.tabs(["ROI 분석", "채널 성과", "상세 지표"])

# 탭 1: ROI 분석
with tab1:
    st.subheader("캠페인별 ROI 분석")

    campaign_roi = MarketingMetrics.get_campaign_roi()

    # 통계
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total_budget = campaign_data['budget'].sum()
        st.metric("총 마케팅 예산", f"₩{total_budget:,.0f}")

    with col2:
        total_revenue = campaign_data['revenue'].sum()
        st.metric("캠페인 수익", f"₩{total_revenue:,.0f}")

    with col3:
        roi = ((total_revenue - total_budget) / total_budget * 100)
        st.metric("평균 ROI", f"{roi:.1f}%")

    with col4:
        payback = total_revenue / total_budget
        st.metric("회수배수", f"{payback:.2f}x")

    # ROI 차트
    fig_roi = px.bar(
        campaign_roi,
        x='campaign_name',
        y='roi',
        color='roi',
        color_continuous_scale='RdYlGn',
        color_continuous_midpoint=0,
        title="캠페인별 ROI"
    )
    fig_roi.update_layout(height=400, yaxis_title="ROI (%)")
    st.plotly_chart(fig_roi, use_container_width=True)

    # 예산 vs 수익 비교
    col1, col2 = st.columns(2)

    with col1:
        fig_budget = go.Figure(data=[
            go.Bar(name='예산', x=campaign_roi['campaign_name'], y=campaign_roi['budget']),
            go.Bar(name='수익', x=campaign_roi['campaign_name'], y=campaign_roi['revenue'])
        ])
        fig_budget.update_layout(barmode='group', height=400, title="예산 vs 수익")
        st.plotly_chart(fig_budget, use_container_width=True)

    with col2:
        fig_profit = px.bar(
            campaign_roi,
            x='campaign_name',
            y=campaign_roi['revenue'] - campaign_roi['budget'],
            title="캠페인별 순이익",
            labels={'y': '순이익 (₩)'}
        )
        fig_profit.update_layout(height=400)
        st.plotly_chart(fig_profit, use_container_width=True)

# 탭 2: 채널 성과
with tab2:
    st.subheader("채널별 성과 분석")

    channel_perf = MarketingMetrics.get_channel_performance()

    # 채널별 메트릭 계산
    channel_perf_calc = campaign_data.copy()
    channel_perf_calc['cpc'] = channel_perf_calc['budget'] / channel_perf_calc['clicks']  # 클릭당 비용
    channel_perf_calc['cpa'] = channel_perf_calc['budget'] / channel_perf_calc['conversions']  # 전환당 비용
    channel_perf_calc['rpc'] = channel_perf_calc['revenue'] / channel_perf_calc['clicks']  # 클릭당 수익

    # 채널별 매출
    fig_channel_revenue = px.pie(
        channel_perf,
        values='revenue',
        names='channel',
        title="채널별 매출 비중"
    )
    st.plotly_chart(fig_channel_revenue, use_container_width=True)

    # 채널별 지표 비교
    col1, col2 = st.columns(2)

    with col1:
        fig_ctr = px.bar(
            channel_perf_calc,
            x='channel',
            y=channel_perf_calc['clicks'] / channel_perf_calc['impressions'] * 100,
            title="채널별 클릭율 (CTR)",
            labels={'y': 'CTR (%)'}
        )
        fig_ctr.update_layout(height=350, showlegend=False)
        st.plotly_chart(fig_ctr, use_container_width=True)

    with col2:
        fig_cvr = px.bar(
            channel_perf_calc,
            x='channel',
            y=channel_perf_calc['conversions'] / channel_perf_calc['clicks'] * 100,
            title="채널별 전환율",
            labels={'y': '전환율 (%)'},
            color_discrete_sequence=['#2ca02c']
        )
        fig_cvr.update_layout(height=350, showlegend=False)
        st.plotly_chart(fig_cvr, use_container_width=True)

    # 효율성 지표
    st.subheader("채널별 효율성 지표")

    efficiency_table = pd.DataFrame({
        '채널': channel_perf_calc['channel'],
        '노출수': channel_perf_calc['impressions'].astype(int),
        '클릭수': channel_perf_calc['clicks'].astype(int),
        '전환수': channel_perf_calc['conversions'].astype(int),
        'CTR': (channel_perf_calc['clicks'] / channel_perf_calc['impressions'] * 100).round(2),
        '전환율': (channel_perf_calc['conversions'] / channel_perf_calc['clicks'] * 100).round(2),
        'CPC': channel_perf_calc['cpc'].round(0),
        'CPA': channel_perf_calc['cpa'].round(0),
    })

    st.dataframe(efficiency_table, use_container_width=True, hide_index=True)

# 탭 3: 상세 지표
with tab3:
    st.subheader("캠페인별 상세 지표")

    # 캠페인 선택
    selected_campaign = st.selectbox(
        "캠페인 선택",
        campaign_data['campaign_name'].unique()
    )

    # 선택된 캠페인 데이터
    campaign_detail = campaign_data[campaign_data['campaign_name'] == selected_campaign].iloc[0]

    # 주요 지표
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("예산", f"₩{campaign_detail['budget']:,.0f}")
    with col2:
        st.metric("수익", f"₩{campaign_detail['revenue']:,.0f}")
    with col3:
        roi = ((campaign_detail['revenue'] - campaign_detail['budget']) / campaign_detail['budget'] * 100)
        st.metric("ROI", f"{roi:.1f}%")
    with col4:
        cpa = campaign_detail['budget'] / campaign_detail['conversions']
        st.metric("CPA", f"₩{cpa:,.0f}")

    # 상세 통계
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("노출수", f"{campaign_detail['impressions']:,}")
    with col2:
        ctr = (campaign_detail['clicks'] / campaign_detail['impressions'] * 100)
        st.metric("클릭율 (CTR)", f"{ctr:.2f}%")
    with col3:
        cvr = (campaign_detail['conversions'] / campaign_detail['clicks'] * 100)
        st.metric("전환율", f"{cvr:.2f}%")

    # 비용 효율성
    st.subheader("비용 효율성 분석")

    efficiency_metrics = {
        'CPC (클릭당 비용)': campaign_detail['budget'] / campaign_detail['clicks'],
        'CPM (노출당 비용)': (campaign_detail['budget'] / campaign_detail['impressions']) * 1000,
        'ROAS (광고 지출 수익)': campaign_detail['revenue'] / campaign_detail['budget'],
    }

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("CPC", f"₩{efficiency_metrics['CPC (클릭당 비용)']:.0f}")
    with col2:
        st.metric("CPM", f"₩{efficiency_metrics['CPM (노출당 비용)']:.2f}")
    with col3:
        st.metric("ROAS", f"{efficiency_metrics['ROAS (광고 지출 수익)']:.2f}x")

    # 전체 캠페인 비교
    st.subheader("모든 캠페인 비교")

    comparison_table = campaign_data[[
        'campaign_name', 'channel', 'budget', 'revenue',
        'impressions', 'clicks', 'conversions'
    ]].copy()

    comparison_table['ROI'] = (
        (comparison_table['revenue'] - comparison_table['budget']) /
        comparison_table['budget'] * 100
    ).round(2)

    comparison_table['CTR'] = (
        comparison_table['clicks'] / comparison_table['impressions'] * 100
    ).round(2)

    comparison_table['CVR'] = (
        comparison_table['conversions'] / comparison_table['clicks'] * 100
    ).round(2)

    st.dataframe(comparison_table, use_container_width=True, hide_index=True)
