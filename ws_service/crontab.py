from crontab import CronTab

cron = CronTab(user=True)
CRONTAB_COMAND = '/home/pi/sites/irrigation-service/run-zone.sh'


def get_zone_crontab(zone):
    for job in cron.lines:
        if f'{CRONTAB_COMAND} {zone}' in str(job):
            return job


def remove_zone_crontab(zone):
    for job in cron:
        if f'{CRONTAB_COMAND} {zone}' in str(job):
            print(f'delete command {job}')
            cron.remove(job)
            cron.write()


def add_zone_crontab(frequency, zone, duration):
    remove_zone_crontab(zone)

    parameters_as_string = f' {zone} {duration}'
    print(CRONTAB_COMAND + parameters_as_string)

    job = cron.new(command='flask run-zone' + parameters_as_string)
    job.setall(frequency)

    cron.write()
