import csv

import MySQLdb
import MySQLdb.cursors


class Indexer(object):

    def __init__(self, host):
        connection = MySQLdb.connect(
            host=host,
            port=9306,
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
            charset='utf8',
        )
        self.conn = connection

    def index(self):
        sql = """INSERT INTO full (id, story_id, story_time, story_url, story_text, story_author, comment_id, 
        comment_text, comment_author, comment_ranking, author_comment_count, story_comment_count) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        counter = 1
        with open('/root/csv/hacker_news_comments.prepared.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if None in row.values():
                    continue
                args = (
                    counter,
                    row['story_id'], row['story_time'], row.get('story_url', ''), row['story_text'],
                    row['story_author'], row['comment_id'], row['comment_text'], row['comment_author'],
                    row['comment_ranking'], row['author_comment_count'], row['story_comment_count']
                )
                try:
                    curr = self.conn.cursor()
                    curr.execute(sql, args)
                    counter += 1
                except:
                    continue

        return True


if __name__ == '__main__':

    host_list = ['hn_manticore', ]
    for host in host_list:
        index_object = Indexer(host)
        index_object.index()
