# Python 3.9 이미지를 기반으로 합니다.
FROM python:3.9-slim-buster

# 작업 디렉토리를 /app으로 설정합니다.
WORKDIR /app

# requirements.txt 파일을 컨테이너의 /app 디렉토리에 복사합니다.
COPY requirements.txt /app/

# 필요한 패키지를 설치합니다.
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드를 컨테이너의 /app 디렉토리에 복사합니다.
COPY . /app/

# Gunicorn을 사용하여 애플리케이션을 실행합니다.
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]