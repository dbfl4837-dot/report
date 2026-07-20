import pandas as pd
import streamlit as st
from database import load_and_validate
from gemini import get_ai_insight

st.set_page_config(
    page_title="Performance Report",
    layout="wide"
)

st.markdown("### 📊 마케팅 성과 분석 리포트")

st.info("Meta는 파일 1개, GFA는 일반 데이터 + 애드부스트 데이터 2개를 함께 업로드하세요.")

uploaded_files = st.file_uploader(
    "데이터 파일 업로드 (xlsx, csv)",
    type=["xlsx", "csv"],
    accept_multiple_files=True
)

if uploaded_files:

    try:
        dfs = []

        for file in uploaded_files:
            dfs.append(load_and_validate(file))

        # 여러 파일 하나로 합치기
        df = pd.concat(dfs, ignore_index=True)

        st.success(f"{len(uploaded_files)}개 파일 분석 완료")

        # ===== 엑셀 미리보기 =====
        with st.expander("📄 업로드 데이터 보기", expanded=False):

            preview = df.copy()

            # 1부터 시작하도록 변경
            preview.index = preview.index + 1

            st.dataframe(
                preview,
                use_container_width=True,
                height=600
            )

        # ===== 보고서 생성 =====
        if st.button(
            "📊 보고서 생성",
            use_container_width=True,
            type="primary"
        ):

            with st.spinner("AI가 성과를 분석하고 있습니다..."):

                report = get_ai_insight(df)

                st.markdown("### 생성된 보고서")

                st.text_area(
                    "",
                    report,
                    height=700
                )

                st.download_button(
                    "보고서 다운로드",
                    report,
                    file_name="performance_report.txt"
                )

    except Exception as e:
        st.error(f"데이터 처리 중 오류 발생 : {e}")