import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Области доступа. Данная позволяет взаимодействовать с календарем
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def authorize():
	creds = None
	# Файл token.json хранит пользовательские токены для доступа и обновления.
	# Он создается автоматически, когда завершается авторизация в первый раз.
	if os.path.exists("./config/token.json"):
		creds = Credentials.from_authorized_user_file("./config/token.json", SCOPES)
  	# Если нет валидных реквизитов для входа, то пользователь должен войти в аккаунт
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
				"./config/credentials.json", SCOPES
			)
			creds = flow.run_local_server(port=0)
		# Save the credentials for the next run
		with open("./config/token.json", "w") as token:
			token.write(creds.to_json())
	
	return creds