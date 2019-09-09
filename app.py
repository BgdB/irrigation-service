import json

import click
import time

from flask import request, Flask
from flask_api import exceptions

from ws_service import ACTIVE_ZONES, DEVICES
from ws_service.crontab import add_zone_crontab, remove_zone_crontab, get_zone_crontab

app = Flask(__name__)


@app.route('/zone/<zone_id>/on')
def zone_on(zone_id):
    if not int(zone_id) in ACTIVE_ZONES:
        raise exceptions.NotFound()

    DEVICES[int(zone_id)].on()
    return {'message': f'Zone {zone_id} is on.'}


@app.route('/zone/<zone_id>/off')
def zone_off(zone_id):
    if not int(zone_id) in ACTIVE_ZONES:
        raise exceptions.NotFound()

    DEVICES[int(zone_id)].on()
    return {'message': f'Zone {zone_id} is off.'}


@app.route('/zone/<zone_id>/program', methods=['GET', 'POST', 'DELETE'])
def schedule(zone_id):
    if not int(zone_id) in ACTIVE_ZONES:
        raise exceptions.NotFound()
    if request.method == 'GET':
        get_zone_crontab(zone_id)

        return {"zone": str(get_zone_crontab(zone_id))}

    if request.method == 'POST':
        data = json.loads(request.data)
        print(data)
        add_zone_crontab(data['frequency'], zone_id, data['duration'])

        return {'message': f'Zone {zone_id} is programmed.'}

    if request.method == 'DELETE':
        remove_zone_crontab(zone_id)

        return {'message': f'Zone {zone_id} program is deleted.'}


@app.cli.command('run-zone')
@click.argument("zone_id")
@click.argument("duration")
def execute_program(zone_id, duration):
    if not int(zone_id) in ACTIVE_ZONES:
        raise exceptions.NotFound()

    print(f'{zone_id} is on')
    DEVICES[int(zone_id)].on()
    time.sleep(int(duration))
    DEVICES[int(zone_id)].off()

    print(f'{zone_id} is off')

    return {'message': f'Zone {zone_id} was running for {duration} seconds.'}


if __name__ == '__main__':
    app.run(debug=True)
