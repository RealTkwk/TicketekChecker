import re
import smtplib
import requests
from smtplib import SMTPException
from time import strftime, localtime, time, sleep


def load_settings(archivo):
    with open(archivo, 'r') as f:
        info = f.read().splitlines()
        sender, pwd, to, url, chk = info

        return sender, pwd, to, url, chk


def send_mail(sender, pwd, to, subject, text):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(sender, pwd)

    body = '\r\n'.join(['To: %s' % to,
                        'From: %s' % sender,
                        'Subject: %s' % subject,
                        '', text])

    try:
        server.sendmail(sender, to, body)
    except SMTPException:
        server.quit()
        return False

    server.quit()
    return True


def log(msg):
    print('[{}] {}'.format(strftime("%H:%M:%S", localtime()), msg))


if __name__ == '__main__':

    runs = 1

    emma, emma_pwd, recipients, tktk_url, freq = load_settings('settings.cfg')

    mail_to = recipients.split(",")

    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5)",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "accept-charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
        "accept-encoding": "gzip,deflate,sdch",
        "accept-language": "en-US,en;q=0.8",
    }

    events = re.compile(
        r'<a href=\"(?P<link>.*)\" title=\"(?P<nombre_int>.*)\" class=\"(?P<evento>artists-list-item-title)\">(?P<nombre_ext>.*)<\/a>',
        re.I | re.M)

    while True:
        start = time()

        r = requests.get(tktk_url, headers=headers)

        scraped = events.findall(r.text)

        if scraped:

            with open('past events.txt', 'r+')as f:
                past_events = f.read()
                for event in scraped:
                    if str(event) not in past_events:
                        if send_mail(emma, emma_pwd, mail_to, 'Evento de tenis nuevo: {}'.format(event[3]),
                                     '\nAparecio un partido!!\n\nwww.ticketek.com.ar{}/'.format(event[0])):
                            log('Email sent on run {}.'.format(runs))
                        f.write(str(event))
        else:
            log('Nothing new on run {}.'.format(runs))

        runs += 1
        sleep(int(freq) * 3600)
