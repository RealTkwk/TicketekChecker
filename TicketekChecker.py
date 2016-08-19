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
        server.sendmail(sender, [to], body)
    except SMTPException:
        server.quit()
        return False

    server.quit()
    return True


def log(msg):
    print('[{}] {}'.format(strftime("%H:%M:%S", localtime()), msg))


if __name__ == '__main__':

    runs = 1

    emma, emma_pwd, mail_to, tktk_url, freq = load_settings('settings.cfg')

    while True:
        start = time()

        r = requests.get(tktk_url)

        if 'artists-list-item-title' in r.text:
            runtime = time() - start

            log('Finally something on run {}. {:.2f}s'.format(runs, runtime))

            if send_mail(emma, emma_pwd, mail_to, 'Partido de tenis!',
                         'Aparecio un partido!!\nwww.ticketeck.com.ar/tenis \nNinos!'):
                log('Email sent on run {}. {:.2f}s'.format(runs, runtime))
                break
        else:
            runtime = time() - start
            log('Nothing new on run {}. {:.2f}s'.format(runs, runtime))

        runs += 1
        sleep(int(freq) * 3600 - runtime)
