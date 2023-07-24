from crontab import CronTab


def add_cron_job(schedule, command):

    cron = CronTab(user=True)

    job = cron.new(command=command)
    job.setall(schedule)

    cron.write()


def remove_cron_job():
    pass
