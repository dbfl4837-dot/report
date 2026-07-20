import pandas as pd
import numpy as np
from models import COLUMN_CANDIDATES


def find_column(df, candidates):
    for c in candidates:
        if c in df.columns:
            return c
    return None


def load_and_validate(files):

    dfs = []


    for file in files:

        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)


        rename = {}


        for key, candidates in COLUMN_CANDIDATES.items():

            col = find_column(
                df,
                candidates
            )

            if col:
                rename[col] = key


        df = df.rename(columns=rename)


        default = {

            "campaign":"",
            "adgroup":"",
            "creative":"",
            "cost":0,
            "impression":0,
            "click":0,
            "purchase":0,
            "revenue":0,
            "atc":0

        }


        for col,val in default.items():

            if col not in df.columns:
                df[col] = val



        number_cols = [
            "cost",
            "impression",
            "click",
            "purchase",
            "revenue",
            "atc"
        ]


        for col in number_cols:

            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",","")
            )

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            ).fillna(0)



        dfs.append(df)



    df = pd.concat(
        dfs,
        ignore_index=True
    )



    # 소재 기준 데이터 통합

    df = (
        df
        .groupby(
            [
                "campaign",
                "adgroup",
                "creative"
            ],
            as_index=False
        )
        .agg({

            "cost":"sum",
            "impression":"sum",
            "click":"sum",
            "purchase":"sum",
            "revenue":"sum",
            "atc":"sum"

        })
    )



    # 성과 계산

    df["CTR"] = np.where(
        df["impression"]>0,
        df["click"]/df["impression"]*100,
        0
    )


    df["CVR"] = np.where(
        df["click"]>0,
        df["purchase"]/df["click"]*100,
        0
    )


    df["CPA"] = np.where(
        df["purchase"]>0,
        df["cost"]/df["purchase"],
        0
    )


    df["ROAS"] = np.where(
        df["cost"]>0,
        df["revenue"]/df["cost"]*100,
        0
    )



    # AI 전달용 컬럼

    df = df.rename(
        columns={

            "campaign":"캠페인명",
            "adgroup":"광고그룹명",
            "creative":"소재명",
            "cost":"비용",
            "impression":"노출",
            "click":"클릭",
            "purchase":"구매",
            "revenue":"매출",
            "atc":"장바구니",
            "CTR":"CTR",
            "CVR":"CVR",
            "CPA":"CPA",
            "ROAS":"ROAS"

        }
    )



    # 정렬

    df = df.sort_values(
        "비용",
        ascending=False
    )



    # 표시용 포맷

    display_df = df.copy()


    for col in [
        "비용",
        "매출",
        "CPA"
    ]:

        display_df[col] = (
            display_df[col]
            .round()
            .astype(int)
            .map("{:,}".format)
        )



    for col in [
        "CTR",
        "CVR",
        "ROAS"
    ]:

        display_df[col] = (
            display_df[col]
            .round(2)
            .astype(str)
            +"%"
        )


    display_df.index = range(
        1,
        len(display_df)+1
    )


    return display_df