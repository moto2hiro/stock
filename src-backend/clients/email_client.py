import ssl
from flask import render_template
from typing import List, Any
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL
from app_config import app_config
from app_utils.log_utils import LogUtils


class EmailClient:
  def __init__(self) -> None:
    self.__context = ssl.create_default_context()

  def send_html(self, subject: str, template_path: str, model: Any) -> None:
    body: str = render_template(template_path, model=model)
    self.send(subject=subject, body=body, content_type='html')

  def send_plain(self, subject: str, body: str) -> None:
    self.send(subject=subject, body=body, content_type='plain')

  def send(self,
           subject: str,
           body: str,
           content_type: str,
           to: List[str] = app_config.DFLT_EMAIL_TO,
           sender: str = app_config.GMAIL_USERNAME,
           pw: str = app_config.GMAIL_PW,
           server: str = app_config.GMAIL_SERVER,
           port: int = app_config.GMAIL_PORT) -> None:
    try:
      msg: MIMEMultipart = MIMEMultipart()
      msg['From'] = sender
      msg['To'] = ','.join(to)
      msg['Subject'] = '{0}{1}'.format(app_config.EMAIL_SUBJECT_PREFIX, subject)
      msg.attach(MIMEText(body, content_type))

      LogUtils.debug(msg)

      with SMTP_SSL(server, port, context=ssl.create_default_context()) as server:
        server.ehlo()
        server.login(sender, pw)
        server.sendmail(sender, to, msg.as_string())
    except Exception as ex:
      LogUtils.error('EMAIL ERROR!', ex)
