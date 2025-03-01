# 기본 Python 이미지 선택
FROM python:3.9

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 프로그램 설치
RUN apt-get update && \
    apt-get install -y ffmpeg

# Python 패키지 설치
COPY app/requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# 앱 코드 복사
COPY ./app .

# 서버 실행 명령
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]