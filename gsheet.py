import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials


def open_gsheet(worksheet, sheet ):
	json_key = json.load(open('gmailapi-fba43d945749.json'))
	scope = ['https://spreadsheets.google.com/feeds']
	credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)
	gc = gspread.authorize(credentials)
	wks = gc.open(worksheet)
	worksheet = wks.worksheet(sheet)

	return worksheet


