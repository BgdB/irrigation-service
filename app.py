import json

import click
import time

from flask import request, Flask
from flask_api import exceptions

from ws_service import ACTIVE_ZONES, DEVICES

app = Flask(__name__)


@app.route('/zone/<zone_id>/on')
def zone_on(zone_id):
    if not int(zone_id) in ACTIVE_ZONES:
        raise exceptions.NotFound()

    print(DEVICES[int(zone_id)])
    return {'message': f'Zone {zone_id} is on.'}


@app.route('/zone/<zone_id>/off')
def zone_off(zone_id):
    if not int(zone_id) in ACTIVE_ZONES:
        raise exceptions.NotFound()

    print(DEVICES[int(zone_id)])
    return {'message': f'Zone {zone_id} is off.'}


@app.route('/zone/<zone_id>/program', methods=['GET', 'POST'])
def schedule(zone_id):
    if not int(zone_id) in ACTIVE_ZONES:
        raise exceptions.NotFound()

    if request.method == 'POST':
        data = request.data
        print(data['frequency'], data['duration'])

    return {'message': f'Zone {zone_id} is programmed.'}


@app.cli.command('run-zone')
@click.argument("zone_id")
@click.argument("duration")
def execute_program(zone_id, duration):
    if not int(zone_id) in ACTIVE_ZONES:
        raise exceptions.NotFound()

    print('on')
    # DEVICES[zone_id].on()
    time.sleep(int(duration))
    # DEVICES[zone_id].off()
    print('off')

    return {'message': f'Zone {zone_id} was running for {duration} seconds.'}


if __name__ == '__main__':
    app.run(debug=True)
