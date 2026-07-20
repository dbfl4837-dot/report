# main.py
import streamlit as st
from database import load_and_validate
from gemini import get_ai_insight

st.set_page_config(page_title="Performance Report", layout="wide")

st.markdown(
    """
    <style>
    .small-title {
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 20px;
    }
    div[data-testid="stExpander"] {
        border-radius: 10px;
    }
    /* AI 리포트 내부 마크다운 헤딩 크기 축소 */
    div[data-testid="stExpander"] h1 { font-size: 20px !important; margin-top: 24px; }
    div[data-testid="stExpander"] h2 { font-size: 18px !important; margin-top: 20px; }
    div[data-testid="stExpander"] h3 { font-size: 16px !important; margin-top: 14px; }
    div[data-testid="stExpander"] h4 { font-size: 15px !important; margin-top: 10px; }
    div[data-testid="stExpander"] p  { font-size: 14px !important; line-height: 1.7; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="small-title">📊 마케팅 성과 분석 리포트</div>', unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "데이터 파일을 업로드하세요 (Meta / GFA / 애드부스트 가능)",
    type=["xlsx", "csv"],
    accept_multiple_files=True,
)

if uploaded_files:
    try:
        df, unmatched_report = load_and_validate(uploaded_files)
        st.success(f"데이터 분석 완료 ({len(df)}개 소재)")

        # 컬럼 매칭 진단 (문제 있을 때만 표시)
        if unmatched_report:
            with st.expander("⚠️ 일부 항목이 자동으로 인식되지 않았어요", expanded=True):
                for fname, info in unmatched_report.items():
                    st.write(f"**{fname}**")
                    st.write(f"- 인식 안 된 항목: {info['missing']}")
                    st.write(f"- 원본 컬럼 목록: {info['raw_columns']}")

        with st.expander("📄 업로드 데이터 확인", expanded=False):
            st.dataframe(df, use_container_width=True, height=500)

        st.divider()

        if st.button("📊 성과 보고서 생성", type="primary", use_container_width=True):
            with st.spinner("성과 데이터를 분석하고 있습니다..."):
                insight = get_ai_insight(df)
            st.success("보고서 생성 완료")

            with st.expander("📋 생성된 보고서", expanded=True):
                st.markdown(insight)

            st.download_button(
                label="💾 보고서 저장",
                data=insight,
                file_name="performance_report.txt",
                mime="text/plain",
            )
    except Exception as e:
        st.error(f"데이터 처리 중 오류 발생: {e}")