import tornado.escape
import tornado.ioloop
import tornado.web
import tasks_queue
import datetime as dt

def create_queue(db_path):
    return tasks_queue.SqliteQueue(db_path)


class TasksTopicHandler(tornado.web.RequestHandler):
    def initialize(self, tasks_queue):
        self.tasks = tasks_queue

    def get(self, topic):
        tasks = self.tasks.get_topic_all(topic)
        for task in tasks:
            self.write(''.join([task.name, ', ', task.arguments, '\n']))
        self.set_status(200)
        self.finish()

    def post(self, topic):
        name = self.get_argument('name')
        arguments = self.get_argument('arguments', "")
        priority = self.get_argument('priority', 1)
        expiration = self.get_argument('expiration', 0)
        expire_time = int(self.get_argument('expire_time', 0))

        expiration_date = dt.datetime.utcnow() + dt.timedelta(seconds=expire_time)

        task = tasks_queue.Task(topic, name, arguments, priority, expiration, expiration_date)
        self.tasks.append(task)
        self.set_status(200)
        self.finish()


class TasksNextHandler(tornado.web.RequestHandler):
    def initialize(self, tasks_queue):
        self.tasks = tasks_queue

    def post(self, topic):
        task = self.tasks.popleft(topic)
        if task:
            self.write(''.join([task.name, ', ', task.arguments, '\n']))

        self.set_status(200)
        self.finish()


class TasksPeekHandler(tornado.web.RequestHandler):
    def initialize(self, tasks_queue):
        self.tasks = tasks_queue

    def get(self, topic):
        task = self.tasks.peek(topic)
        if task:
            self.write(''.join([task.name, ', ', task.arguments, '\n']))

        self.set_status(200)
        self.finish()



