import streamlit as st
from database import load_and_validate
from gemini import get_ai_insight

st.set_page_config(page_title="Performance Report", layout="wide")
st.title("📊 마케팅 성과 분석 리포트") # 제목 수정

uploaded_file = st.file_uploader("데이터 파일을 업로드하세요 (xlsx, csv)", type=['xlsx', 'csv'])

if uploaded_file is not None:
    try:
        # 데이터 로드
        df = load_and_validate(uploaded_file)
        st.success("데이터 분석 완료!")
        
        # 데이터 미리보기 (로딩 확인용)
        st.dataframe(df.head(5))
        
        if st.button("보고서 생성"):
            with st.spinner('분석 중...'):
                insight = get_ai_insight(df)
                st.text_area("생성된 보고서", insight, height=500)
                st.download_button("보고서 저장", insight, "report.txt")
                
    except Exception as e:
        st.error(f"데이터 처리 중 오류 발생: {e}")