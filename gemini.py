import google.generativeai as genai
import streamlit as st
from prompts import ANALYSIS_PROMPT

def get_ai_insight(df):
    # Streamlit Cloud의 설정 메뉴에서 등록한 키를 가져옵니다.
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    model = genai.GenerativeModel('gemini-1.5-flash') # gemini-pro보다 더 빠르고 효율적입니다
    
    # 데이터 요약 (로딩 방지를 위해 텍스트로 변환)
    data_summary = df.to_string()
    
    try:
        response = model.generate_content(f"{ANALYSIS_PROMPT}\n데이터 요약: {data_summary}")
        return response.text
    except Exception as e:
        return f"분석 중 오류 발생: {e}"