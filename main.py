import json
import requests
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Question(Base):
    __tablename__ = 'questions'
    questionID = Column(Integer, primary_key=True)
    questionIndex = Column(Integer)
    questionTitle = Column(String)
    paidOnly = Column(Integer)
    difficulty = Column(String)
    totalAcs = Column(Integer)
    totalAcsRate = Column(String)
    totalSubmits = Column(Integer)
    likes = Column(Integer)
    dislike = Column(Integer)
    # tags = Column(String)

def createDB(dbName='question.db'):
    engine = create_engine('sqlite:///{}'.format(dbName), echo=True)
    metadata = MetaData(engine)
    Base.metadata.create_all(engine, checkfirst=True)
    metadata.create_all()

def createSession(dbName='question.db'):
    engine = create_engine('sqlite:///{}'.format(dbName), echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def fetchAllQuestion():
    ret =list()
    response = requests.get('https://leetcode.com/api/problems/all/')
    responseJson = response.json()
    for stat_status_pair in responseJson['stat_status_pairs']:
        ret.append(stat_status_pair['stat']['question__title_slug'])
    return ret

def getQuestionInfo(name):
    query = """query questionData($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    questionId\n    questionFrontendId\n    title\n    isPaidOnly\n    difficulty\n    likes\n    dislikes\n    topicTags {\n      name\n      translatedName}\n    companyTagStats\n    stats\n    status\n    }\n}\n"""
    body = {"operationName":"questionData",
            "variables":{"titleSlug":name},
            "query":query}
    response = requests.post('https://leetcode.com/graphql', json=body)
    responseJson = response.json()
    return responseJson["data"]["question"]

def createQuestionObj(questionObj):
    ret = Question()
    ret.questionID = questionObj['questionId']
    ret.questionIndex = questionObj['questionFrontendId']
    ret.questionTitle = questionObj['title']
    ret.paidOnly = questionObj['isPaidOnly']
    ret.difficulty = questionObj['difficulty']
    ret.likes = questionObj['likes']
    ret.dislike = questionObj['dislikes']
    
    stats = json.loads(questionObj['stats'])
    ret.totalAcs = stats['totalAcceptedRaw']
    ret.totalSubmits = stats['totalSubmissionRaw']
    ret.totalAcsRate = stats['acRate']
    #ret[tags] = TODO
    return ret

def insertAllQuestions(questions): 
    objs = list()
    cur = 0
    for question in questions:
        cur += 1
        questionInfo = getQuestionInfo(question)
        questionObj = createQuestionObj(questionInfo)
        print('({}) / ({}) : {}, {}'.format(cur, len(questions), questionObj.questionIndex, questionObj.questionTitle))
        objs.append(questionObj)   
    session = createSession()
    session.add_all(objs)
    session.commit()
    pass

'''
def commitTester(questions):
    objs = list()
    cur = 0
    for iter in range(0,3):
        cur += 1
        questionInfo = getQuestionInfo(questions[iter])
        questionObj = createQuestionObj(questionInfo)
        print('({}) / ({}) : {}, {}'.format(cur, len(questions), questionObj.questionIndex, questionObj.questionTitle))
        objs.append(questionObj)   
    session = createSession()
    session.add_all(objs)
    session.commit()
    pass
'''

def queryBase():
    session = createSession()
    rets = session.query(Question)
    return rets

def queryLikes(query, num):
    rets = query.filter(Question.likes > num)
    return rets

def queryDislikes(query, num):
    rets = query.filter(Question.dislike > num)
    return rets

def queryLimit(query, num):
    rets = query.limit(num)
    return rets

def queryExec(query):
    rets = query.all()
    return rets

def main():
    #createDB()
    #questions = fetchAllQuestion()
    #insertAllQuestions(questions)
    
    rets = queryBase()
    rets = queryLikes(rets, 100)
    rets = queryDislikes(rets, 100)
    rets = queryLimit(rets, 10)
    rets = queryExec(rets)
    for ret in rets :
        print('{}, {}'.format(ret.questionID, ret.questionTitle))

if __name__ == '__main__':
    main()