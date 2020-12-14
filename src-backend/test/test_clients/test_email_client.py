from test.test_base import TestBase
from app_consts import AppConsts
from clients.email_client import EmailClient


class TestEmailClient(TestBase):

  def __init__(self, *args, **kwargs):
    super(TestEmailClient, self).__init__(*args, **kwargs)
    self.__email_client: EmailClient = EmailClient()

  def test_send_plain_should_complete_successfully(self) -> None:
    # ACT
    self.__email_client.send_plain(subject='my subject', body='my content')
    pass

  def test_send_html_should_complete_successfully(self) -> None:
    # ARRANGE
    model: Dict = {
        'errors': ['errors']
    }

    # ACT
    self.__email_client.send_html(
        subject='my subject',
        template_path='email/delete_prices.html',
        model=model)
    pass
