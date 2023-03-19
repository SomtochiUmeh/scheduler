from taskscheduler import TaskScheduler
from prepare_tasks import to_do_tasks
import datetime

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/calendar']

creds = Credentials.from_authorized_user_file('token.json', SCOPES)
service = build('calendar', 'v3', credentials=creds)

my_schedule = TaskScheduler(to_do_tasks)
start = 4*60

tasks = my_schedule.dp_run_task_scheduler(start, will_print=False)[0]


def format_time(time):
    """
    Formats given time (in minutes) to a string showing hours and minutes (time in the day)

    Parameters
    ----------
    time : int/float
    time (in minutes) to be formatted

    Returns
    ----------
    str
    a string representation of the time in the day

    """
    return f"{int(time//60):02d}:{round(int(time%60), 2):02d}:00"


print([(task.description, task.duration) for task in tasks])

current_time = start

for id, task in enumerate(tasks):
    print(task.description, format_time(current_time))

    event = {
        'summary': f'{id+1}: {task.description}',
        'description': f'{task.description}',
        'start': {
            'dateTime': f'2023-03-18T{format_time(current_time)}+05:30',
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': f'2023-03-18T{format_time(current_time+task.duration)}+05:30',
            'timeZone': 'America/Los_Angeles',
        },
        'attendees': [
            {'email': 'njeri.mwenjwa@uni.minerva.edu'},
            {'email': 'somtochiumeh@uni.minerva.edu'},
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()

    current_time += task.duration

print('Event created: %s' % (event.get('htmlLink')))
