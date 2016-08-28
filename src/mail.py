# mail.py
# --coding:utf-8--
import email
import email.header
import email.mime.text
import email.utils
import smtplib

import default
import syntactic_sugar


class Mail(object):

    def __init__(self, config=None):
        self.config = config or default.mail.config
        self.connect()

    def connect(self):
        addresser = self.config.addresser
        password = self.config.password
        smtp_server = self.config.smtp_server
        smtp_port = self.config.smtp_port

        self.server = smtplib.SMTP(smtp_server, smtp_port)
        self.server.starttls()
        self.server.set_debuglevel(1)
        self.server.login(addresser, password)

    def test_connection(self):
        try:
            status = self.server.noop()[0]
        except smtplib.SMTPServerDisconnected:
            status = -1

        return status == 250

    @classmethod
    def _format_addr(cls, addr_arg):
        name, addr = email.utils.parseaddr(addr_arg)
        return email.utils.formataddr((email.header.Header(name, 'utf-8').encode(),
                                       addr.encode('utf-8') if isinstance(addr, unicode) else addr))

    def send(self, content):
        # Batch process, content must have __iter__, and each contatins a set
        # of args.
        for mail in content:
            if isinstance(mail, dict):
                self._send(mail.get('content'), addresser=mail.get(
                    'addresser'), addressee=mail.get('addressee'))
            elif isinstance(mail, list):
                self._send(mail[0], mail[1], mail[2])
            elif isinstance(mail, basestring):
                self._send(mail)

    def _send(self, content, addresser=None, addressee=None):
        addresser = addresser or self.config.addresser
        addressee = addressee or self.config.addressee

        if isinstance(addressee, basestring):
            addressee = [addressee]  # Prevent wrongly split content into chars

        message = email.mime.text.MIMEText(content, 'html', 'utf-8')
        message['From'] = self._format_addr(
            u'Financial Information Assistant <%s>' % addresser)
        message['To'] = self._format_addr(
            u'Subscriber <%s>' % ''.join(addressee))
        message['Subject'] = email.header.Header(
            u'Please read this news', 'utf-8').encode()

        if not self.test_connection():
            self.connect()
        self.server.sendmail(addresser, list(addressee), message.as_string())

    def __del__(self):
        with syntactic_sugar.suppress(AttributeError):
            self.server.quit()


def send(content, send_config):
    if not isinstance(content, list):
        content = [content]  # Prevent wrongly split content into chars

    Mail(send_config).send(list(content))

if __name__ == '__main__':
    raise EnvironmentError("Do Not Directly Run This Script")
