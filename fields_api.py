import datetime as dt
import tornado.escape
import tornado.ioloop
import tornado.web
from influxdb import InfluxDBClient

def create_client(host, port):
    client = InfluxDBClient(host, port, 'root', 'root', 'mydb')
    return client

class FieldsHandler(tornado.web.RequestHandler):
    def _influx_write(self, mname, value, topic, time_created=None):
        if time_created is None:
            time_created = dt.datetime.utcnow().isoformat()
        json_body = [
                {
                    "measurement": mname,
                    "tags": {
                        "topic": topic,
                    },
                    "time": time_created,
                    "fields": {
                        "value": value
                    }
                }
            ]
        self.influx_client.write_points(json_body)

    def initialize(self, influx_client):
        self.influx_client = influx_client
 
    def post(self, topic):
        time_created = self.get_argument('timestamp', None)
        mname = self.get_argument('name')
        value = self.get_argument('value')
        
        self._influx_write(mname, value, topic, time_created)
        
        self.set_status(200)
        self.finish()

