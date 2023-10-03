
from django.core.mail import send_mail as core_send_mail
from django.core.mail import EmailMultiAlternatives
import threading
import requests

class EmailThread(threading.Thread):
    def __init__(self, subject, body, from_email, recipient_list, fail_silently, html):
        self.subject = subject
        self.body = body
        self.recipient_list = recipient_list
        self.from_email = from_email
        self.fail_silently = fail_silently
        self.html = html
        threading.Thread.__init__(self)

        print("EMAILLLLLLLLLLL %s /////////// %s" % (recipient_list,from_email))

    def run (self):
        msg = EmailMultiAlternatives(self.subject, self.body, self.from_email, self.recipient_list)
        if self.html:
            msg.attach_alternative(self.html, "text/html")
        msg.send(self.fail_silently)

def send_async_mail(subject, message,texte,url,recipient_list, fail_silently = False):

        from_email = 'noreply@hodari.cd'

        print("DEBUT MAILLLLLLLLLLLLLLLLLLLLLLL")

        html_message =  '<!doctype html><html><head><meta name="viewport" content="initial-scale=1.0, user-scalable=no"><meta charset="utf-8">'
        html_message = html_message + '<style>html, body, * {height: 100%;margin: 0;padding: 0; box-sizing: border-box; font-family: "Trebuchet MS", sans-serif;  font-size: 14px;}'
        html_message = html_message + ' head {display: none;} .grid {display: block; position: relative; margin: .625rem 0;}'
        html_message = html_message + ' .grid .row:last-child {margin-bottom: 0;}'
        html_message = html_message + ' .grid .row {width: 100%; display: block; margin: 0 0 2.12765% 0;}'
        html_message = html_message + ' .grid .row.cells3 > .cell.colspan2 {width: 65.95745%;} '
        html_message = html_message + ' .grid .row > .cell:first-child {margin-left: 0;} .grid .row > .cell {display: block; float: left; min-height: 10px;}'
        html_message = html_message + ' .padding40 {padding: 2.5rem;} p {display: block; -webkit-margin-before: 1em; -webkit-margin-after: 1em;}'
        html_message = html_message + ' .danger, .button.alert {background: #ce352c; color: #ffffff; border-color: #ce352c;}'
        html_message = html_message + ' a.button {padding-top: .53125rem;} a:visited {color: #2086bf;}'
        html_message = html_message + ' .button {padding: 0 1rem; height: 2.125rem; text-align: center; vertical-align: middle;'
        html_message = html_message + ' border: 1px #d9d9d9 solid; cursor: pointer; display: inline-block; outline: none; font-size: .875rem;'
        html_message = html_message + ' line-height: 100%; margin: .15625rem 0; position: relative; } a {text-decoration: none;}</style>'
        html_message = html_message + '</head><body>'
        html_message = html_message + '<div class="grid"><div class="row cells3"><div class="cell colspan2 padding40"><p style="font-size:13px">'
        html_message = html_message + '<h2>Hodari</h2> <br>'
        html_message = html_message + texte + " <br><br>"
        
        #html_message = html_message + 'Veuillez vous authentifier et vous diriger vers ce <a href="http://app.amanilf.cd'+ url +'">lien</a>'
        #html_message = html_message + " pour plus de detail. <br><br>"
        html_message = html_message + "</p></div></div></div></body></html>"

        email = recipient_list
        recipient_list = []
        recipient_list.append(email)
        recipient_list.append("chanyngoy@gmail.com")

        EmailThread(subject, message, from_email, recipient_list, fail_silently, html_message).start()

        print("SENTTTTTTTTTTTTTTTTTTTT MAILLLLLLLLLLLLLLLLLL")


def send_whatsapp(phones, texte):
    token = ""
    instance = ""
    for number in phones:
        r = requests.post( "https://api.chat-api.com/instance"+ instance +"/sendMessage?token="+ token , headers={'Content-Type' :'application/json'}
            ,json={
                    "phone": number.phone,
                    "body": texte
                    })

        result = r.json()

        print("RESULTTTTTTTTTTTTTTTTT %s" % result)

