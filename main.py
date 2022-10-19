import sys
import datetime
from sqlalchemy import create_engine, Column, Integer, VARCHAR, MetaData, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask, jsonify, abort
from flask_restful import Api, Resource, reqparse, inputs, marshal_with, fields


class MyDateFormat(fields.Raw):
    def format(self, value):
        return datetime.datetime.strftime(value, '%Y-%m-%d')


app = Flask('web_calendar')
app.env = "development"
api = Api(app)
parser = reqparse.RequestParser()
parser_get = reqparse.RequestParser()
parser.add_argument('event', type=str, required=True, help="The event name is required!")
parser.add_argument('date', type=inputs.date, required=True, help='The event date with the correct format is required! The correct format is YYYY-MM-DD!')
parser_get.add_argument('start_time', type=str, required=False)
parser_get.add_argument('end_time', type=str, required=False)

engine = create_engine('sqlite:///calendar.db', echo=False)
Base = declarative_base()
calendar_table = {'id': fields.Integer, 'event': fields.String, 'date': MyDateFormat}


def make_session(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


class Calendar(Base):
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True)
    event = Column(VARCHAR, nullable=False)
    date = Column(Date, nullable=False)


metadata = MetaData()
Base.metadata.create_all(engine)


class TodayEvent(Resource):
    @marshal_with(calendar_table)
    def get(self, **kwargs):
        session = make_session(engine)
        today = datetime.datetime.today().date()
        data = session.query(Calendar).filter(Calendar.date == today).all()
        session.close()
        return data


class Event(Resource):

    def post(self):
        args = parser.parse_args()
        session = make_session(engine)
        tuple = Calendar(event=args['event'], date=args['date'])
        session.add(tuple)
        session.commit()
        session.close()
        return {'message': "The event has been added!", 'event': args['event'], 'date': str(args['date'].date())}

    @marshal_with(calendar_table)
    def get(self):
        args = parser_get.parse_args()
        start_time, end_time = args['start_time'], args['end_time']
        session = make_session(engine)
        if start_time and end_time is not None:
            data = session.query(Calendar).filter(Calendar.date.between(start_time, end_time)).all()
        else:
            data = session.query(Calendar).all()
        session.close()
        return data


class EventById(Resource):
    @marshal_with(calendar_table)
    def get(self, id):
        session = make_session(engine)
        event = session.query(Calendar).filter(Calendar.id == id).first()
        session.close()
        if event is None:
            return abort(404, "The event doesn't exist!")
        return event


    def delete(self, id):
        session = make_session(engine)
        event = session.query(Calendar).filter(Calendar.id == id).first()
        if event is None:
            return abort(404, "The event doesn't exist!")
        session.query(Calendar).filter(Calendar.id == id).delete()
        session.commit()
        session.close()
        return jsonify({"message": "The event has been deleted!"})


api.add_resource(TodayEvent, "/event/today")
api.add_resource(Event, '/event')
api.add_resource(EventById, "/event/<int:id>")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run(debug=True)
