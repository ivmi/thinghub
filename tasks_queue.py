import os, sqlite3
import datetime as dt
import json
from datetime import datetime
"""
Task
    topic
    name
    arguments
    priority
    expiration
    expire_time
"""
def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type not serializable")

class Task(object):
    def __init__(self, topic, name, arguments, priority, expiration, expire_time):
        self.topic = topic
        self.name = name
        self.arguments = arguments
        self.priority = priority
        self.expiration = expiration
        self.expire_time = expire_time

    def to_json(self):
        return {
            'topic': self.topic,
            'name': self.name,
            'arguments': self.arguments,
            'priority': self.priority,
            'expiration': self.expiration,
            'expire_time': self.expire_time
        }

    def __repr__(self):
        return json.dumps(self.to_json(), indent=4, default=json_serial)


class SqliteQueue(object):

    _create = (
            'CREATE TABLE IF NOT EXISTS queue ' 
            '('
            '  id INTEGER PRIMARY KEY AUTOINCREMENT,'
            '  topic TEXT,'
            '  name TEXT, '
            '  arguments TEXT, '
            '  priority INTEGER, '
            '  expiration INTEGER, '
            '  expire_time TIMESTAMP'
            ')'
            )

    _delete = 'DROP TABLE IF EXISTS queue '
    _count = 'SELECT COUNT(*) FROM queue'
    _iterate = 'SELECT id, item FROM queue'
    _append = 'INSERT INTO queue(topic, name, arguments, priority, expiration, expire_time) VALUES (?, ?, ?, ?, ?, ?)'
    _write_lock = 'BEGIN IMMEDIATE'
    _popleft_get = (
            'SELECT * FROM queue '
            'WHERE topic = ? AND (expiration = 0 OR expire_time > ?) '
            'ORDER BY priority ASC, id ASC LIMIT 1 '
            )
    _popleft_del = 'DELETE FROM queue WHERE id = ?'
    _peek = (
            'SELECT * FROM queue '
            'WHERE topic = ? AND (expiration = 0 OR expire_time > ?) '
            'ORDER BY priority ASC, id ASC LIMIT 1'
            )
    _get_topic = (
            'SELECT * FROM queue '
            'WHERE topic = ? AND (expiration = 0 OR expire_time > ?) '
            'ORDER BY priority ASC, id ASC '
            )
    _get_all = (
            'SELECT * FROM queue '
            'expiration = 0 OR expire_time > ? '
            'ORDER BY priority ASC, id ASC '
            )
    _clean = (
        'DELETE FROM queue WHERE (expiration = 1 AND expire_time < ?) '
    )

#    _get_all = (
#            'SELECT topic, name, arguments, priority, expiration, expire_time as "timestamp" FROM queue '
#            'ORDER BY priority ASC, id ASC '
#            )

    def __init__(self, path):
        self.path = os.path.abspath(path)
        self.conn = sqlite3.Connection(self.path, timeout=60, detect_types=sqlite3.PARSE_DECLTYPES )
        self.conn.execute(self._create)

    def delete(self):
        self.conn.execute(self._delete)
        self.conn.commit() # unlock the database

    def __len__(self):
        l = self.conn.execute(self._count).fetchone()[0]
        return l

#    def __iter__(self):
#        for id, obj_buffer in self.conn.execute(self._iterate):
#            yield loads(str(obj_buffer))

    def append(self, task):
        if not task.expire_time:
            task.expire_time = dt.datetime.utcnow()
        self.conn.execute(self._append, (task.topic, task.name, task.arguments, task.priority, task.expiration, task.expire_time, ) )
        self.conn.commit() # unlock the database

    def popleft(self, topic, t=None):
        if not t:
            t = dt.datetime.utcnow()

        self.conn.execute(self._write_lock)
        cursor = self.conn.execute(self._popleft_get, (topic,t))
        tsk = cursor.fetchone()
        task = None
        
        if tsk:
            self.conn.execute(self._popleft_del, (tsk[0],))
            task = Task(tsk[1], tsk[2], tsk[3], tsk[4], tsk[5], tsk[6], )
        self.conn.commit() # unlock the database
        return task
        
    def peek(self, topic, t=None):
        if not t:
            t = dt.datetime.utcnow()

        cursor = self.conn.execute(self._peek, (topic, t))
        try:
            tsk = cursor.fetchone()
            if tsk:
                return Task(tsk[1], tsk[2], tsk[3], tsk[4], tsk[5], tsk[6], )
            else:
                return None
        except StopIteration:
            return None

    def get_topic_all(self, topic, t=None):
        if not t:
            t = dt.datetime.utcnow()

        cursor = self.conn.execute(self._get_topic, (topic,t))
        tsks = cursor.fetchall()
        tasks = [Task(tsk[1], tsk[2], tsk[3], tsk[4], tsk[5], tsk[6], ) for tsk in tsks]
        return tasks

    def get_all(self):
        cursor = self.conn.execute(self._get_all)
        tsks = cursor.fetchall()
        tasks = [Task(tsk[1], tsk[2], tsk[3], tsk[4], tsk[5], tsk[6], ) for tsk in tsks]
        return tasks

    def clean(self):
        cursor = self.conn.execute(self._clean)
        self.conn.commit() # unlock the database

