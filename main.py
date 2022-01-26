from fastapi import FastAPI
from pydantic import BaseModel
import json
import os
import redis

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
    article = question['Article']
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


@app.get("/api/exist/{wiki_article}")
async def wiki_exist(wiki_article):
    return ({wiki_article: {'used': False}} if redis.execute_command('JSON.GET', wiki_article) == None else {wiki_article: {'used': True}})
