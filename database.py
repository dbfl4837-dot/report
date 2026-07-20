import pandas as pd
import numpy as np
from models import COLUMN_CANDIDATES


def find_column(df, candidates):
    for c in candidates:
        if c in df.columns:
            return c
    return None


def load_and_validate(file):
    # 파일 읽기
    if file.name.lower().endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    # 컬럼 자동 매칭
    mapping = {}

    for key, candidates in COLUMN_CANDIDATES.items():
        col = find_column(df, candidates)
        if col:
            mapping[key] = col

    # 표준 컬럼 생성
    data = pd.DataFrame()

    data["캠페인"] = df[mapping["campaign"]] if "campaign" in mapping else ""
    data["광고그룹"] = df[mapping["adgroup"]] if "adgroup" in mapping else ""
    data["소재명"] = df[mapping["creative"]] if "creative" in mapping else ""

    data["비용"] = (
        pd.to_numeric(df[mapping["cost"]], errors="coerce").fillna(0)
        if "cost" in mapping else 0
    )

    data["노출"] = (
        pd.to_numeric(df[mapping["impression"]], errors="coerce").fillna(0)
        if "impression" in mapping else 0
    )

    data["클릭"] = (
        pd.to_numeric(df[mapping["click"]], errors="coerce").fillna(0)
        if "click" in mapping else 0
    )

    data["구매"] = (
        pd.to_numeric(df[mapping["purchase"]], errors="coerce").fillna(0)
        if "purchase" in mapping else 0
    )

    data["매출"] = (
        pd.to_numeric(df[mapping["revenue"]], errors="coerce").fillna(0)
        if "revenue" in mapping else 0
    )

    data["장바구니"] = (
        pd.to_numeric(df[mapping["atc"]], errors="coerce").fillna(0)
        if "atc" in mapping else 0
    )

    data["타겟"] = df[mapping["target"]] if "target" in mapping else ""
    data["지면"] = df[mapping["placement"]] if "placement" in mapping else ""

    # ===== 자동 계산 =====

    data["CTR"] = np.where(
        data["노출"] > 0,
        data["클릭"] / data["노출"] * 100,
        0
    )

    data["CVR"] = np.where(
        data["클릭"] > 0,
        data["구매"] / data["클릭"] * 100,
        0
    )

    data["CPC"] = np.where(
        data["클릭"] > 0,
        data["비용"] / data["클릭"],
        0
    )

    data["CPA"] = np.where(
        data["구매"] > 0,
        data["비용"] / data["구매"],
        0
    )

    data["ROAS"] = np.where(
        data["비용"] > 0,
        data["매출"] / data["비용"] * 100,
        0
    )

    return data