import unittest
import datetime as dt

import tasks_queue

class TestTasksDB(unittest.TestCase):
    def _cmp_tasks(self, task1, task2):
        if task1.topic != task2.topic:
            return False
        if task1.name != task2.name:
            return False
        if task1.arguments != task2.arguments:
            return False
        if task1.priority != task2.priority:
            return False
        if task1.expiration != task2.expiration:
            return False
        if task1.expire_time != task2.expire_time:
            return False

        return True

    def setUp(self):
        tasks = tasks_queue.SqliteQueue("tasks.sqlite")
        tasks.delete()

    def test_add(self):
        tasks = tasks_queue.SqliteQueue("tasks.sqlite")
        new_task1 = tasks_queue.Task(topic="topic.topic1", name="task1", arguments="arg1", priority=1, expiration=0, expire_time=dt.datetime.utcnow())
        tasks.append(new_task1)
        new_task2 = tasks_queue.Task(topic="topic.topic2", name="task2", arguments="arg1", priority=0, expiration=1, expire_time=dt.datetime.utcnow()+dt.timedelta(days=1))
        tasks.append(new_task2)

        all = tasks.get_all()

        cnt = len(tasks)
        self.assertEqual(cnt, 2)
        self.assertTrue(self._cmp_tasks(all[1], new_task1))
        self.assertTrue(self._cmp_tasks(all[0], new_task2))

    def test_next(self):
        tasks = tasks_queue.SqliteQueue("tasks.sqlite")
        new_task1 = tasks_queue.Task(topic="topic.topic1", name="task1", arguments="arg1", priority=1, expiration=0, expire_time=dt.datetime.utcnow())
        tasks.append(new_task1)
        new_task2 = tasks_queue.Task(topic="topic.topic2", name="task2", arguments="arg1", priority=0, expiration=1, expire_time=dt.datetime.utcnow()+dt.timedelta(days=1))
        tasks.append(new_task2)
        new_task3 = tasks_queue.Task(topic="topic.topic2", name="task3", arguments="arg1", priority=2, expiration=1, expire_time=dt.datetime.utcnow()+dt.timedelta(days=1))
        tasks.append(new_task3)

        cnt = len(tasks)
        self.assertEqual(cnt, 3)

        next_task = tasks.popleft('topic.topic2')

        cnt = len(tasks)
        self.assertEqual(cnt, 2)
        self.assertTrue(self._cmp_tasks(new_task2, next_task))

    def test_expired(self):
        tasks = tasks_queue.SqliteQueue("tasks.sqlite")
        new_task1 = tasks_queue.Task(topic="topic.topic1", name="task1", arguments="arg1", priority=0, expiration=1, expire_time=dt.datetime.utcnow()-dt.timedelta(hours=1))
        tasks.append(new_task1)
        new_task2 = tasks_queue.Task(topic="topic.topic1", name="task2", arguments="arg1", priority=1, expiration=0, expire_time=dt.datetime.utcnow()+dt.timedelta(days=1))
        tasks.append(new_task2)
        new_task3 = tasks_queue.Task(topic="topic.topic1", name="task3", arguments="arg1", priority=2, expiration=1, expire_time=dt.datetime.utcnow()+dt.timedelta(days=1))
        tasks.append(new_task3)

        cnt = len(tasks)
        self.assertEqual(cnt, 3)

        next_task = tasks.popleft('topic.topic1')

        cnt = len(tasks)
        self.assertEqual(cnt, 2)
        self.assertTrue(self._cmp_tasks(new_task2, next_task))


if __name__ == '__main__':
    unittest.main()