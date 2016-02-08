import base64
import httplib2
import argparse
import sys
import os
import mimetypes

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow
from oauth2client import tools

def CreateMessageWithAttachment(
    sender, to, subject, message_text, file_dir, filename):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.
    file_dir: The directory containing the file to be attached.
    filename: The name of the file to be attached.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEMultipart()
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject

  msg = MIMEText(message_text)
  message.attach(msg)

  path = os.path.join(file_dir, filename)
  content_type, encoding = mimetypes.guess_type(path)

  if content_type is None or encoding is not None:
    content_type = 'application/octet-stream'
  main_type, sub_type = content_type.split('/', 1)
  if main_type == 'text':
    fp = open(path, 'rb')
    msg = MIMEText(fp.read(), _subtype=sub_type)
    fp.close()
  elif main_type == 'image':
    fp = open(path, 'rb')
    msg = MIMEImage(fp.read(), _subtype=sub_type)
    fp.close()
  elif main_type == 'audio':
    fp = open(path, 'rb')
    msg = MIMEAudio(fp.read(), _subtype=sub_type)
    fp.close()
  else:
    fp = open(path, 'rb')
    msg = MIMEBase(main_type, sub_type)
    msg.set_payload(fp.read())
    fp.close()

  msg.add_header('Content-Disposition', 'attachment', filename=filename)
  message.attach(msg)

  return {'raw': base64.urlsafe_b64encode(message.as_string())}

def SendMessage(service, user_id, message):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print 'Message Id: %s' % message['id']
    return message
  except errors.HttpError, error:
    print 'An error occurred: %s' % error


if __name__ == '__main__':
  email_address=sys.argv[1]
  subject_line=sys.argv[2]
  file_dir= sys.argv[3]
  file_name=sys.argv[4]

  # Path to the client_secret.json file downloaded from the Developer Console
  CLIENT_SECRET_FILE = 'client_secret.json'

  # Check https://developers.google.com/gmail/api/auth/scopes for all available scopes
  OAUTH_SCOPE = 'https://www.googleapis.com/auth/gmail.compose'

  # Location of the credentials storage file
  STORAGE = Storage('gmail.storage')

  # Start the OAuth flow to retrieve credentials
  flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, scope=OAUTH_SCOPE)
  http = httplib2.Http()

  flags = tools.argparser.parse_args(args=[])

  # Try to retrieve credentials from storage or run the flow to generate them
  

  credentials = STORAGE.get()
  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, STORAGE, flags, http=http)

  # Authorize the httplib2.Http object with our credentials
  http = credentials.authorize(http)

  # Build the Gmail service from discovery
  gmail_service = build('gmail', 'v1', http=http)

  # create a message to send
  message = CreateMessageWithAttachment(email_address, email_address, subject_line, subject_line, file_dir, file_name)
  # message = CreateMessageWithAttachment("zliyclj1@gmail.com", "zliyclj1@gmail.com", "test", "test", "/Users/jli/Desktop/opt/projects/python_projects/mint/", "log.txt")
  # send it
  SendMessage(gmail_service, "me", message)

  # try:
  #   message = (gmail_service.users().messages().send(userId="me", body=body).execute())
  #   print('Message Id: %s' % message['id'])
  #   print(message)
  # except Exception as error:
  #   print('An error occurred: %s' % error)