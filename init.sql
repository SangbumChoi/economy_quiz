-- 경제 퀴즈 초기 데이터
USE economy_quiz;

-- 테이블이 존재하는지 확인하고 샘플 퀴즈 데이터 삽입
-- (테이블은 FastAPI에서 자동으로 생성됩니다)

-- 샘플 퀴즈 데이터는 FastAPI 애플리케이션이 시작된 후
-- API를 통해 추가하거나 별도의 데이터 삽입 스크립트를 사용하세요.

-- 예시: API를 통한 데이터 추가
-- curl -X POST "http://localhost:8000/api/quizzes" \
--      -H "Content-Type: application/json" \
--      -d '{
--        "question": "인플레이션이란 물가가 지속적으로 상승하는 현상을 의미한다.",
--        "answer": true,
--        "explanation": "인플레이션은 일반적으로 물가수준이 지속적으로 상승하는 현상을 말합니다.",
--        "category": "기본경제개념",
--        "difficulty": "easy"
--      }'