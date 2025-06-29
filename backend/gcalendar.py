import datetime
from random import randint
import logging

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from classes import Task
from authorize import authorize

# Здесь представлен пример из официальной документации Google. Ничего не трогать!
def add_event(task: Task, **kwargs):
	"""Функция, добавляющая заявку, представленную объектом класса Task, в Google
	Calendar пользователя, который прошел авторизацию.
	"""

	creds = authorize()

	try:
		service = build("calendar", "v3", credentials=creds)

		# Call the Calendar API
		calendars_result = service.calendarList().list().execute().get("items", [])
		calendars = {}
		for calendar in calendars_result:
			calendars[calendar.get('summary')] = calendar.get('id')

		if 'start' in kwargs.keys() and 'end' in kwargs.keys():
			start = datetime.datetime.strptime(start, "%d.%m.%Y %H:%M").isoformat()
			end = datetime.datetime.strptime(end, "%d.%m.%Y %H:%M").isoformat()
		elif 'day' in kwargs.keys():
			start = datetime.datetime.strptime(kwargs['day'], '%d.%m.%Y').isoformat()
			end = (datetime.datetime.strptime(kwargs['day'], '%d.%m.%Y') + datetime.timedelta(days=1)).isoformat()
		services = task.services.split('///')[:-1]

		event = {
			'summary': services[int(kwargs['service_id'])],
			'description': task.format(number=int(kwargs['service_id'])),
			'colorId': str(randint(1, 11)),
			'start': {
				'dateTime': start,
				'timeZone': 'Asia/Tomsk'
			},
			'end': {
				'dateTime': end,
				'timeZone': 'Asia/Tomsk'
			}
		}
		service.events().insert(
			calendarId=calendars['Лапудай'],
			body=event
		).execute()

	except HttpError as error:
		logging.error(f"An error occurred: {error}")

	except KeyError as error:
		logging.error(f"An authorized user don't have calendar 'Лапудай'. Please create this calendar")

if __name__ == "__main__":
	authorize()
