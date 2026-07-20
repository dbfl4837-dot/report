# gemini.py

import google.generativeai as genai
import streamlit as st
from prompts import ANALYSIS_PROMPT


def get_ai_insight(df):

    try:
        api_key = st.secrets["GEMINI_API_KEY"]

        genai.configure(api_key=api_key)

        model = genai.GenerativeModel(
            "gemini-3.1-flash-lite"
        )

        # 데이터 전달용
        # index 제거 (0,1,2 표시 방지)
        data_text = df.to_markdown(
            index=False
        )

        prompt = f"""
{ANALYSIS_PROMPT}

아래 광고 데이터를 기반으로 분석해주세요.

[광고 데이터]
{data_text}

반드시 데이터에 존재하는 값만 사용하세요.
소재명, 캠페인명, 광고그룹명은 원본 그대로 유지하세요.
"""

        response = model.generate_content(
            prompt
        )

        return response.text

    except Exception as e:
        return f"AI 분석 오류: {str(e)}"