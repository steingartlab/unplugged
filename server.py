import json
import logging
import os
from threading import Thread

import flask

from unplugged import constants, controller, docker, initializer, loop

log_filename = "logs/logs.log"
os.makedirs(os.path.dirname(log_filename), exist_ok=True)
logging.basicConfig(
    filename=log_filename,
    level=logging.WARNING,
    format='%(asctime)s: %(message)s'
)


def make_ip(ip_ending) -> str:
    return f'{constants.NETWORK_IP}.{ip_ending}'

initializer.initialize()  # To ensure the GUI starts up properly

app = flask.Flask(__name__)
HOST = make_ip(ip_ending=docker.unplugged.ip_ending)
PORT = docker.unplugged.port

@app.template_filter('tojson')  # Needed for commit() call in index.html
def tojson_filter(value):
    return json.dumps(value)


@app.route('/')
def index():
    return flask.render_template(
        'index.html',
        JIGS=constants.JIGS,
        USERS=constants.USERS,
        STATUS=constants.STATUS,
        META=controller.load_most_recent_meta(),
        TIMESTAMPS=controller.load_most_recent_timestamps(),
        IMAGES=controller.load_most_recent_images()
    )

@app.route('/fruitloops')
def fruitloops():
    thread = Thread(target=loop.doit)
    thread.daemon = True  # This thread dies when main thread (only non-daemon thread) exits.
    thread.start()
    
    return ('I am the captain\nmy name is Dave')

@app.route('/commit', methods=['POST'])
def commit():
    payload = flask.request.json

    controller.write_meta(updated_jigs=payload)

    return 'OK'

@app.route('/<path:filename>')
def get_image(filename):
    return flask.send_from_directory('', filename)


if __name__ == '__main__':
    
    app.run(host=HOST, port=PORT, debug=True)
