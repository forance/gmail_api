import base64
import email
from apiclient import errors



"""Get a list of Messages from the user's mailbox.
"""



def ListMessagesMatchingQuery(service, user_id, query='', **kwargs):
  """List all Messages of the user's mailbox matching the query.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    query: String used to filter messages returned.
    Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

  Returns:
    List of Messages that match the criteria of the query. Note that the
    returned list contains Message IDs, you must use get with the
    appropriate ID to get the details of a Message.
  """
  
  single_page = kwargs.pop('single_page', False)

  try:
    response = service.users().messages().list(userId=user_id,
                                               q=query).execute()
    messages = []
    if 'messages' in response:
      messages.extend(response['messages'])

    if not single_page:
      while 'nextPageToken' in response:
        page_token = response['nextPageToken']
        response = service.users().messages().list(userId=user_id, q=query,
                                         pageToken=page_token).execute()
        messages.extend(response['messages'])

    return messages
  except errors.HttpError, error:
    print 'An error occurred: %s' % error


def ListMessagesWithLabels(service, user_id, label_ids=[], **kwargs):
  """List all Messages of the user's mailbox with label_ids applied.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    label_ids: Only return Messages with these labelIds applied.

  Returns:
    List of Messages that have all required Labels applied. Note that the
    returned list contains Message IDs, you must use get with the
    appropriate id to get the details of a Message.
  """
  single_page = kwargs.pop('single_page', False)

  try:
    response = service.users().messages().list(userId=user_id,
                                               labelIds=label_ids).execute()
    messages = []
    if 'messages' in response:
      messages.extend(response['messages'])

    if not single_page:
      while 'nextPageToken' in response:
        page_token = response['nextPageToken']
        response = service.users().messages().list(userId=user_id,
                                                 labelIds=label_ids,
                                                 pageToken=page_token).execute()
        messages.extend(response['messages'])

    return messages
  except errors.HttpError, error:
    print 'An error occurred: %s' % error



def find_valid_body(payload):
  '''
    recursive function to find the message body which is not zero
    in the gmail api, "payload" is dictionary, "body" is dictionary
    "parts" is list

     payload -- body {"data", "size"}
              | 
              -- parts[0] -- body {"data", "size"}
                          |
                          -- parts[0]

  '''
  if payload["body"]["size"] != 0:
    # print 'Message snippet: %s' %base64.urlsafe_b64decode(payload["body"]["data"].encode("utf-8"))
    return payload["body"]["size"] 
  else:
    return find_valid_body(payload["parts"][0])





def GetMessage(service, user_id, msg_id):
  """Get a Message with given ID.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The ID of the Message required.

  Returns:
    A Message.
  """
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id, format='full').execute()
    payload = message['payload']
    # parts = payload['parts']
    # print 'Message snippet: %s' %base64.urlsafe_b64decode(parts[0]["body"]["data"].encode("utf-8"))
    # print 'Message body size: %s' %parts["body"]["size"]
    # print 'Message id: %s' %message["id"]
    # print 'Message id: %s' %message["snippet"]
    # print 'attachment: %s' %len(payload["parts"])
    # for i, d in enumerate(payload["parts"][1]["headers"]):
    #   if "attachment" in d["value"]:
    #     attachment = True

    size = find_valid_body(payload)
    return message['snippet'], size


  except errors.HttpError, error:
    print 'An error occurred: %s' % error


def GetMimeMessage(service, user_id, msg_id):
  """Get a Message and use it to create a MIME Message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The ID of the Message required.

  Returns:
    A MIME Message, consisting of data from Message.
  """
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id,
                                             format='raw').execute()

    print 'Message snippet: %s' % message['snippet']

    msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))

    mime_msg = email.message_from_string(msg_str)

    return mime_msg
  except errors.HttpError, error:
    print 'An error occurred: %s' % error





