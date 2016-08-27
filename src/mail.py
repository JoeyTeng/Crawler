# mail.py
# --coding:utf-8--
import email
import email.header
import email.mime.text
import email.utils
import smtplib

import default


class Mail(object):

    def __init__(self, config=None):
        self.config = config or default.mail.config

    @classmethod
    def _format_addr(cls, addr_arg):
        name, addr = email.utils.parseaddr(addr_arg)
        return email.utils.formataddr((email.header.Header(name, 'utf-8').encode(),
                                       addr.encode('utf-8') if isinstance(addr, unicode) else addr))

    def send(self, content):
        addresser = self.config.addresser
        password = self.config.password
        addressee = self.config.addressee
        smtp_server = self.config.smtp_server
        smtp_port = self.config.smtp_port

        msg = email.mime.text.MIMEText(content, 'plain', 'utf-8')
        msg['From'] = self._format_addr(u'Financial Information Assistant <%s>' %addresser)
        msg['To'] = self._format_addr(u'Subscriber <%s>' %addressee)
        msg['Subject'] = email.header.Header(u'Please read this news', 'utf-8').encode()

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.set_debuglevel(1)
        server.login(addresser, password)
        server.sendmail(addresser, [addressee], msg.as_string())
        server.quit()

def send(content, config_dict):
    _config = config.Config()
    _config.addresser = config_dict['addresser']
    _config.password = config_dict['password']
    _config.addressee = config_dict['addressee']
    _config.smtp_server = config_dict['smtp_server']
    _config.smtp_port = config_dict['smtp_port']

    Mail(_config).send(content)

