# 경제 퀴즈 애플리케이션

경제 지식을 테스트하는 웹 기반 O/X 퀴즈 애플리케이션입니다.

## 🚀 주요 기능

- **O/X 퀴즈**: 간단한 참/거짓 문제로 경제 지식 테스트
- **실시간 통계**: 정답률, 정답/오답 개수 추적
- **랜덤 문제**: 매번 다른 경제 문제 제공
- **상세 설명**: 각 문제에 대한 해설 제공
- **반응형 디자인**: 모바일과 데스크톱 모두 지원

## 🛠 기술 스택

- **Backend**: FastAPI, SQLAlchemy, MySQL
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Database**: MySQL 8.0
- **Deployment**: Docker, Docker Compose

## 📁 프로젝트 구조

```
economy_quiz/
├── main.py                 # FastAPI 애플리케이션
├── database.py             # 데이터베이스 모델 및 설정
├── config.py               # 환경 설정
├── requirements.txt        # Python 의존성
├── docker-compose.yml      # Docker Compose 설정
├── Dockerfile             # Docker 이미지 설정
├── init.sql               # 초기 데이터
├── run_local.py           # 로컬 실행 스크립트
├── templates/
│   └── index.html         # 메인 페이지
└── static/
    ├── css/
    │   └── style.css      # 스타일시트
    └── js/
        └── app.js         # 클라이언트 JavaScript
```

## 🚀 실행 방법

### 방법 1: Docker Compose 사용 (권장)

1. **프로젝트 클론 및 이동**
   ```bash
   cd economy_quiz
   ```

2. **Docker Compose로 실행**
   ```bash
   docker-compose up --build
   ```

3. **샘플 데이터 추가 (선택사항)**
   ```bash
   python add_sample_data.py
   ```

4. **브라우저에서 접속**
   - 로컬: http://localhost:8000
   - 외부 접속: http://[서버IP]:8000

### 방법 2: 로컬 환경에서 실행

1. **MySQL 설치 및 실행**
   ```bash
   # macOS (Homebrew)
   brew install mysql
   brew services start mysql
   
   # Ubuntu/Debian
   sudo apt-get install mysql-server
   sudo systemctl start mysql
   ```

2. **데이터베이스 생성**
   ```sql
   CREATE DATABASE economy_quiz;
   CREATE USER 'quiz_user'@'localhost' IDENTIFIED BY 'quiz_password';
   GRANT ALL PRIVILEGES ON economy_quiz.* TO 'quiz_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

3. **Python 의존성 설치**
   ```bash
   pip install -r requirements.txt
   ```

4. **애플리케이션 실행**
   ```bash
   python run_local.py
   ```

## 🔧 설정

`config.py` 파일에서 다음 설정을 변경할 수 있습니다:

```python
# 데이터베이스 설정
DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "quiz_user"
DB_PASSWORD = "quiz_password"
DB_NAME = "economy_quiz"

# API 설정
API_HOST = "0.0.0.0"  # 외부 접속 허용
API_PORT = 8000
```

## 📊 API 엔드포인트

- `GET /` - 메인 페이지
- `GET /api/quizzes` - 퀴즈 목록 조회
- `GET /api/quizzes/random` - 랜덤 퀴즈 조회
- `GET /api/quizzes/{id}` - 특정 퀴즈 조회
- `POST /api/quizzes` - 새 퀴즈 생성
- `PUT /api/quizzes/{id}` - 퀴즈 수정
- `DELETE /api/quizzes/{id}` - 퀴즈 삭제
- `GET /api/categories` - 카테고리 목록 조회

## 🎯 사용법

1. **퀴즈 시작**: 웹페이지에 접속하면 자동으로 랜덤 문제가 표시됩니다.
2. **답변 선택**: O(맞습니다) 또는 X(틀렸습니다) 버튼을 클릭합니다.
3. **결과 확인**: 정답 여부와 해설을 확인합니다.
4. **다음 문제**: "다음 문제" 버튼을 클릭하여 새로운 문제를 받습니다.
5. **통계 확인**: 하단에서 정답률과 통계를 확인할 수 있습니다.

## 📝 퀴즈 추가

새로운 퀴즈를 추가하려면:

1. **API 사용**:
   ```bash
   curl -X POST "http://localhost:8000/api/quizzes" \
        -H "Content-Type: application/json" \
        -d '{
          "question": "새로운 경제 문제",
          "answer": true,
          "explanation": "해설 내용",
          "category": "카테고리",
          "difficulty": "medium"
        }'
   ```

2. **데이터베이스 직접 삽입**:
   ```sql
   INSERT INTO quizzes (question, answer, explanation, category, difficulty) 
   VALUES ('새로운 문제', true, '해설', '카테고리', 'medium');
   ```

## 🐳 Docker 명령어

```bash
# 컨테이너 빌드 및 실행
docker-compose up --build

# 백그라운드 실행
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 컨테이너 중지
docker-compose down

# 볼륨까지 삭제 (데이터 초기화)
docker-compose down -v
```

## 🔍 문제 해결

### Docker Compose 실행 오류
```bash
# 기존 컨테이너와 볼륨 정리
docker-compose down -v
docker system prune -f

# 다시 실행
docker-compose up --build
```

### MySQL 연결 오류
- MySQL 서버가 실행 중인지 확인
- 데이터베이스와 사용자가 생성되었는지 확인
- 방화벽 설정 확인
- Docker Compose에서 health check가 완료될 때까지 대기

### API 서버 시작 실패
- MySQL 컨테이너가 완전히 준비될 때까지 대기 (약 30-60초)
- 로그에서 "데이터베이스 테이블 생성 완료" 메시지 확인
- 재시도 로직이 포함되어 있어 자동으로 복구됩니다

### 샘플 데이터 추가 실패
```bash
# API 서버 상태 확인
curl http://localhost:8000/api/categories

# 수동으로 샘플 데이터 추가
python add_sample_data.py
```

### 포트 충돌
- 8000번 포트가 사용 중인 경우 `config.py`에서 `API_PORT` 변경
- 3306번 포트가 사용 중인 경우 `docker-compose.yml`에서 포트 매핑 변경

### 외부 접속 불가
- `API_HOST`를 `0.0.0.0`으로 설정했는지 확인
- 방화벽에서 8000번 포트 허용 확인

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 🤝 기여

버그 리포트나 기능 제안은 이슈를 통해 알려주세요.

---

**즐거운 경제 학습 되세요! 📚💰**
