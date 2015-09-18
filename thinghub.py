import tornado.web
from tornado.platform.asyncio import AsyncIOMainLoop
import asyncio
import fields_api
import tasks_api


def run():
    # tasks db
    tasks_queue = tasks_api.create_queue("test/tasks.sqlite")

    # influx db
    influx_client = fields_api.create_client('192.168.163.134', 8086)

    application = tornado.web.Application([
        #(r"/getfullpage", GetFullPageAsyncHandler),
        (r"/fields/([a-zA-Z0-9.]+)", fields_api.FieldsHandler, dict(influx_client=influx_client)),
        (r"/tasks/([a-zA-Z0-9.]+)", tasks_api.TasksTopicHandler, dict(tasks_queue=tasks_queue)),
        (r"/tasks/([a-zA-Z0-9.]+)/next", tasks_api.TasksNextHandler, dict(tasks_queue=tasks_queue)),
        (r"/tasks/([a-zA-Z0-9.]+)/peek", tasks_api.TasksPeekHandler, dict(tasks_queue=tasks_queue)),
    ])

    AsyncIOMainLoop().install()
    application.listen(8888)
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    run()