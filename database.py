import pandas as pd
from models import REQUIRED_COLUMNS

def load_and_validate(file):
    # 확장자에 따른 파일 로드 및 엔진 명시
    if file.name.endswith('.csv'):
        df = pd.read_csv(file)
    else:
        # engine='openpyxl'을 추가하여 오류 해결
        df = pd.read_excel(file, engine='openpyxl')
    
    # 엑셀 컬럼 이름 매핑
    mapping = {
        '광고 소재 이름': '광고 이름',
        '광고 그룹 이름': '광고 세트 이름',
        '총비용': '지출 금액 (KRW)',
        '노출수': '노출',
        '구매완료 수': '구매',
        '구매완료 전환매출액': '구매 전환값',
        '클릭률(%)': 'CTR(전체)',
        '평균 CPC': 'CPC(링크 클릭당 비용)',
        '구매완료 광고수익률(%)': '구매 ROAS(광고 지출 대비 수익률)'
    }
    df = df.rename(columns=mapping)
    
    # 필수 컬럼 확인
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"필수 데이터가 없습니다: {missing}")
    return df