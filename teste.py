import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

data = {
  "id": "db0bcbfd-45d6-4240-9b2f-4710330e954f",
  "creation_date": 1692901532001,
  "event": "PURCHASE_APPROVED",
  "version": "2.0.0",
  "data": {
    "product": {
      "id": 0,
      "ucode": "fb056612-bcc6-4217-9e6d-2a5d1110ac2f",
      "name": "Produto test postback2",
      "has_co_production": False
    },
    "affiliates": [
      {
        "affiliate_code": "Q58388177J",
        "name": "Affiliate name"
      }
    ],
    "buyer": {
      "email": "neysa5924@uorak.com",
      "name": "Teste Comprador",
      "checkout_phone": "99999999900"
    },
    "producer": {
      "name": "Producer Test Name"
    },
    "commissions": [
      {
        "value": 149.5,
        "source": "MARKETPLACE",
        "currency_value": "BRL"
      },
      {
        "value": 1350.5,
        "source": "PRODUCER",
        "currency_value": "BRL"
      }
    ],
    "purchase": {
      "approved_date": 1511783346000,
      "full_price": {
        "value": 1500,
        "currency_value": "BRL"
      },
      "original_offer_price": {
        "value": 1500,
        "currency_value": "BRL"
      },
      "price": {
        "value": 1500,
        "currency_value": "BRL"
      },
      "offer": {
        "code": "test"
      },
      "checkout_country": {
        "name": "Brasil",
        "iso": "BR"
      },
      "order_bump": {
        "is_order_bump": True,
        "parent_purchase_transaction": "HP02316330308193"
      },
      "order_date": 1511783344000,
      "status": "APPROVED",
      "transaction": "HP1121336654889",
      "buyer_ip": "00.00.00.00",
      "payment": {
        "installments_number": 12,
        "type": "CREDIT_CARD"
      }
    },
    "subscription": {
      "status": "ACTIVE",
      "plan": {
        "id": 123,
        "name": "plano de teste"
      },
      "subscriber": {
        "code": "I9OT62C3"
      }
    }
  },
  "hottok": "ypwFN5FP6MX0x4wPCKVV0NdhFbkkLR1377d3bb-b62e-43e3-95df-78fd85993967"
}

response = requests.post('http://127.0.0.1:8080/api/webhook/hotmart', json=data)
with open('w.html', 'w') as f:
    f.write(response.text)

'''email = 'nathaniel1994@uorak.com'
password = '123213h21hbni213'
name = 'Carlos Oliveira'
host = '127.0.0.1:8080'

smtp_host = 'smtp-mail.outlook.com'
smtp_port = 587
smtp_email = 'farias.mts@outlook.com'
smtp_password = 'Twelve@2975@0197'

subject = 'Acesso Criado com sucesso!'
body = f"""
Olá {name},

Agradecemos por sua compra em nossa loja! Estamos felizes por tê-lo como parte de nossa comunidade.

Aqui estão os detalhes de sua conta:
E-mail: {email}
Senha: {password}

Você pode acessar sua conta através do seguinte link:
https://{host}/api/login/param/{email}&{password}

Se tiver alguma dúvida ou precisar de ajuda, não hesite em entrar em contato com nossa equipe de suporte.

Esperamos vê-lo em breve em nosso site!
"""

msg = MIMEMultipart()
msg['From'] = smtp_email
msg['To'] = email
msg['Subject'] = subject
msg.attach(MIMEText(body, 'plain'))

server = smtplib.SMTP(smtp_host, smtp_port)
server.ehlo()
server.starttls()
server.login(smtp_email, smtp_password)
server.sendmail(smtp_email, email, msg.as_string())
server.quit()'''