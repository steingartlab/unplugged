from dataclasses import dataclass
import json
import logging

from flask import Flask, request, render_template, jsonify
import requests

import config
import utils


@dataclass
class Server:
    zerotier_base_ip: str
    local_ip: str
    port: int
    remote_ip_endings: list[int]
    controller_port: int


server: Server = utils.dataclass_from_dict(dataclass_=Server, dict_=config.config)
app = Flask(__name__)


def make_url(ip_ending: str, endpoint: str) -> str:
    return f'http://{server.zerotier_base_ip}.{ip_ending}:{server.controller_port}/{endpoint}'


def execute(endpoint: str):
    exp_params: dict = request.get_json()
    logging.info(exp_params)
    url = make_url(ip_ending=config.machines[exp_params['jig']], endpoint=endpoint)
    print(exp_params)
    print(url)
    response = requests.post(url=url, data=exp_params).text
    
    return response


@app.route('/')
def index():
    return render_template('index.html', jigs=config.machines.keys())


@app.route('/pulse', methods=['POST'])
def get_wave():
    return execute(endpoint=config.endpoints['single pulse'])


@app.route('/start', methods=['POST'])
def calculate():
    return execute(endpoint=config.endpoints['run experiment'])


@app.route('/status', methods=['POST'])
def status():
    jig = request.get_json()
    url = make_url(
        ip_ending=config.machines[jig],
        endpoint=config.endpoints['get jig status']
    )
    response = requests.get(url=url).text
    return json.dumps({'status': config.jig_status[response]})


if __name__ == '__main__':
    app.run(host=server.local_ip, port=server.port, debug=True)