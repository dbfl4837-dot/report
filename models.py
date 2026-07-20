# models.py
COLUMN_CANDIDATES = {
    "campaign": [
        "캠페인 이름", "Campaign", "Campaign Name", "캠페인", "캠페인명"
    ],
    "adgroup": [
        "광고 세트 이름", "광고그룹 이름", "광고그룹", "Ad Set", "Ad Set Name",
        "광고그룹명", "그룹명", "그룹 이름", "Ad Group", "Ad Group Name",
        "AdSet Name", "타겟팅 이름", "세트 이름"
    ],
    "creative": [
        "광고 이름", "광고 소재 이름", "소재명", "Creative", "Ad Name",
        "광고명", "소재 이름", "Ad", "Creative Name"
    ],
    "cost": [
        "지출 금액 (KRW)", "총비용", "광고비", "비용", "Spend", "Cost",
        "사용 금액", "지출 금액", "소진 금액"
    ],
    "impression": [
        "노출", "노출수", "Impressions", "노출수(회)", "노출 수"
    ],
    "click": [
        "링크 클릭", "링크 클릭수", "클릭", "클릭수", "Clicks", "Link Clicks",
        "클릭 수"
    ],
    "purchase": [
        "구매", "구매완료 수", "구매완료", "Purchase", "Purchases",
        "전환수", "구매 수", "구매전환수"
    ],
    "revenue": [
        "구매완료 전환매출액", "구매완료 전환값", "구매 전환값", "전환매출액",
        "매출", "Revenue", "Purchase Value", "전환 가치", "구매 매출액"
    ],
    "atc": [
        "장바구니", "장바구니 추가", "장바구니 추가 수", "장바구니추가",
        "AddToCart", "Add to cart", "장바구니 담기", "장바구니 수",
        "장바구니담기", "장바구니전환수", "카트담기", "카트 담기",
        "장바구니 담기 수", "Add To Cart"
    ]
}