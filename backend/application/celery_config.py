broker_url = "redis://localhost:6379/1" 
result_backend = "redis://localhost:6379/2" 
timezone = "Asia/Kolkata" 
broker_connection_retry_on_startup = True

from celery.schedules import crontab

beat_schedule = {
    "send-daily-reminders": {
        "task": "application.tasks.send_daily_reminders",
        "schedule": crontab(hour=19, minute=10)
    #    "schedule": crontab(minute="*"),  # 7:10 PM every day
    },
    "send-monthly-reports": {
        "task": "application.tasks.send_monthly_reports",
        "schedule": crontab(hour=8, minute=0, day_of_month=1),  # 8:00 AM, 1st day of month
    },
}