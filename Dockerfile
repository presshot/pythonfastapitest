FROM python:3.11-slim-buster



# 设置 root 用户的密码
RUN echo "root:admin123456" | chpasswd

COPY app.py app.py
RUN pip install fastapi uvicorn

ENTRYPOINT ["uvicorn", "app:app", "--host=0.0.0.0", "--port=80"]