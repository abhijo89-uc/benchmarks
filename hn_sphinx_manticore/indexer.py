import csv

import MySQLdb


class Connector(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__()
            connection = MySQLdb.connect(
                host='127.0.0.1',
                port=9306,
                cursorclass=MySQLdb.cursors.DictCursor,
                use_unicode=True,
                charset='utf8',
            )
            cls._instance.connection = connection
        return cls._instance


class Indexer(object):

    def __init__(self):
        connector = Connector()
        self.conn = connector.connection

    def index(self):
        sql = """INSERT INTO full (id, story_id, story_time, story_url, story_text, story_author, comment_id, 
        comment_text, comment_author, comment_ranking, author_comment_count, story_comment_count) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        counter = 1
        with open('hacker_news_comments.10x.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                args = (
                    counter,
                    row['story_id'], row['story_time'], row['story_url'], row['story_text'],
                    row['story_author'], row['comment_id'], row['comment_text'], row['comment_author'],
                    row['comment_ranking'], row['author_comment_count'], row['story_comment_count']
                )
                self.conn.execute(sql, args)
                counter += 1

        return True


if __name__ == '__main__':
    index_object = Indexer()
    index_object.index()
