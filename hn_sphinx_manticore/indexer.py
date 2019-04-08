import csv

import MySQLdb
import MySQLdb.cursors
import time


class Indexer(object):

    def __init__(self, host, port):
        connection = MySQLdb.connect(
            host=host,
            port=port,
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
            charset='utf8',
        )
        self.conn = connection

    def index(self, name):
        ts = time.time()
        sql = """INSERT INTO full (id, story_id, story_time, story_url, story_text, story_author, comment_id, 
        comment_text, comment_author, comment_ranking, author_comment_count, story_comment_count) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        counter = 1

        with open('/home/mis/data/csv/hacker_news_comments.prepared.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if not counter % 1000:
                    print("Total Processed {}".format(counter))
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
        print("Total Time Taken for {0} is {1}".format(name, time.time()-ts))
        return True


if __name__ == '__main__':
    import multiprocessing

    def index_search(host, port):
        index_object = Indexer(host, port)
        index_object.index('sphinx')

    def index_manticore(host, port):
        index_object = Indexer(host, port)
        index_object.index('manticore')


    queue = multiprocessing.Queue()
    host_list = [('hn_manticore', 9307), ('hn_sphinx', 9308)]
    for host, port in host_list:
        proc1 = multiprocessing.Process(target=index_manticore, args=('127.0.0.1', port))
        proc2 = multiprocessing.Process(target=index_search, args=('127.0.0.1', port))
        proc1.start()
        proc2.start()
