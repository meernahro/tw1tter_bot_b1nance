FROM python:slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 7999
CMD ["python3", "manage.py", "runserver", "0.0.0.0:7999"]

