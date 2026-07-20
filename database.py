import pandas as pd

def load_and_validate(file):
    df = pd.read_excel(file)
    
    # 엑셀의 실제 컬럼명을 프로그램이 쓰는 이름으로 바꾸기 (매핑)
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
    
    # 이제 필요한 컬럼이 다 있는지 확인
    required = ['광고 세트 이름', '광고 이름', '지출 금액 (KRW)', '구매', '구매 전환값', '노출']
    missing = [c for c in required if c not in df.columns]
    
    if missing:
        raise ValueError(f"필수 데이터가 없습니다: {missing}")
    
    return df