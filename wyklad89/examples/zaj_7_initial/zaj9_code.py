from prettytable import PrettyTable

__author__ = 'jb'

import settings
import time
TABLE_STATS = """
CREATE OR REPLACE VIEW table_stats AS
SELECT
stat.relname AS relname,
seq_scan, seq_tup_read, idx_scan, idx_tup_fetch,
heap_blks_read, heap_blks_hit, idx_blks_read, idx_blks_hit
FROM
pg_stat_user_tables stat
RIGHT JOIN pg_statio_user_tables statio
ON stat.relid=statio.relid;
"""

def create_table_stats():
    session = settings.Session()
    session.execute(TABLE_STATS)
    session.commit()
    session.close()


def p(res):
    t = PrettyTable(res.keys())
    t.align = "l"
    for row in list(res):
        t.add_row(row)
    return t
def e(sess, string):
    res = sess.execute(string)
    if not res.returns_rows:
          return None
    return res

def ee(sess, string):
    sess.execute("SELECT pg_stat_reset()");
    res = sess.execute(string)
    time.sleep(1)
    return sess.execute("SELECT * FROM table_stats");
