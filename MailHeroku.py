from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient import errors
import email
import base64

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly','https://mail.google.com/']

def get_service():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)


    service = build('gmail', 'v1', credentials=creds)
    return service


def ListMessagesMatchingQueryAndLabelId(service, user_id, query='',label_ids=[]):
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
      try:
        response = service.users().messages().list(userId=user_id,
                                                   q=query,labelIds=label_ids).execute()
        messages = []
        if 'messages' in response:
          messages.extend(response['messages'])

        while 'nextPageToken' in response:
          page_token = response['nextPageToken']
          response = service.users().messages().list(userId=user_id, q=query,
                                             pageToken=page_token).execute()
          messages.extend(response['messages'])
        #for msg in messages:
        #    print(msg)
        return messages
      except errors.HttpError as error:
        print (f'An error occurred: {error}')

def Get_Mime_Message_And_Attachments(service, message,user_id):
  """Get and store attachment from Message with given id.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: ID of Message containing attachment.
    store_dir: The directory used to store attachments.
  """
  try:
  	
    msg_id=message["id"]
   
    message = service.users().messages().get(userId=user_id, id=msg_id).execute()
    #print(message)
    parts = [message['payload']]
    labels=message['labelIds']
    headers=message["payload"]["headers"]

    MailSubject = next((sub for sub in headers if sub['name'] == 'Subject'), "NO Suject")
    MailSubject=MailSubject["value"]

    MailSender = next((sub for sub in headers if sub['name'] == 'From'), None)
    MailSender=MailSender["value"]

    #print(f'Subject :{dir} \n')
    MailSender=" *From :"+MailSender+"*"+"\n\n"
    Subject="*Subject :"+MailSubject+"*"+"\n\n"
    types=type(parts)
    #print(f"Type of parts ={types}")
    flag=1
    text=1
    has_attachments=0
    while parts:
        part = parts.pop()
        if part.get('parts'):
            parts.extend(part['parts'])
        if  part.get('filename'):
            has_attachments=1
            
        elif flag:

            try:
                data=part['body']["data"]
                if text:
                    text=0
                    continue
                msg_str = base64.urlsafe_b64decode(data.encode('ASCII'))
                mime_msg = email.message_from_bytes(msg_str)
                body=str(mime_msg.get_payload())
                #print(body)
                if(has_attachments):
                  body+="\n\n"+"* This mail contain attachments*\n"
                return MailSender,Subject,body
            except Exception as e:
                pass


  except errors.HttpError as error:
    print (f'An error occurred: {error}')

def ModifyMessage(service, user_id, msg_id, msg_labels):
  """Modify the Labels on the given Message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The id of the message required.
    msg_labels: The change in labels.

  Returns:
    Modified message, containing updated labelIds, id and threadId.
  """
  try:

    message = service.users().messages().modify(userId=user_id, id=msg_id,
                                                body=msg_labels).execute()

    label_ids = message['labelIds']
    #print(label_ids)
    #print 'Message ID: %s - With Label IDs %s' % (msg_id, label_ids)
    return message
  except errors.HttpError as error:
     print (f'An error occurred: {error}')





#if __name__ == '__main__':
service=get_service()      
query=""
query+='is:unread'
query+=" AND "+"category:forums "  
query+=" AND "+ " after:06/01/2020"
                                                    #MM/DD/YYYY
messages=ListMessagesMatchingQueryAndLabelId(service,'me', query,label_ids=[])#after:05/20/2020 AND is:unread
    #message=messages[0]
#print()
i=0
msg_labels={'removeLabelIds': ['UNREAD'], 'addLabelIds': []}
TextBody=[]
MailSenderList=[]
MailSubjectList=[]

for message in messages:
  if i > 3:
    break
  i=i+1
  #print(message['id'])
  #print(message)
  ModifyMessage(service,'me', message['id'], msg_labels)
  from_mail,Subject,text=Get_Mime_Message_And_Attachments(service, message,'me')
  TextBody.append(text)
  MailSenderList.append(from_mail)
  MailSubjectList.append(Subject)
        
        
        
        
        
        
        
        
        
     
