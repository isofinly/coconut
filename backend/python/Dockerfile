FROM python:3.11-slim

WORKDIR /app/

COPY /requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN python -m spacy download en_core_web_sm
RUN python -m spacy download ru_core_news_sm
RUN python -m spacy download uk_core_news_sm
RUN python -m spacy download ro_core_news_sm
RUN python -m spacy download fr_core_news_sm
RUN python -m spacy download de_core_news_sm

COPY . .

EXPOSE 3030

CMD ["python", "app.py"]