#!/usr/bin/env python3
"""
로컬에서 직접 실행하는 스크립트
MySQL이 로컬에 설치되어 있어야 합니다.
"""

import subprocess
import sys
import time
import os
from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME, API_HOST, API_PORT

def check_mysql_connection():
    """MySQL 연결 확인"""
    try:
        import pymysql
        connection = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        connection.close()
        print("✅ MySQL 연결 성공")
        return True
    except Exception as e:
        print(f"❌ MySQL 연결 실패: {e}")
        print("MySQL이 실행 중인지 확인하고 데이터베이스가 생성되었는지 확인하세요.")
        return False

def install_dependencies():
    """의존성 설치"""
    print("📦 의존성 설치 중...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ 의존성 설치 완료")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 의존성 설치 실패: {e}")
        return False

def create_database():
    """데이터베이스 생성"""
    try:
        import pymysql
        # 데이터베이스 생성
        connection = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        connection.commit()
        connection.close()
        print("✅ 데이터베이스 생성 완료")
        return True
    except Exception as e:
        print(f"❌ 데이터베이스 생성 실패: {e}")
        return False

def run_server():
    """서버 실행"""
    print(f"🚀 서버 시작 중... (http://{API_HOST}:{API_PORT})")
    try:
        import uvicorn
        uvicorn.run("main:app", host=API_HOST, port=API_PORT, reload=True)
    except KeyboardInterrupt:
        print("\n👋 서버를 종료합니다.")
    except Exception as e:
        print(f"❌ 서버 실행 실패: {e}")

def main():
    print("🎯 경제 퀴즈 애플리케이션 시작")
    print("=" * 50)
    
    # 1. 의존성 설치
    if not install_dependencies():
        return
    
    # 2. 데이터베이스 생성
    if not create_database():
        return
    
    # 3. MySQL 연결 확인
    if not check_mysql_connection():
        print("\n💡 해결 방법:")
        print("1. MySQL 서버가 실행 중인지 확인")
        print("2. config.py에서 데이터베이스 설정 확인")
        print("3. MySQL 사용자 권한 확인")
        return
    
    # 4. 서버 실행
    run_server()

if __name__ == "__main__":
    main()
