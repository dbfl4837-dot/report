import google.generativeai as genai
from prompts import ANALYSIS_PROMPT

# API 키 설정 (본인의 키로 대체)
# genai.configure(api_key="YOUR_API_KEY")

def get_ai_insight(data_summary):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(f"{ANALYSIS_PROMPT}\n데이터 요약: {data_summary}")
    return response.text