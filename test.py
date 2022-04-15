import requests
from flask import Flask, render_template, request, make_response, jsonify


app = Flask('app')


@app.route('/<name>/')
def index(name):
    return 'Hi, from Flaks ' + name


@app.route('/<name>/<position>/')
def render_something(name, position):
    return f'This is my {name} and pos {position}'


def google_request(query, result_num):
    req = requests.get('https://google.com/search', params={'q': query, 'num': result_num})
    print(req.content)
    print(req.url)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        template = """
        <form method='POST'>
        <input type='text' placeholder='Username...'>
        <input type='password' placeholder='Password...'>
        <input type='submit' value='Auth'>
        </form>
        """
        return template
    elif request.method == 'POST':
        return 'You are logged in'


@app.route('/error')
def error_page():
    response = make_response("<h1>Here is an error occured</h1>", 400)
    return response


@app.route('/json')
def json_page():
    response = jsonify({'first': 'value_1', "second": "value_2"})
    return response

app.run(debug=True)
