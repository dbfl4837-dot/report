import google.generativeai as genai
import streamlit as st
from prompts import ANALYSIS_PROMPT

def get_ai_insight(df):
    # Streamlit Secrets에서 API 키 가져오기
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    # 어제 정상 작동했던 3.1 flash lite 모델명 그대로 적용
    model = genai.GenerativeModel('gemini-3.1-flash-lite')
    
    # 데이터를 AI가 읽을 수 있도록 텍스트로 변환
    data_summary = df.to_string()
    
    # 분석 요청
    try:
        response = model.generate_content(f"{ANALYSIS_PROMPT}\n데이터 요약:\n{data_summary}")
        return response.text
    except Exception as e:
        return f"분석 중 오류 발생: {e}"