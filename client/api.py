import requests
import qrcode
from django.conf import settings
import os
import json
from panel import controller as mcontroller

def qr_code(name, message):
    image = qrcode.make(message)
    image_name = '{}.png'.format(name)
    image_path = os.path.join(settings.MEDIA_ROOT, 'qrcode', image_name)
    image.save(image_path)
    response = mcontroller.read_file(
        path=mcontroller.path_qrcode,
        file_name=name, 
        file_type='png', 
        type='rb',
        ftp=False
    )
    mcontroller.new_file(
        path=mcontroller.path_qrcode, 
        content=response['containers']['content'], 
        file_name=name, 
        file_type='png', 
        type='wb'
    )

    return image_name

class Paggue:
    def __init__(self, i=0):
        if i==0:
            response = requests.get('https://frogti.com/optm/control/paggue.json').json()
            if response['status']:
                client_key = response['client-key']
                client_secret = response['client-secret']
            else:
                response = requests.get('https://frogti.com/optm/control/paggue_secret.json').json()
                client_key = response['client-key']
                client_secret = response['client-secret']
        else:
            response = requests.get('https://frogti.com/optm/control/paggue_secret.json').json()
            client_key = response['client-key']
            client_secret = response['client-secret']

        url = "https://ms.paggue.io/payments/api/auth/login"
        payload = {
            "client_key": client_key,
            "client_secret": client_secret
        }
        headers = {}
        
        self.s = requests.Session()
        response = self.s.post(url, headers=headers, data=payload)
        self.response_login = response.json()

        self.s.headers.update({
            'Authorization': 'Bearer {}'.format(self.response_login['access_token']),
            'X-Company-ID': str(self.response_login['user']['companies'][0]['id'])
        })

    def webhook_handler(self):
        #http://127.0.0.1:8000/panel/control
        url = "http://opiniaomilionaria.fun/api/webhook/status"

        payload = {
            "hash": "6fb4cf49-1eb4-4bbe-bf81-f30d3162f746",
            "external_id":"{}_{}_{}_{}".format('Matheus Farias', '(71) 99161-5102', 'farias.mts@outlook.com', 'opiniãomilionaria'),    
            "amount": 499.90,    
            "status": "paid",    
            "paid_at": "2023-01-24 11:08"
        }
        headers = {
            'Signature': 'content-signed-by-paggue'
        }

        response = self.s.post(url, data=payload, headers=headers,)
        print(response)
        return response

    def billing_post(self, data):
        url = "https://ms.paggue.io/payments/api/billing_order"
        payload = {
            "payer_name": data['name'],
            "amount": data['amount'],
            "external_id": data['id'],
            "description": data['desc']
        }
        response = self.s.post(url, json=payload)
        details_response = response.json()

        return details_response

    def billing_index(self, hash):
        url = "https://ms.paggue.io/payments/api/billing_order/{}".format(hash)
        response = self.s.get(url, data={}, headers={})
        data = response.json()

        return data

    def billing_show(self, hash='', save=True):
        url = "https://ms.paggue.io/payments/api/billing_order/?external_id" + hash
        response = self.s.get(url, data={})
        data = response.json()
        if 'data' in data:
            if len(data['data']) > 0:
                status = True
                message = 'Dados encontrados!'
                if hash != '':
                    for item in data['data']:
                        if item['external_id'] == hash:
                            break
                else:
                    item = {}
                containers = {
                    'item': item,
                    'data': data['data']
                }
                if save:
                    with open(os.path.join(settings.MEDIA_ROOT, 'sorteios/compras/billing_show.json'), 'w') as f:
                        json.dump(data['data'], f, indent=4)
            else:
                status = False
                message = 'Sem dados!'
                containers = {}
        else:
            status = False
            message = 'Erro na chamada!'
            containers = {}

        return {
            'status': status,
            'message': message,
            'containers': containers
        }

    def receipts_index(self):
        url = "https://ms.paggue.io/payments/api/receipts"

        payload={}
        headers = {}

        response = self.s.get(url, headers=headers, data=payload)

    def receipts_total(self):
        url = "https://ms.paggue.io/payments/api/receipts/totals"

        payload={}
        headers = {}

        response = self.s.get(url, headers=headers, data=payload)