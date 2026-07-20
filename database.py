# database.py

import pandas as pd
import numpy as np
from models import COLUMN_CANDIDATES


def find_column(df, candidates):
    for col in candidates:
        if col in df.columns:
            return col
    return None


def load_and_validate(files):

    dataframes = []

    # 파일 여러 개 처리
    for file in files:

        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(
                file,
                engine="openpyxl"
            )

        rename_map = {}

        # 컬럼 자동 매칭
        for key, candidates in COLUMN_CANDIDATES.items():

            found = find_column(
                df,
                candidates
            )

            if found:
                rename_map[found] = key


        df = df.rename(
            columns=rename_map
        )


        # 없는 컬럼 생성
        default_columns = {
            "campaign": "",
            "adgroup": "",
            "creative": "",
            "cost": 0,
            "impression": 0,
            "click": 0,
            "purchase": 0,
            "revenue": 0,
            "atc": 0,
            "placement": "",
            "target": ""
        }


        for col, default in default_columns.items():

            if col not in df.columns:
                df[col] = default



        # 숫자 변환
        numeric_columns = [
            "cost",
            "impression",
            "click",
            "purchase",
            "revenue",
            "atc"
        ]


        for col in numeric_columns:

            df[col] = (
                df[col]
                .astype(str)
                .str.replace(
                    ",",
                    "",
                    regex=False
                )
            )

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            ).fillna(0)



        dataframes.append(df)



    # 여러 파일 합치기
    df = pd.concat(
        dataframes,
        ignore_index=True
    )


    # 동일 소재/캠페인 데이터 합산
    group_columns = [
        "campaign",
        "adgroup",
        "creative",
        "placement",
        "target"
    ]


    df = (
        df
        .groupby(
            group_columns,
            dropna=False,
            as_index=False
        )
        .agg(
            {
                "cost": "sum",
                "impression": "sum",
                "click": "sum",
                "purchase": "sum",
                "revenue": "sum",
                "atc": "sum"
            }
        )
    )



    # 성과 지표 자동 계산

    df["CTR"] = np.where(
        df["impression"] > 0,
        df["click"]
        /
        df["impression"]
        *
        100,
        0
    )


    df["CVR"] = np.where(
        df["click"] > 0,
        df["purchase"]
        /
        df["click"]
        *
        100,
        0
    )


    df["CPA"] = np.where(
        df["purchase"] > 0,
        df["cost"]
        /
        df["purchase"],
        0
    )


    df["ROAS"] = np.where(
        df["cost"] > 0,
        df["revenue"]
        /
        df["cost"]
        *
        100,
        0
    )



    # AI 전달용 컬럼명 변경
    df = df.rename(
        columns={
            "campaign": "캠페인명",
            "adgroup": "광고그룹명",
            "creative": "소재명",
            "cost": "비용",
            "impression": "노출",
            "click": "클릭",
            "purchase": "구매",
            "revenue": "매출",
            "atc": "장바구니",
            "CTR": "CTR(%)",
            "CVR": "CVR(%)",
            "CPA": "CPA",
            "ROAS": "ROAS(%)"
        }
    )


    # 비용 높은 순 정렬
    df = df.sort_values(
        by="비용",
        ascending=False
    )


    # 엑셀처럼 1부터 표시
    df.index = range(
        1,
        len(df)+1
    )


    return df