# main.py

import streamlit as st
from database import load_and_validate
from gemini import get_ai_insight


st.set_page_config(
    page_title="Performance Report",
    layout="wide"
)


# 제목 크기 조정
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
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown(
    '<div class="small-title">📊 마케팅 성과 분석 리포트</div>',
    unsafe_allow_html=True
)


uploaded_files = st.file_uploader(
    "데이터 파일을 업로드하세요 (Meta / GFA / 애드부스트 가능)",
    type=["xlsx", "csv"],
    accept_multiple_files=True
)


if uploaded_files:

    try:

        df = load_and_validate(uploaded_files)

        st.success(
            f"데이터 분석 완료 ({len(df)}개 소재)"
        )


        # 원본 데이터 접기/펼치기
        with st.expander(
            "📄 업로드 데이터 확인",
            expanded=False
        ):

            st.dataframe(
                df,
                use_container_width=True,
                height=500
            )


        st.divider()


        if st.button(
            "📊 성과 보고서 생성",
            type="primary",
            use_container_width=True
        ):

            with st.spinner(
                "성과 데이터를 분석하고 있습니다..."
            ):

                insight = get_ai_insight(df)


            st.success(
                "보고서 생성 완료"
            )


            # 결과 접기
            with st.expander(
                "📋 생성된 보고서",
                expanded=True
            ):

                st.markdown(
                    insight
                )


            st.download_button(
                label="💾 보고서 저장",
                data=insight,
                file_name="performance_report.txt",
                mime="text/plain"
            )


    except Exception as e:

        st.error(
            f"데이터 처리 중 오류 발생: {e}"
        )