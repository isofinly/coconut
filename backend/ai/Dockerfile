FROM python:3.11-slim

COPY requirements.txt .

RUN pip3 install --pre torch --index-url https://download.pytorch.org/whl/nightly/cu121
RUN pip install -r requirements.txt

COPY . .

RUN "./install64.sh"

CMD ["python", "app.py"]