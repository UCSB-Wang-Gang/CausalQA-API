from fastapi import FastAPI
from pydantic import BaseModel
import json
import os
import redis
import uvicorn

app = FastAPI()
redis = redis.Redis(host=os.environ.get('REDIS_HOST'), port=os.environ.get(
    'REDIS_PORT'), username=os.environ.get('REDIS_USERNAME'), password=os.environ.get('REDIS_PASSWORD'))


class Question(BaseModel):
    HITId: str
    AssignmentId: str
    WorkerId: str
    Question: str
    Answer: str
    Article: str
    Fact: str
    Q_Drop_Score: str
    A_Drop_Score: str
    Total_Possible_Score: str


@app.get("/api")
async def root():
    return {"message": "Hello World"}


@app.post("/api/update_question")
async def update_question(q_in: Question):
    question = q_in.dict()
    article = question['Article'].replace("https://en.wikipedia.org/wiki/", "")
    article = article.substring(0, article.index(
        "#")) if article.index("#") > 0 else article
    del question['Article']
    redis.execute_command('JSON.SET', article, '.', json.dumps(question))
    return {article: question}


@app.get("/api/count/{article}")
async def vote_count(article):
    question = redis.execute_command('JSON.GET', article)
    if question == None:
        return {article: {'AssignmentId': -1, 'Q_Drop_Score': -1, 'A_Drop_Score': -1, 'Total_Possible_Score': -1}}
    question = json.loads(question)
    return {article: {'AssignmentId': question['AssignmentId'], 'Q_Drop_Score': question['Q_Drop_Score'], 'A_Drop_Score': question['A_Drop_Score'], 'Total_Possible_Score': question['Total_Possible_Score']}}


@app.get("/api/exist/{article}")
async def wiki_exist(article):
    return ({article: {'exists': False}} if redis.execute_command('JSON.GET', article) == None else {article: {'exists': True}})

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=50000,
                ssl_keyfile=os.environ.get('SSL_KEY'), ssl_certfile=os.environ.get('SSL_CERT'),
                reload=True)
