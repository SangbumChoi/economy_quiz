#!/usr/bin/env python3
"""
샘플 퀴즈 데이터를 데이터베이스에 추가하는 스크립트
"""

import requests
import json
import time

# 샘플 퀴즈 데이터
SAMPLE_QUIZZES = [
    {
        "question": "인플레이션이란 물가가 지속적으로 상승하는 현상을 의미한다.",
        "answer": True,
        "explanation": "인플레이션은 일반적으로 물가수준이 지속적으로 상승하는 현상을 말합니다. 이는 통화량 증가, 수요 증가, 공급 감소 등의 요인으로 발생할 수 있습니다.",
        "category": "기본경제개념",
        "difficulty": "easy"
    },
    {
        "question": "GDP는 국내총생산을 의미하며, 한 나라의 경제 규모를 측정하는 지표이다.",
        "answer": True,
        "explanation": "GDP(Gross Domestic Product)는 국내총생산으로, 특정 기간 동안 한 나라 내에서 생산된 모든 최종재화와 서비스의 시장가치를 합한 것입니다.",
        "category": "기본경제개념",
        "difficulty": "easy"
    },
    {
        "question": "중앙은행의 주요 역할은 통화정책을 통해 경제를 관리하는 것이다.",
        "answer": True,
        "explanation": "중앙은행은 통화정책을 통해 물가안정과 경제성장을 도모하고, 금융시스템의 안정성을 유지하는 역할을 담당합니다.",
        "category": "금융정책",
        "difficulty": "medium"
    },
    {
        "question": "주식시장에서 주가가 상승하면 반드시 경제가 좋아진다는 뜻이다.",
        "answer": False,
        "explanation": "주가 상승이 반드시 경제 상황이 좋아진다는 의미는 아닙니다. 주가는 다양한 요인(심리, 유동성, 기대 등)에 의해 변동하며, 실물경제와 완전히 일치하지 않을 수 있습니다.",
        "category": "주식시장",
        "difficulty": "medium"
    },
    {
        "question": "복리란 원금에 이자를 더한 금액에 대해 다시 이자가 붙는 것을 말한다.",
        "answer": True,
        "explanation": "복리는 원금과 이자를 합한 금액에 대해 다시 이자가 붙는 것을 의미합니다. 시간이 지날수록 효과가 커지는 특징이 있습니다.",
        "category": "금융상식",
        "difficulty": "easy"
    },
    {
        "question": "경기침체는 GDP가 연속 2분기 동안 감소하는 현상이다.",
        "answer": True,
        "explanation": "일반적으로 경기침체는 GDP가 연속 2분기(6개월) 동안 감소하는 현상으로 정의됩니다. 이는 경제 활동이 전반적으로 위축된 상태를 의미합니다.",
        "category": "경기분석",
        "difficulty": "medium"
    },
    {
        "question": "환율이 상승하면 수출이 증가하고 수입이 감소한다.",
        "answer": True,
        "explanation": "환율 상승(원화 약세)은 수출 상품의 가격 경쟁력을 높여 수출을 증가시키고, 수입 상품의 가격을 상대적으로 높여 수입을 감소시킵니다.",
        "category": "국제경제",
        "difficulty": "medium"
    },
    {
        "question": "인플레이션은 항상 경제에 나쁜 영향을 미친다.",
        "answer": False,
        "explanation": "인플레이션은 적정 수준(보통 2-3%)에서는 경제 성장에 도움이 될 수 있습니다. 하지만 과도한 인플레이션은 경제에 악영향을 미칩니다.",
        "category": "기본경제개념",
        "difficulty": "hard"
    },
    {
        "question": "중앙은행이 기준금리를 인상하면 통화량이 감소한다.",
        "answer": True,
        "explanation": "기준금리 인상은 시중 금리를 상승시켜 대출을 줄이고 저축을 늘려 통화량을 감소시키는 효과가 있습니다.",
        "category": "금융정책",
        "difficulty": "hard"
    },
    {
        "question": "주식은 채권보다 위험하지만 수익률이 높을 가능성이 크다.",
        "answer": True,
        "explanation": "주식은 채권보다 변동성이 크고 위험이 높지만, 장기적으로는 더 높은 수익률을 제공할 가능성이 큽니다.",
        "category": "투자상식",
        "difficulty": "easy"
    }
]

def add_sample_data(api_url="http://localhost:8000"):
    """샘플 데이터를 API를 통해 추가"""
    print("📝 샘플 퀴즈 데이터 추가 중...")
    
    success_count = 0
    error_count = 0
    
    for i, quiz in enumerate(SAMPLE_QUIZZES, 1):
        try:
            response = requests.post(
                f"{api_url}/api/quizzes",
                json=quiz,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"✅ 퀴즈 {i} 추가 성공: {quiz['question'][:30]}...")
                success_count += 1
            else:
                print(f"❌ 퀴즈 {i} 추가 실패: {response.status_code} - {response.text}")
                error_count += 1
                
        except requests.exceptions.RequestException as e:
            print(f"❌ 퀴즈 {i} 추가 중 오류: {e}")
            error_count += 1
        
        # API 부하 방지를 위한 짧은 대기
        time.sleep(0.1)
    
    print(f"\n📊 결과: 성공 {success_count}개, 실패 {error_count}개")
    
    if success_count > 0:
        print("🎉 샘플 데이터 추가가 완료되었습니다!")
        print(f"🌐 브라우저에서 http://localhost:8000 에 접속하여 퀴즈를 시작하세요!")
    else:
        print("⚠️  데이터 추가에 실패했습니다. API 서버가 실행 중인지 확인하세요.")

def check_api_health(api_url="http://localhost:8000"):
    """API 서버 상태 확인"""
    try:
        response = requests.get(f"{api_url}/api/categories", timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    print("🎯 경제 퀴즈 샘플 데이터 추가 도구")
    print("=" * 50)
    
    # API 서버 상태 확인
    if not check_api_health():
        print("❌ API 서버에 연결할 수 없습니다.")
        print("💡 다음을 확인하세요:")
        print("   1. Docker Compose가 실행 중인지 확인")
        print("   2. API 서버가 http://localhost:8000 에서 실행 중인지 확인")
        print("   3. 잠시 후 다시 시도해보세요")
        return
    
    print("✅ API 서버 연결 확인됨")
    add_sample_data()

if __name__ == "__main__":
    main()
