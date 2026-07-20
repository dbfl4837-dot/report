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
            df = pd.read_excel(file, engine="openpyxl")

        rename = {}

        for key, candidates in COLUMN_CANDIDATES.items():
            col = find_column(df, candidates)
            if col:
                rename[col] = key

        df = df.rename(columns=rename)

        # 필수 컬럼 없으면 생성
        base_cols = [
            "campaign",
            "adgroup",
            "creative",
            "cost",
            "impression",
            "click",
            "purchase",
            "revenue",
            "atc",
            "placement",
            "target",
        ]

        for c in base_cols:
            if c not in df.columns:
                if c in ["campaign","adgroup","creative","placement","target"]:
                    df[c] = ""
                else:
                    df[c] = 0

        # 숫자형 변환
        num_cols = [
            "cost",
            "impression",
            "click",
            "purchase",
            "revenue",
            "atc"
        ]

        for c in num_cols:
            df[c] = (
                df[c]
                .astype(str)
                .str.replace(",", "", regex=False)
                .replace("", 0)
            )

            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

        dfs.append(df)

    ##################################################
    ## 여러 파일 합치기 (메타 + 애드부스트 자동 합산)
    ##################################################

    df = pd.concat(dfs, ignore_index=True)

    group_cols = [
        "campaign",
        "adgroup",
        "creative",
        "placement",
        "target"
    ]

    df = (
        df.groupby(group_cols, dropna=False, as_index=False)
        .agg({
            "cost":"sum",
            "impression":"sum",
            "click":"sum",
            "purchase":"sum",
            "revenue":"sum",
            "atc":"sum"
        })
    )

    #########################################
    # 계산
    #########################################

    df["CTR"] = np.where(
        df["impression"] > 0,
        df["click"] / df["impression"] * 100,
        0
    )

    df["CVR"] = np.where(
        df["click"] > 0,
        df["purchase"] / df["click"] * 100,
        0
    )

    df["CPA"] = np.where(
        df["purchase"] > 0,
        df["cost"] / df["purchase"],
        0
    )

    df["ROAS"] = np.where(
        df["cost"] > 0,
        df["revenue"] / df["cost"] * 100,
        0
    )

    #########################################
    # 보기 좋게
    #########################################

    df = df.sort_values("cost", ascending=False)

    df = df.reset_index(drop=True)

    df.index = df.index + 1

    return df