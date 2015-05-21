import datetime,logging
import smtplib,mimetypes,os
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.Header import Header
from email import encoders
from email import utils
import util

def response(args,settings):
    if settings.has_key("email_settings"):
        setting = settings.get("email_settings")

        if util.dict_required(setting,["smtp","from","to","password"]):
            smtp = setting.get("smtp")
            fromaddr = setting.get("from")
            toaddr = setting.get("to") 
            password = setting.get("password")

            title = setting.get("title","mwatch response")
            tls = ("True" == setting.get("tls","False"))
            high_priority = ("High" == setting.get("priority","Normal"))
            body = setting.get("body","%s")
            formatter = setting.get("formatter","")
            msg = args

            if len(formatter) > 0 and util.has_module_fun("util",formatter):
                fun = util.get_module_fun("util",formatter)
                msg = fun(args)
            else:
                logging.warn("undefined formatter " + formatter)

            send_mail(smtp,body%(msg),title,fromaddr,password,toaddr,tls,high_priority)

    else:
        logging.error("can not find email setting:%s"%(name))



def send_mail(server,msg,title,fromaddr,passwd,toaddr,tls=False,high_priority=False):
    body=MIMEMultipart()
    body['From'] = fromaddr
    body['To'] = ';'.join(toaddr)
    if high_priority:
        body['X-Priority'] = '2'
    body['Subject'] = Header(title,charset='UTF-8') 
    txt=MIMEText(msg,_subtype='html',_charset='UTF-8')
    body.attach(txt)

    server = smtplib.SMTP(server)
    if tls:
        server.starttls()
    server.login(fromaddr,passwd)
    server.sendmail(fromaddr,toaddr,body.as_string())
    server.quit()
    logging.debug("send email")
