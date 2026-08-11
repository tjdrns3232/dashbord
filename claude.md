# 마케팅 데이터 분석 & Streamlit 대시보드

## 프로젝트 개요
Python 기반의 마케팅 데이터 분석 및 Streamlit 대시보드 개발 프로젝트. 판매 데이터, 고객 행동, 캠페인 성과 등을 분석하고 시각화합니다.

## 프로젝트 구조
```
.
├── venv/                      # Python 가상환경
├── data/                       # 데이터 파일 (CSV, Excel 등)
│   ├── raw/                   # 원본 데이터
│   └── processed/             # 전처리된 데이터
├── src/                        # 소스 코드
│   ├── analysis.py            # 데이터 분석 로직
│   ├── data_loader.py         # 데이터 로드 및 전처리
│   ├── metrics.py             # 마케팅 지표 계산
│   └── utils.py               # 유틸리티 함수
├── dashboard/                  # Streamlit 대시보드
│   ├── app.py                 # 메인 대시보드
│   ├── pages/                 # 멀티 페이지
│   │   ├── sales_analysis.py
│   │   ├── customer_insights.py
│   │   └── campaign_performance.py
│   └── assets/                # 이미지, 로고 등
├── requirements.txt           # 패키지 의존성
└── README.md                  # 프로젝트 문서
```

## 설치 및 실행

### 1. 가상환경 활성화
```powershell
.\venv\Scripts\Activate.ps1
```

### 2. 패키지 설치
```bash
pip install -r requirements.txt
```

### 3. Streamlit 대시보드 실행
```bash
streamlit run dashboard/app.py
```

## 데이터 분석 영역

### 핵심 분석 항목
- **판매 분석**: 총 매출, 판매량 추이, 상품별 판매 현황
- **고객 분석**: 고객 세그먼트, RFM 분석, 고객 획득 비용(CAC)
- **캠페인 성과**: 캠페인별 ROI, 전환율, 클릭 시퀀스
- **마케팅 메트릭**: KPI 대시보드, 성과 벤치마크

### 주요 시각화
- 시계열 차트 (매출, 판매량 추이)
- 카테고리별 비교 (막대, 파이 차트)
- 히트맵 (요일별, 월별 성과)
- 산점도 (고객 분석)
- KPI 카드 (주요 지표 요약)

## 사용 라이브러리

| 라이브러리 | 용도 |
|-----------|------|
| **pandas** | 데이터 전처리 및 분석 |
| **numpy** | 수치 계산 |
| **streamlit** | 웹 대시보드 프레임워크 |
| **plotly** | 인터랙티브 차트 |
| **altair** | 선언형 시각화 |
| **scikit-learn** | 기계학습 및 분석 |
| **matplotlib/seaborn** | 통계 시각화 |

## 개발 가이드

### 데이터 로드
- `data_loader.py`에서 CSV/Excel 파일을 pandas DataFrame으로 로드
- 날짜, 숫자형 데이터 타입 변환 처리

### 분석 로직
- `analysis.py`에 분석 함수 작성 (예: RFM 분석, 판매 추이 계산)
- `metrics.py`에 마케팅 지표 계산 함수 작성

### 대시보드 구성
- Streamlit의 `st.title()`, `st.metric()`, `st.plotly_chart()` 사용
- 사이드바 필터로 대화형 분석 가능
- `@st.cache_data` 데코레이터로 성능 최적화

## 성능 최적화

- 큰 데이터셋은 필요한 열만 로드
- 계산 결과를 캐싱하여 재실행 방지
- 대시보드 로드 속도 개선을 위해 데이터 인덱싱

## 다음 단계

1. [ ] 데이터 수집 및 `data/raw/` 폴더에 저장
2. [ ] `data_loader.py` 작성 (데이터 전처리)
3. [ ] `analysis.py` 작성 (핵심 분석 함수)
4. [ ] Streamlit 대시보드 페이지 구성
5. [ ] 시각화 및 인터랙티브 필터 추가
6. [ ] 성능 테스트 및 최적화

## 참고사항

- 데이터는 `data/raw/` 폴더에만 저장 (버전 관리 제외)
- 전처리된 데이터는 `data/processed/`에 저장
- 대시보드 개발 중 `streamlit run`으로 실시간 반영됨
