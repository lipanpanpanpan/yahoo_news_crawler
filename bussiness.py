#-*- coding:utf-8 -*-

from orm import *
class NewsHandler(object):
    def insert_news(self, session, url, title='', summary='', content='', time_text='', comment_crawl_flag=0, press='', comment_num=0, content_id=''):
        t_news = session.query(News).filter(News.url==url).first()
        if not t_news:
            n_news = News(url=url, title=title, summary=summary, content=content, time_text=time_text, comment_crawl_flag=comment_crawl_flag, press=press, comment_num=comment_num, content_id=content_id)
            session.add(n_news)
            session.flush()
            n_news = session.query(News).filter(News.url==url).first()
            return n_news.id
        else:
            return t_news.id

    def get_news_without_crawl_comment(self, session, count=20):
        news_list = session.query(News).filter(News.comment_crawl_flag==0).limit(count)
        return news_list

    def set_news_crawl_flag(self, session, id, flag=1):
        session.query(News).filter(News.id==id).update({News.comment_crawl_flag:flag})
        session.flush()

    def update_comment_number(self, session, id, comment_num):
        session.query(News).filter(News.id==id).update({News.comment_num:comment_num})
        session.flush()

class CommentHandler(object):
    def insert_comment(self, session, nick, thumb_up, thumb_down, content, is_reply, has_reply, reply_comment_id, news_id):
        t_comment = session.query(Comment).filter((Comment.nick==nick) & (Comment.content==content) & (Comment.news_id==news_id)).first()
        if not t_comment:
            n_comment = Comment(nick=nick, thumb_up=thumb_up, thumb_down=thumb_down, content=content, is_reply=is_reply, has_reply=has_reply, reply_comment_id=reply_comment_id, news_id=news_id)
            session.add(n_comment)
            session.flush()
            n_comment = session.query(Comment).filter((Comment.content==content) & (Comment.nick==nick) & (Comment.news_id==news_id)).first()
            return n_comment.id
        else:
            return t_comment.id
