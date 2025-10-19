import os
from typing import List, Optional
from dotenv import load_dotenv

import sqlalchemy
from sqlalchemy.engine import Engine, Row
from sqlalchemy.exc import SQLAlchemyError

from google.cloud.sql.connector import Connector, IPTypes
from cloud_sql_database_manager import CloudSQLDatabase

if __name__ == "__main__":
    
    load_dotenv()

    INSTANCE_CONNECTION_NAME = os.environ.get("INSTANCE_CONNECTION_NAME", "my-project:asia-northeast3:my-instance")
    DB_USER = os.environ.get("DB_USER", "postgres")
    DB_PASS = os.environ.get("DB_PASS", "your-db-password")
    DB_NAME = os.environ.get("DB_NAME", "my-database")
    TABLE_NAME = os.environ.get("TABLE_NAME", "test-db")

    ## MySQL의 경우 "mysql+pymysql"
    DB_DRIVER = "postgresql+pg8000" #"postgresql+psycopg2"
    DB_API_DRIVER = "pg8000" #"psycopg2"

    # 필수 환경 변수가 모두 설정되었는지 확인
    required_vars = {
        "INSTANCE_CONNECTION_NAME": INSTANCE_CONNECTION_NAME,
        "DB_USER": DB_USER,
        "DB_PASS": DB_PASS,
        "DB_NAME": DB_NAME
    }
    
    missing_vars = [key for key, value in required_vars.items() if not value]
    if missing_vars:
        raise ValueError(f"필수 환경 변수가 설정되지 않았습니다: {', '.join(missing_vars)}. .env 파일을 확인하세요.")

    print("Cloud SQL Python Connector를 초기화합니다...")
    connector = None
    conn = None

    try:
        connector = Connector()
        
        print(f"'{INSTANCE_CONNECTION_NAME}'에 직접 연결을 시도합니다 (드라이버: {DB_API_DRIVER})...")
        
        # SQLAlchemy 없이 직접 연결 시도
        # conn = connector.connect(
        #     INSTANCE_CONNECTION_NAME,
        #     driver=DB_API_DRIVER,
        #     user=DB_USER,
        #     password=DB_PASS,
        #     db=DB_NAME,
        # )
    
        db = CloudSQLDatabase(
            instance_connection_name=INSTANCE_CONNECTION_NAME,
            db_user=DB_USER,
            db_pass=DB_PASS,
            db_name=DB_NAME,
            db_api_driver=DB_API_DRIVER,
            db_driver=DB_DRIVER
        )

        columns = db.get_table_columns(TABLE_NAME)
        result = db.get_data(TABLE_NAME)

        print(' => Columns:', columns)
        print(' => Result [0]:', '\n', result[0])
        
    except Exception as e:
        print(f"❌ 스크립트 실행 중 오류 발생: {e}")
        print("\n=== 문제 해결 가이드 ===")
        print("1. .env 파일의 DB 접속 정보(INSTANCE_CONNECTION_NAME, USER, PASS, NAME)가 정확한지 확인하세요.")
        print("2. 터미널에서 'gcloud auth application-default login' 명령어로 GCP 인증을 완료했는지 확인하세요.")
        print("3. 'pip install --upgrade cloud-sql-python-connector psycopg2-binary' 명령어로 라이브러리를 최신 버전으로 업데이트하세요.")
        
    finally:
        if conn:
            conn.close()
            print("데이터베이스 연결을 닫았습니다.")
        if connector:
            connector.close()
            print("Cloud SQL 커넥터 리소스를 정리했습니다.")
