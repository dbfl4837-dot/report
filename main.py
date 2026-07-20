import streamlit as st
from database import load_and_validate
from gemini import get_ai_insight

st.set_page_config(page_title="시니어 마케터의 성과 분석기", layout="wide")
st.title("🚀 시니어 마케터의 성과 분석기")

uploaded_file = st.file_uploader("엑셀/CSV 업로드", type=['xlsx', 'csv'])

if uploaded_file:
    try:
        df = load_and_validate(uploaded_file)
        st.success("데이터 로드 완료!")
        
        if st.button("보고서 생성"):
            insight = get_ai_insight(df)
            
            # 보고서 출력 (7단계)
            report = f"""
# 주간 운영 보고서
## 1. 주간 성과 요약
{insight}

## 2. 캠페인 분석
(캠페인별 ROAS 데이터 요약 예정)

## 3. 소재 분석
(CTR, CVR, CPA, ROAS 데이터 요약 예정)

## 4. 타겟 분석
(타겟별 효율 데이터 요약 예정)

## 5. 지면 분석
(지면별 성과 데이터 요약 예정)

## 6. AI 인사이트
데이터 근거 기반 분석 내용이 들어갑니다.

## 7. 운영 방향
데이터를 바탕으로 한 다음 주 액션 플랜을 제안합니다.
            """
            st.text_area("생성된 보고서", report, height=600)
            st.download_button("보고서 다운로드 (txt)", report, "weekly_report.txt")
            
    except Exception as e:
        st.error(f"오류: {e}")