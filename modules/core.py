import smtplib
import imaplib
import email
import ssl

providers = [
  'txt.att.net', 'mms.att.net', 'sms.myboostmobile.com', 'myboostmobile.com',
  'cspire1.com', 'sms.cricketwireless.net', 'mms.cricketwireless.net',
  'mailmymobile.net', 'msg.fi.google.com', 'mymetropcs.com',
  'mailmymobile.net', 'vtext.com', 'mypixmessages.com',
  'text.republicwireless.com', 'messaging.sprintpcs.com', 'pm.sprint.com',
  'vtext.com', 'mypixmessages.com', 'tmomail.net', 'message.ting.com',
  'mmst5.tracfone.com', 'email.uscc.net', 'mms.uscc.net', 'vtext.com',
  'vzwpix.com', 'vmobl.com', 'vmpix.com', 'vtext.com', 'mypixmessages.com'
]


class SMS_Handler:

  def __init__(self, email_, name, password):
    self.email_ = email_
    self.name = name
    self.password = password

  def setup(self):
    email_receiver = imaplib.IMAP4_SSL('imap.gmail.com')
    email_receiver.login(self.email_, self.password)
    email_receiver.select('inbox')
    self.email_receiver = email_receiver

    email_sender = smtplib.SMTP('smtp.gmail.com')
    email_sender.starttls(context=ssl.create_default_context())
    email_sender.login(self.email_, self.password)
    self.email_sender = email_sender

  def send_text(self, phone_number: str, receiver_name, subject, content):
    receiver = phone_number + "@vtext.com"
    message = f"""From: {self.name} <{self.email_}>
To: {receiver_name} {receiver}
Subject: {subject}
  
{content}"""
    try:
      self.email_sender.sendmail(self.email_, [receiver], message)
      return True
    except Exception as e:
      print("Failed to send email")
      print(e)
      return False

  def get_texts(self, num: int = 10):
    emails = []
    self.email_receiver.select('inbox')
    status, data = self.email_receiver.search(None, 'ALL')
    mail_ids = []
    for block in data:
      mail_ids += block.split()

    for i in mail_ids[:len(mail_ids) - num:-1]:
      status, data = self.email_receiver.fetch(i, '(RFC822)')
      for response_part in data:
        if isinstance(response_part, tuple):
          message = email.message_from_bytes(response_part[1])

          mail_from = message['from']
          mail_subject = message['subject']

          if message.is_multipart():
            mail_content = ''

            for part in message.get_payload():

              if part.get_content_type() == 'text/plain':
                mail_content += part.get_payload()
          else:
            mail_content = message.get_payload()

          emails.append({
            "from": mail_from,
            "subject": mail_subject,
            "content": mail_content
          })
    to_return = []
    for email__ in emails:
      if email__["from"].lower().split("@")[1] in providers:
        to_return.append(email__)
    return to_return


def print_dict(dictionary, pre=""):
  for k, v in dictionary.items():
    if type(v) == dict:
      print(pre + k + ": ")
      print_dict(v, pre=pre + "    ")
    elif type(v) == list:
      print(pre + k + ": [")
      for item in v:
        if type(item) == dict:
          print_dict(item, pre=pre + "    ")
        else:
          print(pre + "    " + item)
      print(pre + "]")
    else:
      print(pre + k + ": " + str(v))
