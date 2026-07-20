import pandas as pd
import numpy as np
from models import COLUMN_CANDIDATES


def _normalize(s):
    """공백/대소문자/특수문자 차이를 무시하고 비교하기 위한 정규화"""
    return str(s).replace("\ufeff", "").strip().lower().replace(" ", "")


def find_column(df, candidates):
    norm_cols = {_normalize(c): c for c in df.columns}

    # 1) 정규화 후 완전 일치
    for cand in candidates:
        n = _normalize(cand)
        if n in norm_cols:
            return norm_cols[n]

    # 2) 부분 일치 (예: "장바구니 담기 수(웹)" vs "장바구니")
    for cand in candidates:
        n = _normalize(cand)
        if not n:
            continue
        for col_norm, orig in norm_cols.items():
            if n in col_norm or col_norm in n:
                return orig

    return None


def load_and_validate(files):
    dfs = []
    unmatched_report = {}  # {파일명: {"missing": [...], "raw_columns": [...]}}

    for file in files:
        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        rename = {}
        missing_fields = []
        for key, candidates in COLUMN_CANDIDATES.items():
            col = find_column(df, candidates)
            if col:
                rename[col] = key
            else:
                missing_fields.append(key)

        if missing_fields:
            unmatched_report[file.name] = {
                "missing": missing_fields,
                "raw_columns": list(df.columns),
            }

        df = df.rename(columns=rename)

        default = {
            "campaign": "",
            "adgroup": "",
            "creative": "",
            "cost": 0,
            "impression": 0,
            "click": 0,
            "purchase": 0,
            "revenue": 0,
            "atc": 0,
        }
        for col, val in default.items():
            if col not in df.columns:
                df[col] = val

        # PMax처럼 소재(creative) 단위가 없는 리포트 대응:
        # creative가 비어있으면 adgroup(애셋 그룹명 등)으로 대체
        df["creative"] = df["creative"].astype(str).str.strip()
        df.loc[df["creative"].isin(["", "nan", "0"]), "creative"] = df["adgroup"]

        number_cols = [
            "cost",
            "impression",
            "click",
            "purchase",
            "revenue",
            "atc",
        ]
        for col in number_cols:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", "")
                .str.replace("-", "0")  # 매체별로 0을 '-'로 표기하는 경우 대응
                .str.strip()
            )
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        dfs.append(df)

    df = pd.concat(dfs, ignore_index=True)

    # 소재 기준 데이터 통합
    df = (
        df.groupby(
            ["campaign", "adgroup", "creative"],
            as_index=False,
        )
        .agg({
            "cost": "sum",
            "impression": "sum",
            "click": "sum",
            "purchase": "sum",
            "revenue": "sum",
            "atc": "sum",
        })
    )

    # 성과 계산
    df["CTR"] = np.where(
        df["impression"] > 0,
        df["click"] / df["impression"] * 100,
        0,
    )
    df["CVR"] = np.where(
        df["click"] > 0,
        df["purchase"] / df["click"] * 100,
        0,
    )
    df["CPA"] = np.where(
        df["purchase"] > 0,
        df["cost"] / df["purchase"],
        0,
    )
    df["ROAS"] = np.where(
        df["cost"] > 0,
        df["revenue"] / df["cost"] * 100,
        0,
    )

    # AI 전달용 컬럼명
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
            "CTR": "CTR",
            "CVR": "CVR",
            "CPA": "CPA",
            "ROAS": "ROAS",
        }
    )

    # 정렬
    df = df.sort_values("비용", ascending=False)

    # 표시용 포맷
    display_df = df.copy()
    for col in ["비용", "매출", "CPA"]:
        display_df[col] = (
            display_df[col]
            .round()
            .astype(int)
            .map("{:,}".format)
        )
    for col in ["CTR", "CVR", "ROAS"]:
        display_df[col] = (
            display_df[col]
            .round(2)
            .astype(str)
            + "%"
        )

    # 컬럼 순서 명시적으로 고정 (CVR 포함해서 누락 없이 표시)
    column_order = [
        "캠페인명",
        "광고그룹명",
        "소재명",
        "비용",
        "노출",
        "클릭",
        "구매",
        "매출",
        "장바구니",
        "CTR",
        "CVR",
        "CPA",
        "ROAS",
    ]
    display_df = display_df[column_order]

    display_df.index = range(1, len(display_df) + 1)

    return display_df, unmatched_report
