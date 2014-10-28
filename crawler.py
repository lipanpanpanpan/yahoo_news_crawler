#-*- coding:utf-8 -*-
import httplib2
import urllib
import json
from bs4 import BeautifulSoup
import bs4

mainpage_url = 'http://news.yahoo.com/us/most-popular/'
comment_base_url = 'http://news.yahoo.com/_xhr/contentcomments/get_all/?'
reply_base_url = 'http://news.yahoo.com/_xhr/contentcomments/get_replies/?'

t_news_url = 'http://news.yahoo.com/ebola-victims-sister-says-hospital-denied-request-025725064.html'

def urlencode(base, param):
    param_code = urllib.urlencode(param)
    rurl = base + param_code
    return rurl

def get_response(url):
    head, content = httplib2.Http().request(url)
    return head, content

def get_news_mainpage():
    mainpage_head, mainpage_content = get_response(mainpage_url)
    return mainpage_head, mainpage_content

def parse_news_from_mainpage(mainpage_content):
    soup = BeautifulSoup(mainpage_content, from_encoding='utf-8')
    l_news = soup.find_all('div', {'class':'body-wrap'})
    for n in l_news:
        print n.h3.a['href']
        print n.p
    print len(l_news)

def parse_news_title_and_content(news_url):
    head, content = httplib2.Http().request(news_url)
    soup = BeautifulSoup(content.decode('utf-8'))
    title = soup.find('h1', {'class':'headline'}).string
    news_time = soup.find('abbr').string
    l_p = soup.find_all('p', {'class':False})
    c_num = soup.find('span', {'id':'total-comment-count'}).string
    press_name = soup.find('img', {'class':'provider-img'})
    content_id = soup.find('section', {'id':'mediacontentstory'})
    c_id = content_id['data-uuid']
    p_name = press_name['alt']
    l_content = []
    for p in l_p:
        if len(p.contents) > 0 and type(p.contents[0])==bs4.element.NavigableString:
            l_content.append(p.string)
    content = '\n'.join(l_content).encode('utf-8')
    news_dict = {}
    news_dict['title'] = title
    news_dict['content'] = content
    news_dict['comment_num'] = int(c_num)
    news_dict['press_name'] = press_name
    news_dict['content_id'] = c_id
    news_dict['time'] = news_time
    return news_dict

def parse_comments(content_url, content_id, current_index):
    head, content = httplib2.Http().request(content_url)
    j_data = json.loads(content)
    more_url = j_data['more']
    soup = BeautifulSoup(j_data['commentList'])
    comment_list = soup.find_all('li', {'data-uid':True})

    for comment in comment_list:
        comment_id = comment['data-cmt']
        span_nickname = comment.find('span', {'class':'int profile-link'})
        span_timestamp = comment.find('span', {'class':'comment-timestamp'})
        p_comment_content = comment.find('p', {'class', 'comment-content'})
        div_thumb_up = comment.find('div', {'id':'up-vote-box'})
        div_thumb_down = comment.find('div', {'id':'down-vote-box'})
        nickname = span_nickname.string
        timestamp = span_timestamp.string
        content = '\n'.join([x.string.strip() for x in p_comment_content.contents if x.string])
        thumb_up_count = int(div_thumb_up.span.string)
        thumb_down_count = int(div_thumb_down.span.string)

        span_reply = comment.find('span', {'class':'replies int'})
        if span_reply:
            reply_url = urlencode(reply_base_url, {'content_id':content_id, 'comment_id':comment_id})
            parse_reply_comment(reply_url, content_id, comment_id, 0)
        #div_reply = comment.
        #print nickname, timestamp, thumb_up_count, thumb_down_count, content.encode('utf-8')
    if more_url:
        m_soup = BeautifulSoup(more_url)
        nextpage_url = urlencode(comment_base_url, {'content_id':content_id}) + '&'+ m_soup.li.span['data-query']
        current_index = current_index + len(comment_list)
        print current_index
'''
        parse_comments(nextpage_url, content_id, current_index)
    else:
        return
'''

def parse_reply_comment(content_url, content_id, comment_id, current_index):
    head, content = httplib2.Http().request(content_url)
    j_data = json.loads(content)
    more_url = j_data['more']
    soup = BeautifulSoup(j_data['commentList'])
    reply_comment_list = soup.find_all('li', {'data-uid':True})

    for comment in reply_comment_list:
        span_nickname = comment.find('span', {'class':'int profile-link'})
        span_timestamp = comment.find('span', {'class':'comment-timestamp'})
        p_comment_content = comment.find('p', {'class', 'comment-content'})
        div_thumb_up = comment.find('div', {'id':'up-vote-box'})
        div_thumb_down = comment.find('div', {'id':'down-vote-box'})
        nickname = span_nickname.string
        timestamp = span_timestamp.string
        content = '\n'.join([x.string.strip() for x in p_comment_content.contents if x.string])
        thumb_up_count = int(div_thumb_up.span.string)
        thumb_down_count = int(div_thumb_down.span.string)
        print content.encode('utf-8')

    if more_url:
        m_soup = BeautifulSoup(more_url)
        nextpage_url = urlencode(reply_base_url, {'content_id':content_id, 'comment_id':comment_id}) + '&'+ m_soup.li.span['data-query']
        current_index = current_index + len(comment_list)
        print current_index
            
if __name__=='__main__':
    yahoo_mainpage_head, yahoo_mainpage_content = get_news_mainpage()
    #parse_news_from_mainpage(yahoo_mainpage_content)
    news_dict = parse_news_title_and_content(t_news_url)
    news_c_id = news_dict['content_id']
    param_dict = {'content_id':news_c_id, 'sortBy':'highestRated'}
    rurl = urlencode(comment_base_url, param_dict)
    parse_comments(rurl, news_c_id, 0)
