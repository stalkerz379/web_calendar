import sys
import datetime
from flask import Flask
from flask_restful import Api, Resource

app = Flask('web_calendar')
api = Api(app)

class ExtendResource(Resource):
    def get(self):
        return {"data": "There are no events for today!"}


api.add_resource(ExtendResource, "/event/today")
days = {'01': 'Sunday', '02': 'Monday', '03': 'Tuesday', '04': 'Wednesday', '05': 'Thursday', '06': 'Friday', '07': 'Saturday'}
start = datetime.datetime(10, 10, 10)
print(start.strftime("%A"))
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
