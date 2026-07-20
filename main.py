import streamlit as st
from database import load_and_validate

st.set_page_config(page_title="마케팅 보고서 도우미", layout="wide")
st.title("🚀 시니어 마케터의 성과 분석기")

uploaded_file = st.file_uploader("엑셀 업로드", type=['xlsx'])

if uploaded_file:
    try:
        df = load_and_validate(uploaded_file)
        st.success("데이터 로드 완료!")
        
        # 분석 로직 (옵션 1, 3 반영)
        # 1. 데이터 없음 체크(옵션 1)
        # 2. 성장률 계산 등(옵션 3)
        
        # 버튼을 누르면 gemini.py 호출
        if st.button("보고서 생성"):
            report = "여기에 분석 결과가 자동으로 들어갑니다." # 실제론 gemini.py 호출
            st.text_area("최종 결과", report, height=500)
    except Exception as e:
        st.error(f"오류: {e}")