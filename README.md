# 📊 마케팅 성과 대시보드

포켓몬 스토어 마케팅 데이터를 실시간으로 분석하고 시각화하는 Streamlit 기반 대시보드입니다.

## ✨ 주요 기능

### 1. **기간별 성과 분석**
- 📅 전체/최근 30일/최근 7일 기간 필터
- 📊 기간별 매출 성장률 실시간 비교
- 💹 전월 대비 성과 비교

### 2. **성과 히트맵**
- 🔥 시간대 × 요일별 판매 히트맵
- 🟢 우수 성과 구간 (초록색)
- 🔴 개선 필요 구간 (빨간색)
- 📈 평균 대비 편차 표시

### 3. **개선 인사이트**
- ⚠️ 개선 필요 구간 자동 분석
- ✅ 우수 사례 벤치마킹
- 🤖 AI 기반 동적 인사이트

### 4. **다양한 분석 페이지**
- **판매 분석**: 일일/시간대/요일별 판매 추이
- **캠페인 성과**: ROI, CTR, 전환율 분석
- **고객 인사이트**: RFM 분석, 세그먼트 분석

### 5. **필터 기능**
- 📅 기간 선택
- 🛍️ 상품별 필터
- 📦 카테고리별 필터

## 🚀 설치 및 실행

### 1. 가상환경 설정
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Mac/Linux
```

### 2. 패키지 설치
```bash
pip install -r requirements.txt
```

### 3. 로컬에서 실행
```bash
streamlit run dashboard/app.py
```

브라우저에서 `http://localhost:8501` 접속

## ☁️ Streamlit Cloud 배포

### 1. Streamlit 계정 생성
https://streamlit.io 에서 무료 계정 생성

### 2. 배포 방법
```bash
# GitHub에 코드 푸시 (이미 완료됨)
git push origin main

# Streamlit Cloud에서 배포
# 1. https://share.streamlit.io 접속
# 2. "New app" 클릭
# 3. GitHub 리포지토리 선택: tjdrns3232/dashbord
# 4. 메인 파일 경로: dashboard/app.py
# 5. Deploy 클릭
```

**배포 완료 후 URL:** `https://share.streamlit.io/tjdrns3232/dashbord/main/dashboard/app.py`

## 📁 프로젝트 구조

```
.
├── dashboard/
│   ├── app.py                    # 메인 대시보드
│   └── pages/
│       ├── 01_sales_analysis.py  # 판매 분석
│       ├── 02_campaign_performance.py  # 캠페인 성과
│       └── 03_customer_insights.py  # 고객 인사이트
├── src/
│   ├── data_loader.py           # 데이터 로드
│   ├── metrics.py               # 분석 메트릭
│   └── generate_sample_data.py  # 샘플 데이터 생성
├── data/
│   ├── raw/                     # 원본 데이터
│   └── processed/               # 전처리 데이터
├── requirements.txt             # 패키지 의존성
├── claude.md                    # 프로젝트 문서
└── README.md                    # 이 파일
```

## 📊 주요 지표

| 지표 | 설명 |
|------|------|
| **총 매출** | 선택한 기간의 총 판매액 |
| **거래건수** | 선택한 기간의 총 거래 건수 |
| **평균거래액** | 거래당 평균 판매액 |
| **ROI** | 마케팅 캠페인 투자 수익률 |
| **CTR** | 클릭율 (Clicks / Impressions) |
| **전환율** | 전환율 (Conversions / Clicks) |
| **RFM** | Recency(최근성), Frequency(빈도), Monetary(금액) |

## 🔧 기술 스택

- **프레임워크**: Streamlit
- **데이터 분석**: pandas, numpy, scikit-learn
- **시각화**: plotly, altair, matplotlib, seaborn
- **언어**: Python 3.8+

## 📈 주요 개선사항 (v2)

✅ 기간 필터를 모든 차트에 통합  
✅ 기간별 성과 비교 (전월 대비)  
✅ 히트맵 색상 정규화 (평균 대비 편차)  
✅ 동적 AI 인사이트 추가  
✅ 상품/카테고리 멀티 필터  
✅ 개선 권고사항 자동 분석  

## 📞 지원

문제가 발생하면 GitHub Issues에 보고해주세요:  
https://github.com/tjdrns3232/dashbord/issues

## 📝 라이선스

MIT License - 자유롭게 사용하세요!

---

**마지막 업데이트**: 2026-08-11  
**제작**: Claude Code  
**상태**: ✅ 운영 중
