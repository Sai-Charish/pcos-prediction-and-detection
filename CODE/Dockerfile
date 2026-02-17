FROM python:latest
COPY . /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "./FRONTEND/PCOS.py"]
