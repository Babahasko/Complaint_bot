FROM python:3.12
WORKDIR /app

EXPOSE 80

# Add code and project dependencies
COPY requirements.txt ./
RUN pip install --upgrade setuptools
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app


#CMD ["python", "main.py"]