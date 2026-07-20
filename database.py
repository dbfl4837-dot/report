import pandas as pd
from models import REQUIRED_COLUMNS

def load_and_validate(file):
    df = pd.read_excel(file)
    # 필수 컬럼 존재 여부 확인
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"필수 데이터가 없습니다: {missing}")
    return df