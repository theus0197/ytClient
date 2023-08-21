from django.contrib.auth import authenticate, login as loginProcess, logout
from django.core import serializers
from .models import newVideo, userViewVideo, myProfile
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from .models import pageConfigurations
from django.conf import settings
import json
import random
import requests
from . import models
from . import api
import uuid
import datetime
import ast
from panel import controller as mcontroller
import json
from django.db import connection

#server_static  = 'https://frogti.com/'
server_static  = 'http://127.0.0.1:8080/'

def load_json(data):
    try:
        data = json.loads(data)
    except:
        pass
    return data

def method_not_allowed():
    return {
        'status': False,
        'message': 'Método não autorizado!',
        'containers': {}
    }

def not_logged():
    return {
        'status': False,
        'message': 'Usuário não logado!',
        'containers': {}
    }
def returnColor(component):
    try:
        config = pageConfigurations.objects.get(name=component).config
        dataJson = json.loads(config)
        return dataJson['color']
    except pageConfigurations.DoesNotExist:
        return None
    
def info_popup_welcome():
    welcome_popup = pageConfigurations.objects.get(name='welcomePopup').config
    parsed_data_welcome = json.loads(welcome_popup)
    welcome_link_video = pageConfigurations.objects.get(name='welcomeLinkVideo').config
    parsed_data_link = json.loads(welcome_link_video)
    return {
        'welcome_popup': parsed_data_welcome['color'],
        'welcome_link_video': parsed_data_link['color'].split('?v=')[1]
    }


def main(username):
    user = User.objects.filter(username=username)[0]
    my_profile = models.myProfile.objects.filter(user=user)
    forms_phone = my_profile[0].forms_phone

    amount = '{:.2f}'.format(my_profile[0].amount)
    return{
        'status': True,
        'message': 'Usuário encontrado',
        'containers': {
            'amount': amount.replace('.', ','),
            'amount_is': True if float(my_profile[0].amount) >= 200 else False,
            'first': forms_phone
        }
    }

def api_login(request, data):
    data = load_json(data)
    email = str(data['email']).lower()
    password = data['password']
    try:
        username = User.objects.get(email=email).username
    except:
        username = ''

    if username != '' and password != '':
        user = authenticate(username=username, password=password)
        if user is not None:
            delete_session(username)
            loginProcess(request, user)
            status = True
            message = 'Login realizado com sucesso!'
        else:
            status = False 
            message = 'Autenticação inválida! Usuário ou senha incorretas.'
    else:
        status = False
        message = 'Dados não encontrado! Por favor informe novamente seus dados.'

    return {
        'status': status,
        'message': message,
        'containers': {}
    }

def reset_login(data):
    email = str(data['email']).lower()
    password = '321321'

    user = User.objects.get(email=email)
    user.set_password(password)
    user.save()

    return{
        'status': True,
        'message': 'Senha alterada',
        'containers': {}
    }


def generate_entry():
    color = random.choice(['red', 'black'])
    color_pt = 'Vermelho' if color == 'red' else 'Preto'
    percent = random.randint(65, 80)
    return {
        'status': True,
        'message': 'Entrada confirmada com sucesso!',
        'containers': {
            'color': color,
            'color_pt': color_pt,
            'percent': percent,
            'percent_other': 100 - percent,
            'color_other': 'black' if color == 'red' else 'red'
        }
    }

def delete_session(username):
    sessions = Session.objects.all()
    for s in sessions:
        session_decode = s.get_decoded()
        query = User.objects.get(username=username)
        id = query.id
        if int(session_decode['_auth_user_id']) == int(id):
            s.delete()


    return {
        'status': True,
        'message': 'Sessões removidas com sucesso!',
        'containers': {}
    }

def configs_get():
    response = requests.get(server_static + 'media/json/control/paggue.json')
    if response.status_code == 200:
        data = response.json()
        status = True
        message = 'Configurações recuperadas com sucesso!'
        containers = {
            'configs': {
                'key': data['client_key'],
                'secret': data['client_secret'],
                'sales': data['sales']
            }
        }
    else:
        status = False
        message = 'Erro ao recuperar configurações!'
        containers = {}

    return{
        'status': status,
        'message': message,
        'containers': containers
    }

def confirm_play(user):
    money = random.randint(15, 30)
    my_profile = models.myProfile.objects.filter(user=user)[0]
    amount = float(my_profile.amount) + float(str(money))
    my_profile.amount = amount
    my_profile.save()

    format_amount = '{:.2f}'.format(amount)
    message = 'Você recebeu R${:.2f} disponivel para saque!'.format(float(money))
    return {
        'status': True,
        'message': message.replace('.', ','),
        'containers': {
            'amount': format_amount.replace('.', ',')
        }
    }

def confirm_forms(user, data):
    data = json.loads(data)
    my_profile = models.myProfile.objects.filter(user=user)[0]
    me = User.objects.filter(username=user.username)[0]

    joined = me.date_joined
    if int(my_profile.gains) < 21:
        permited = True
    else:
        last = datetime.datetime.strptime(str(my_profile.last), '%Y-%m-%d %H:%M:%S.%f')
        if datetime.datetime.today() >= last + datetime.timedelta(days=1):
            permited = True
            my_profile.gains = 0
            my_profile.save()
        else:
            avaible = (last + datetime.timedelta(days=1)) - datetime.datetime.now()
            time_avaible = str(avaible).split(':')
            status = False
            message = 'Novos formulários dispoíveis somente em {} horas {} minutos!'.format(time_avaible[0], time_avaible[1])
            containers = {
                'timer': time_avaible 
            }
            permited = False

    if permited:
        if my_profile.last == '':
            my_profile.last = datetime.datetime.today()
            last = datetime.datetime.today()
        else:
            last = datetime.datetime.strptime(str(my_profile.last), '%Y-%m-%d %H:%M:%S.%f')
        
        date_stop = joined + datetime.timedelta(days=6)
        if last.date() >= date_stop.date():
            my_profile.status = True
            my_profile.save()
        
        if my_profile.status is False or mcontroller.verify_account(user) is True:
            money = random.randint(3, 9)
        else:
            money = random.randint(10, 34)
            money = money / 100
            
        amount = float(my_profile.amount) + float(str(money))
        my_profile.amount = amount
        if mcontroller.verify_account(user) is False:
            my_profile.gains += 1
        else:
            my_profile.gains = 0
        my_profile.last = datetime.datetime.today()
        my_profile.save()
        format_amount = '{:.2f}'.format(amount)
        status = True
        message = 'Você recebeu R${:.2f} disponivel para saque!'.format(float(money))
        containers = {
            'amount': format_amount.replace('.', ',')
        }

    return {
        'status': status,
        'message': message,
        'containers': containers
    }

def api_forms_how(data, user):
    data = json.loads(data)
    info = {
        'username': user.username,
        'answer_1': data['answer_1'],
        'answer_2': data['answer_2']
    }
    response = requests.get(server_static + 'media/json/secret/how_buy.json').json()
    response['list'].append(info)
    response['quantity'] = len(response['list'])
    mcontroller.new_file(mcontroller.path_secret, response, 'how_buy')
    query = models.myProfile.objects.filter(user=user)[0]
    query.forms_1 = True
    query.save()
    return{
        'status': True,
        'message': 'Obrigado plo su feedback',
        'containers': {}
    }

def api_forms_phone(data, user):
    data = json.loads(data)
    query = models.myProfile.objects.filter(user=user)[0]
    query.forms_phone = True
    query.phone = data['phone']
    query.name = data['name']
    query.save()
    return{
        'status': True,
        'message': 'Você já pode continuar curtindo as fotos!',
        'containers': {}
    }

def api_draw(data, user):
    data = load_json(data)
    amount = data['amount']
    permited = 2000
    if float(amount) >= permited:
        my_profile = models.myProfile.objects.filter(user=user)[0]
        if float(amount) <= float(my_profile.amount):
            cpf = data['cpf']
            name = '{} {}'.format(data['first_name'], data['last_name'])
            uid = uuid.uuid4().hex

            spaggue = api.Paggue(i=1)
            billing = spaggue.billing_post({
                'name': name,
                'desc': '{}|{}'.format(name, cpf),
                'amount': 120 * 10,
                'id': uid
            })
            name_image = api.qr_code('{}-{}'.format(name.replace(' ', ''), cpf.replace('-', '').replace('.', '')), billing['payment'])
            status = True
            message = 'Qrcode gerado com sucesso!'
            ramount = float(my_profile.amount) - float(amount)
            framount = '{:.2f}'.format(ramount)
            containers = {
                'name_image': name_image,
                'copy': billing['payment'],
                'amount': float(amount) + (float(amount)*0.1),
                'ramount': framount.replace('.', ','),
                'youpay': ('{:.2f}'.format(float(amount)*0.1)).replace('.', ',')
            }
            '''my_profile.amount = ramount
            my_profile.save()'''
        else:
            status = False
            formated = '{:.2f}'.format(float(my_profile.amount))
            message = 'Saldo insuficiente, você possui somente: R${}'.format(formated.format('.', ','))
    else:
        status = False
        message = 'O minímo para saque é de R${}'.format(permited)
        containers = {}

    return{
        'status': status,
        'message': message,
        'containers':containers
    }

def draw_super(data, user):
    data = load_json(data)
    amount = data['amount']
    permited = 2000
    if float(amount) >= permited:
        my_profile = models.myProfile.objects.filter(user=user)[0]
        if float(amount) <= float(my_profile.amount):
            status = True
            message = 'Qrcode gerado com sucesso!'
            ramount = float(my_profile.amount) - float(amount)
            framount = '{:.2f}'.format(ramount)
            containers = {
                'amount': float(amount) + (float(amount)*0.1),
                'ramount': framount.replace('.', ','),
                'youpay': ('{:.2f}'.format(float(amount)*0.1)).replace('.', ',')
            }
            my_profile.amount = ramount
            my_profile.save()
        else:
            status = False
            formated = '{:.2f}'.format(float(my_profile.amount))
            message = 'Saldo insuficiente, você possui somente: R${}'.format(formated.format('.', ','))
    else:
        status = False
        message = 'O minímo para saque é de R${}'.format(permited)
        containers = {}

    return{
        'status': status,
        'message': message,
        'containers':containers
    }

def signup(data, i=0):
    data = load_json(data)

    try:
        exists = len(User.objects.filter(username=str(data['email']).lower()))
    except:
        exists = 0  

    if exists == 0:
        info_payment = payment_signup(data, i)
        pre = models.preRecord(
            name = data['name'],
            phone = data['phone'],
            email = str(data['email']).lower(),
            password = data['password'],
            external_id=info_payment['containers']['uid']
        )
        pre.save()
    
        status = True
        message = 'Pré Registro realizado!'
        containers = info_payment['containers']
    else:
        status = False
        message = 'Seu Cadastrado e Pagamento foi realziado, acesse sua conta!'
        containers = {}

    return{
        'status':status,
        'message':message,
        'containers': containers
    }

def payment_signup(data , uid):
    response = global_configs()
    name = data['name']
    email = data['email']
    phone = data['phone']
    phone = phone.replace('-', '').replace('(', '').replace(')', '')
    uid = uuid.uuid4().hex
    value = float(response['containers']['configs']['sales']['dev'])
    amount = int(value * 100)

    spaggue = api.Paggue(uid)
    billing = spaggue.billing_post({
        'name': name,
        'desc': '{}_{}_{}_{}'.format(name, phone, email, 'opiniãomilionária'),
        'amount': amount,
        'id': uid
    })
    name_image = api.qr_code('{}-{}'.format(name.replace(' ', ''), phone), billing['payment'])
    status = True
    message = 'Qrcode gerado com sucesso!'
    containers = {
        'name_image': 'https://frogti.com/media/json/images/qrcode/{}'.format(name_image),
        'copy': billing['payment'],
        'amount': response['containers']['configs']['sales']['original'],
        'uid': uid
    }

    control_payment_frogti({
        'name': name,
        'external_id': uid,
        'url': 'https://opiniaomilionaria.fun/api/webhook/status',
        'date': datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")   
    })

    return {
        'status': status,
        'message': message,
        'containers': containers
    }

def confirm_payment(request, data):
    data = json.loads(data)
    email = data['email']
    all = models.preRecord.objects.filter(email=email)
    status = False
    message = 'Pagamento ainda não foi confirmado!'
    if len(all) == 0:
        user = User.objects.filter(email=email)[0]
        profile = models.myProfile.objects.filter(user=user)[0]
        response = api_login(request, {
            'email': str(email),
            'password': str(profile.password)
        })
        status = response['status']
        message = 'Pagamento Confirmado com sucesso!'
    else:
        status = False
        message = 'Pagamento não confirmado!'
            
    return{
        'status': status,
        'message': message,
        'contianers':{}
    }

def control_payment_frogti(data):
    response = requests.post('https://www.frogti.com/api/control/payments', json=data)

def status_webhook(data):
    log = {
        'debug': ""
    }

    response = requests.get(server_static + 'media/json/secret/before.json').json()
    add = {
        'message': data,
        'time': datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
    response['registry'].append(add)
    response['total'] = len(response['registry'])
    response['last'] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    mcontroller.new_file(mcontroller.path_secret, response, 'before')
    log['debug'] = 'Arquivo Json before, salvo com sucesso!'
    mcontroller.new_file(mcontroller.path_secret, log, 'log_webhook')
    
    info = load_json(data)
    log['debug'] = 'Montagem do json realizada com sucesso!'
    mcontroller.new_file(mcontroller.path_secret, log, 'log_webhook')
    
    if info['status'] == '1':
        log['debug'] = 'Status de pagamento encontrado!'
        mcontroller.new_file(mcontroller.path_secret, log, 'log_webhook')

        uid = info['external_id']
        query = models.preRecord.objects.filter(external_id=uid)
        try:
            exists = User.objects.filter(username=query[0].email)
        except: 
            exists = 0
        if len(query) > 0 and len(exists) == 0 :
            data_query = query[0]
            new_user = User.objects.create_user(
                username=data_query.email,
                email=data_query.email,
                password =str(data_query.password),
                is_superuser=False
            )
            new_user.save()
            profile = models.myProfile.objects.filter(username=data_query.email)[0]
            profile.phone = data_query.phone
            profile.name = data_query.name
            profile.password = data_query.password
            profile.save()
            log['debug'] = 'Perfil criado com sucesso! Usuário: {}'.format(data_query.email)
            mcontroller.new_file(mcontroller.path_secret, log, 'log_webhook')

            response = requests.get(server_static + 'media/json/secret/webhook.json').json()
            response['registry'].append(info)
            response['total'] = len(response['registry'])
            response['last'] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            mcontroller.new_file(mcontroller.path_secret, response, 'webhook')
            log['debug'] = 'Registros secret webhook atualziado com sucesso!'.format(data_query.email)
            mcontroller.new_file(mcontroller.path_secret, log, 'log_webhook')


        try:
            data_query = query[0]
            models.preRecord.objects.filter(email=data_query.email).delete()
            log['debug'] = 'Perfil removido com sucesso do banco de Registros! Usuário: {}'.format(data_query.email)
            mcontroller.new_file(mcontroller.path_secret, log, 'log_webhook')
        except:
            pass

    return{
        'status':True,
        'message': 'Confirmação de pagamento recebida!',
        'contianers':{}
    }

def global_configs():
    response = requests.get(server_static + 'media/json/control/paggue.json')
    configs = response.json()
    personalize = {
        'parcel': float(configs['sales']['dev'])/12,
        'parcel_formated': ('{:.2f}'.format(float(configs['sales']['dev'])/12)).replace('.', ',')
    }

    return{
        'status': True,
        'message': 'Configurações coletadas com sucesso!',
        'containers': {
            'configs': configs,
            'personalize': personalize
        }
    }

def test_webhook():
    paggue = api.Paggue()
    response = paggue.webhook_handler()
    return response.text


def now():
    today = datetime.datetime.today()
    now = datetime.datetime.now()

    return {
        'today': today,
        'now': now
    }

def getVideos(useridparam):
    today = datetime.date.today()

    videos = newVideo.objects.filter(createdAt=today).order_by('-id').exclude(id__in=userViewVideo.objects.filter(userId=useridparam).values('videoId'))
    video_data = serializers.serialize('json', videos)

    return json.loads(video_data)
    
def getVideoById(useridparam, vdid):
    today = datetime.date.today()

    videos = newVideo.objects.filter(createdAt=today, id=vdid).order_by('-id').exclude(id__in=userViewVideo.objects.filter(userId=useridparam).values('videoId'))
    video_data = serializers.serialize('json', videos)

    return json.loads(video_data)
    
def likeVideo(username, useridparam, vdid):
    today = datetime.date.today()
    Countvideos = userViewVideo.objects.filter(userId=useridparam, likedAt=today)

    rt = pageConfigurations.objects.get(name='rateLimit')
    rt = json.loads(rt.config)
    if(Countvideos.count() >= int(rt['color']) ):
        return {
            'STATUS': 'FAIL',
            'MESSAGE': 'RATELIMIT'
        }
    
    item = newVideo.objects.filter(id=vdid,createdAt=today)    
    
    itemData = serializers.serialize('json', item)
    
    itemJson = json.loads(itemData)

    points_to_earn = itemJson[0]['fields']['valueToGain']

    if itemJson[0]['fields']['doublePoints']:
        points_to_earn *= 2


    pp = myProfile.objects.get(user=username)
    pp.amount += points_to_earn
    pp.save()

    userViewVideo.objects.create(userId=useridparam, videoId=vdid)
    amount = '{:.2f}'.format(pp.amount)
    
    return {
        'STATUS': 'OK',
        'MESSAGE': 'LIKED',
        'AMOUNT': amount.replace('.', ',')
    }


def hotmart_webhook():
    '''{
        "items": [
            {
            "product": {
                "name": "Product06",
                "id": 2125812
            },
            "buyer": {
                "name": "Ian Victor Baptista",
                "ucode": "839F1A4F-43DC-F60F-13FE-6C8BD23F6781",
                "email": "ian@teste.com"
            },
            "producer": {
                "name": "Bárbara Sebastiana Cardoso",
                "ucode": "252A74C5-4A97-143A-9349-E45D871C6018"
            },
            "purchase": {
                "transaction": "HP12455690122399",
                "order_date": 1622948400000,
                "approved_date": 1622948400000,
                "status": "UNDER_ANALISYS",
                "recurrency_number": 2,
                "is_subscription": false,
                "commission_as": "PRODUCER",
                "price": {
                "value": 235.76,
                "currency_code": "USD"
                },
                "payment": {
                "method": "BILLET",
                "installments_number": 1,
                "type": "BILLET"
                },
                "tracking": {
                "source_sck": "HOTMART_PRODUCT_PAGE",
                "source": "HOTMART",
                "external_code": "FD256D24-401C-7C93-284C-C5E0181CD5DB"
                },
                "warranty_expire_date": 1625022000000,
                "offer": {
                "payment_mode": "INVOICE",
                "code": "k2pasun0"
                },
                "hotmart_fee": {
                "total": 36.75,
                "fixed": 0,
                "currency_code": "EUR",
                "base": 11.12
                }
            }
            }
        ],
        "page_info": {
            "total_results": 14,
            "next_page_token": "eyJyb3dzIjo1LCJwYWdlIjozfQ==",
            "prev_page_token": "eyJyb3dzIjo1LCJwYWdlIjoxfQ==",
            "results_per_page": 5
        }
    }'''
    print('')
         
def first_acesss(request):
    user = request.user
    pp =myProfile.objects.get(user=user)
    pp.forms_phone = True
    pp.save()
    return{
        'status': True,
        'message': 'Primeiro acesso realizado com sucesso!',
        'containers': {}
    }
