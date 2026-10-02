import os
import time
from typesafe_sdk import TypeSafeClient, Choice, Noul

# 1. 클라이언트 생성
client = TypeSafeClient(api_key="apikey_2777800eebb7ad34a1796f3c242fb2b02d2_ff59820f0ca9c839ba81b2c7167d5a469b4a3a42a29cdf6b3aa450420c1b7261")

# 2. 분석할 데이터 (State)
context = {
    "user_tier": "VIP",
    "message": "결제가 두 번 되었는데 환불해주세요! 앱 오류 같습니다."
}

# --- [시간 측정 시작] ---
start_time = time.perf_counter()

# 3. 질문 및 판단 정의
response = client.decide(
    state=context,
    questions={
        "category": Choice(
            options=["billing", "technical", "account", "other"],
            description="고객 문의의 주된 카테고리를 선택하세요."
        ),
        "is_urgent": Noul(
            description="이 문의가 즉시 해결을 필요로 하는 긴급한 요청인가요?"
        )
    }
)

# --- [시간 측정 완료] ---
end_time = time.perf_counter()
elapsed_time_ms = (end_time - start_time) * 1000  # 밀리초(ms) 단위 변환

# 4. 결과 활용
category_result = response.questions["category"].selected_option
urgent_prob = response.questions["is_urgent"].probability

if category_result == "billing" and urgent_prob > 0.8:
    print("-> 긴급 결제 지원 팀으로 즉시 할당합니다.")
else:
    print("-> 일반 지원 큐로 이동합니다.")

# --- [시간 및 비용 출력] ---
print("\n" + "=" * 40)
print(f"⏱️  소요 시간 (Latency) : {elapsed_time_ms:.2f} ms")

# response 객체 내 사용량(usage) 메타데이터 확인
if hasattr(response, "usage") and response.usage:
    input_tokens = getattr(response.usage, "prompt_tokens", 0)
    output_tokens = getattr(response.usage, "completion_tokens", 0)
    total_tokens = getattr(response.usage, "total_tokens", input_tokens + output_tokens)
    
    # 예시 단가 (실제 TypeSafe 요금제 단가에 맞게 변경)
    # 예: 1k 토큰당 $0.0015 라면 -> 1토큰당 $0.0000015
    COST_PER_INPUT_TOKEN = 0.0000015
    COST_PER_OUTPUT_TOKEN = 0.0000020
    
    estimated_cost = (input_tokens * COST_PER_INPUT_TOKEN) + (output_tokens * COST_PER_OUTPUT_TOKEN)
    
    print(f"🔢 사용 토큰 수      : 입력 {input_tokens} / 출력 {output_tokens} (총 {total_tokens} tokens)")
    print(f"💵 예상 계산 비용    : ${estimated_cost:.6f} (약 {estimated_cost * 1350:.4f}원)")
else:
    # usage 정보를 SDK에서 dict 형식으로 제공할 경우
    print(f"📊 Response Metadata  : {getattr(response, 'metadata', 'N/A')}")
print("=" * 40)