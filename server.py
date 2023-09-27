import json
import logging

from flask import Flask, request, render_template
import requests

NETWORK_IP = '0.0.0'

with open('docker.json', 'r') as json_file:
    containers = json.load(json_file)


def make_ip(ip_ending) -> str:
    return f'{NETWORK_IP}.{ip_ending}'


HOST = make_ip(ip_ending=containers['unplugged']['ip'])
PORT = containers['unplugged']['port']
URL = f"http://10.251.67.179:{containers['remotecontrol']['port']}"

JIGS = (
    'pikachu',
    'snorlax',
    'charmander',
    'bulbasaur',
    'clefairy'
)

app = Flask(__name__)


def make_url(endpoint: str) -> str:
    return f'{URL}/{endpoint}'


def execute(endpoint: str):
    exp_params: dict = request.get_json()
    logging.info(exp_params)
    url = make_url(endpoint=endpoint)

    return requests.post(url=url, data=exp_params).text


@app.route('/')
def index():
    return render_template('index.html', jigs=JIGS)


@app.route('/pulse', methods=['POST'])
def pulse():
    return execute(endpoint='pulser')


@app.route('/start', methods=['POST'])
def start():
    return execute(endpoint='start')


@app.route('/status', methods=['POST'])
def status():
    jig = request.get_json()
    print(jig)
    response = requests.post(url=URL, data=jig).text
    
    return json.dumps({'status': response})


@app.route('/stop', methods=['POST'])
def stop():
    jig = request.get_json()
    response = requests.post(url=URL, data=jig).text
    
    return json.dumps({'status': response})


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)