#-*- coding:utf-8 -*-
import time
import random
import datetime
import traceback

from crawler import *
from bussiness import *
from orm import *

ONE_MINUTE = 60
ONE_HOUR = 3600
LIMIT_COUNT = 20

def sleep_random_time(t):
    t_suspend = t + random.uniform(0, t/100.0)
    print 'sleeping for ' + str(t_suspend) + ' seconds.'
    time.sleep(t_suspend)

def visit_news_mainpage():
    y_news_head, y_news_content = get_news_mainpage()
    l_news = parse_news_from_mainpage(y_news_content)
    print len(l_news)
    session = get_session()
    try:
        for news in l_news:
            url = news[0]
            summary = news[1]
            print url
            url = url.encode('utf-8')
            summary = summary.encode('utf-8')
            news_dict = parse_news_title_and_content(url)
            title = news_dict['title']
            content = news_dict['content']
            comment_num = news_dict['comment_num']
            press_name = news_dict['press_name']
            content_id = news_dict['content_id']
            ntime = news_dict['time']
            NewsHandler().insert_news(session, url, title, summary, content, ntime, 0, press_name, comment_num, content_id)
            session.commit()
    except:
        traceback.print_exc() 
        session.rollback()
    finally:
        session.close()

def update_news_comment_number():
    session = get_session()
    news_id = -1
    try:
        l_news = NewsHandler().get_update_news_list(session)
        for item in l_news:
            news_url = item['url']
            news_id = item['id']
            comment_num = parse_comment_num(news_url)
            NewsHandler().update_comment_number(session, news_id, comment_num)
    except:
        NewsHandler().set_news_crawl_flag(session, news_id, 2)
        traceback.print_exc()
    finally:
        session.close()
    
def visit_news_comment():
    session = get_session()
    l_news = NewsHandler().get_news_without_crawl_comment(session)
    for n_i in l_news:
        news_id = n_i['id']
        news_url = n_i['url']
        content_id = n_i['content_id']
        comment_crawl_flag = n_i['comment_crawl_flag']
        try:
            param_dict = {'content_id':content_id, 'sortBy':'highestRated'}
            rurl = urlencode(comment_base_url, param_dict)
            parse_comments(session, rurl, content_id, 0, news_id)
            NewsHandler().set_news_crawl_flag(session, news_id, 1)
            session.commit()
        except:
            NewsHandler().set_news_crawl_flag(session, news_id, 2)
            traceback.print_exc()
        finally:
            session.close()
    
if __name__=='__main__':
    while(True):
        visit_news_mainpage()
        update_news_comment_number()
        visit_news_comment()
        sleep_random_time(ONE_MINUTE)
