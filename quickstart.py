from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import readmail, gsheet


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def item_gen(li, key):
    for i in range(0, len(li)):
        yield [li[i].pop(key," ")]





def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    user = "nick.tang@shugie.com.tw"

    worksheet_name = "Prediction Spreadsheet"
    sheet = "Prediction API Worksheet"
    
    query = 'filename:pdf OR filename:jpg OR filename:jpeg OR filename:xlsx'
    mail_attchement = readmail.ListMessagesMatchingQuery(service, user, label_ids='INBOX',query=query, single_page=True)
    # print(mail_attchement)

    mail_ID = readmail.ListMessagesWithLabels(service, user, label_ids='INBOX', single_page=True)
    # print ("attachment %s" %readmail.ListMessagesMatchingQuery(service, user, query=query, single_page=True))
    # print (mail_ID) 

    ids = []

    for i in item_gen(mail_ID,"id"):
        ids.extend(i)

    worksheet = gsheet.open_gsheet(worksheet_name, sheet)
   
    attachment_list = [d['id'] for d in mail_attchement if 'id' in d]
    
    starting_row = 108

    for i in range(0, len(ids)):
        '''
         i is the index
         attachment_list is the list of email's ID which has attachment (jpg,jpeg, pdf and xlsx) 
        '''
        attachment = False
        if ids[i] in attachment_list:
            attachment = True

        msg, size = readmail.GetMessage(service, user, ids[i])
        worksheet.update_cell(i+starting_row, 3, msg) 
        worksheet.update_cell(i+starting_row, 4, size)
        worksheet.update_cell(i+starting_row, 6, attachment)  



    # results = service.users().labels().list(userId='me').execute()
    # labels = results.get('labels', [])

    # if not labels:
    #     print('No labels found.')
    # else:
    #   print('Labels:')
    #   for label in labels:
    #     print(label['name'])


if __name__ == '__main__':
    main()