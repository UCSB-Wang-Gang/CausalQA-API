from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
import redis
import uvicorn

app = FastAPI()
redis = redis.Redis(host=os.environ.get('REDIS_HOST'), port=os.environ.get(
    'REDIS_PORT'), username=os.environ.get('REDIS_USERNAME'), password=os.environ.get('REDIS_PASSWORD'))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    id = question['AssignmentId']
    article = question['Article'].replace("https://en.wikipedia.org/wiki/", "")
    article = article[0:article.index("#")] if article.index(
        "#") > 0 else article
    del question['Article']
    del question['AssignmentId']

    out = ({} if prev_article == None else json.loads(prev_article))
    prev_article = redis.execute_command('JSON.GET', article)
    out[id] = question
    redis.execute_command('JSON.SET', article, '.', json.dumps(out))
    return {article: out}


@app.get("/api/scores/{article_name}")
async def article_scores(article_name):
    questions = redis.execute_command('JSON.GET', article_name)
    if questions == None:
        return {}

    out = {}
    questions = json.loads(questions)
    for q in questions.keys():
        out[q] = {'Q_Drop_Score': questions[q]['Q_Drop_Score'], 'A_Drop_Score': questions[q]
                  ['A_Drop_Score'], 'Total_Possible_Score': questions[q]['Total_Possible_Score']}
    return {article_name: out}


@app.get("/api/scores/{article_name}/{assignment_id}")
async def article_scores(article_name, assignment_id):
    questions = redis.execute_command('JSON.GET', article_name)
    if questions == None:
        return {}

    out = {}
    questions = json.loads(questions)
    return ({} if assignment_id not in questions.keys()
            else {article_name: {assignment_id: {'Q_Drop_Score': questions[assignment_id]['Q_Drop_Score'],
                                                 'A_Drop_Score': questions[assignment_id]['A_Drop_Score'],
                                                 'Total_Possible_Score': questions[assignment_id]['Total_Possible_Score']}}})


@app.get("/api/count/{article_name}")
async def article_count(article_name):
    article = redis.execute_command('JSON.GET', article_name)
    if article == None:
        return {article_name: {'count': 0}}
    article = json.loads(article)
    return{article_name: {'count': len(article.keys())}}


comparisons = {
    "eq": lambda x, y: x == y,
    "gt": lambda x, y: x > y,
    "lt": lambda x, y: x < y,
    "geq": lambda x, y: x >= y,
    "leq": lambda x, y: x <= y,
}


@app.get("/api/count/{comparison}/{count}")
async def article_count(comparison, count):
    if comparison not in comparisons.keys():
        return {"Error": "Invalid comparison"}

    out = {}
    for article_name in redis.scan_iter("*"):
        article = json.loads(redis.execute_command('JSON.GET', article_name))
        key_count = len(article.keys())
        if comparisons[comparison](key_count, int(count)):
            out[article_name] = {'count': key_count}
    return out


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=50000,
                ssl_keyfile=os.environ.get('SSL_KEY'), ssl_certfile=os.environ.get('SSL_CERT'),
                reload=True)
