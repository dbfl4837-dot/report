import google.generativeai as genai
import streamlit as st
from prompts import ANALYSIS_PROMPT

def get_ai_insight(df):

    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-3.1-flash-lite")

    # 데이터를 마크다운 표 형태로 변환
    data_text = df.to_markdown(index=False)

    prompt = f"""
{ANALYSIS_PROMPT}

=========================
광고 데이터
=========================

{data_text}

=========================
중요 규칙
=========================

1.
데이터에 없는 내용은 절대 작성하지 않는다.

2.
소재명은 반드시 데이터 그대로 사용한다.

3.
후기형, 차냄새, CCTV 등의 소재 내용은 절대 추측하지 않는다.

4.
성과 좋은 소재는
ROAS → 구매 → CPA → CVR → CTR → 비용
순으로 판단한다.

5.
성과가 좋은 소재 TOP3
성과가 낮은 소재 TOP3
를 반드시 작성한다.

6.
타겟 분석은 데이터의 타겟명 그대로 작성한다.

7.
지면 분석은 데이터 그대로 작성한다.

8.
광고주 보고용 문구는
실무자가 실제 보내는 말투로 작성한다.

9.
마크다운 표를 사용하지 않는다.

10.
이모지를 사용하지 않는다.
"""

    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return str(e)