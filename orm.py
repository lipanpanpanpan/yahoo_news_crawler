#-*- coding:utf-8 -*-
import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def get_session():
    engine = create_engine('mysql+mysqldb://bshi:20141031shib@seis10/bshi?charset=utf8', pool_recycle=1800, pool_size=20, encoding='utf-8')
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

class News(Base):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True)
    url = Column(String, default='')
    title = Column(String, default='')
    summary = Column(String, default='')
    content = Column(String, default='')
    time_text = Column(String, default='')
    comment_crawl_flag = Column(Integer, default=0)
    press = Column(String, default='')
    comment_num = Column(Integer, default=0)
    crawl_timestamp = Column(DateTime, default=datetime.datetime.now())
    content_id = Column(String, default='')

class Comment(Base):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True)
    nick = Column(String, default='')
    thumb_up = Column(Integer, default=0)
    thumb_down = Column(Integer, default=0)
    content = Column(String, default='')
    is_reply = Column(Integer, default=0)
    has_reply = Column(Integer, default=0)
    reply_comment_id = Column(Integer, default=0)
    news_id = Column(Integer, default=0)

if __name__=='__main__':
    session = get_session()
    t_n = News()
    session.add(t_n)
    session.commit()