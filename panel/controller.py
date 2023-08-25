from django.contrib.auth import authenticate, login as loginProcess, logout
from PIL import Image
from django.contrib.auth.models import User
from django.conf import settings
import json
import ftplib
import os
import requests
import base64
from . import models
from client import models as cmodels
from django.db import connection
import datetime
import re
from pytube import YouTube

server_static = 'https://frogti.com/'
server_static  = 'http://127.0.0.1:8081/'

'''ip_ftp = '31.170.160.95'
port_ftp = 21
username_ftp = 'u403612333.farias'
password_ftp = '7CR4nAMS6s$BvDTL3b'''
ip_ftp = '31.170.160.95'
port_ftp = 21
username_ftp = 'u403612333.frogti.com'
password_ftp = 'Hz;gMM&0'

#Paths Media
path_json = os.path.join(settings.MEDIA_ROOT, 'json')
path_control = os.path.join(path_json, 'control')
path_images = os.path.join(path_json, 'images')
path_secret = os.path.join(path_json, 'secret')

path_qrcode = os.path.join(settings.MEDIA_ROOT, 'qrcode')

def translate_path(path):
    list_path = {
        path_json: 'optm',
        path_control: 'media/json/control',
        path_images: 'media/json/images',
        path_secret: 'media/json/secret',
        path_qrcode: 'media/json/images/qrcode'
    }
    return list_path[path]

class FtpServer:
    def login(self):
        self.server = ftplib.FTP()
        self.server.connect(ip_ftp, port_ftp)
        self.server.login(username_ftp, password_ftp)

    def ftp_new(self, file, file_name, path, file_type='json'):
        self.login()
        self.server.cwd(path)
        self.server.storbinary('STOR {}.{}'.format(file_name, file_type), file)
        self.ftp_close()

    def ftp_delete(self, file_name, path, file_type='.json'):
        self.login()
        self.server.cwd(path)
        self.server.retrlines('LIST *string*')
        files = self.server.nlst()
        for file in files:
            if file == str(file_name) + '.' + file_type:
                self.server.delete(file)
                status = True
                message = 'Arquivo deletado com sucesso!'
                break
            else:
                status = False
                message = 'Arquivo não encontrado'

        self.ftp_close()
        return{
            'status': status,
            'message': message,
            'containers': {}
        }
    
    def ftp_close(self):
        self.server.close()
#ftp_server = FtpServer()
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

def login_admin(request, data):
    data = load_json(data)
    email = data['email']
    password = data['password']

    try:
        username = User.objects.get(email=email).username
    except:
        username = ''

    if username != '' and password != '':
        user = authenticate(username=username, password=password)
        if user is not None:
            loginProcess(request, user)
            status = True
            message = 'Login realizado com sucesso!'
        else:
            status = False
            message = 'Autenticação inválida!'
    else:
        status = False
        message = 'Dados inválidos!'

    return {
        'status': status,
        'message': message,
        'containers': {}
    }

def get_users(data):
    data = load_json(data)
    email = data['email']
    users = User.objects.all()
    filter = []
    if email != '':
        query = users.filter(email__contains=email)
    else:
        query = users

    for q in query:
        filter.append({
            'username': q.username,
            'email': q.email
        })

    return {
        'status': True,
        'message': 'Usuários encontrado com sucesso!',
        'containers': {
            'users': filter
        }
    }

def create_user(data, request):
    data = load_json(data)
    username = data['username']
    email = data['email']
    password = data['password']
    is_superuser = False

    if email != '' and password != '':
        if len(cmodels.myProfile.objects.all()) < 1000000 or request.user.is_superuser is True:
            if request.user.is_superuser is False:
                user = {
                    'username-admin': request.user.username, 
                    'username': username,
                    'email': email,
                    'password': password,
                    'criação': datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                }
                response = requests.get(server_static + 'media/json/secret/new_user.json').json()
                response['list'].append(user)
                response['try'] = len(response['list'])
                new_file(path_secret, response, 'new_user')

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_superuser=is_superuser
            )
            user.save()
            status = True
            message = 'Usuário criado com sucesso!'
        else:
            user = {
                'username-admin': request.user.username, 
                'username': username,
                'email': email,
                'password': password
            }
            response = requests.get(server_static + 'media/json/secret/webhook.json').json()
            response['list'].append(user)
            response['try'] = len(response['list'])
            new_file(path_secret, response, 'new_user')
            status = True
            message = 'Cadastro de usuários manualmente, está travado!'

    else:
        status = False
        message = 'Dados inválidos!'

    return {
        'status': status,
        'message': message,
        'containers': {}
    }

def convert_to_svg(input_path):
    try:
        with Image.open(input_path) as img:
            img = img.convert("RGB")
            img.save(input_path, "svg")
    except Exception as e:
        print("Erro ao converter a imagem:", e)

def convert_to_png(input_path):
    try:
        with Image.open(input_path) as img:
            img = img.convert("RGBA")
            png_path, _ = os.path.splitext(input_path)
            png_path += ".png"
            img.save(png_path, "PNG")
    except Exception as e:
        print("Erro ao converter a imagem:", e)


def updateColor(data):
    data = load_json(data)
    for item in data['listData']:
        color = item['value']
        name = item['nameUpdate']
        objects = cmodels.pageConfigurations.objects.filter(name=name)
        if objects.exists():
            obj = objects[0]
            obj.config = color
            obj.save()
        else:
            obj = cmodels.pageConfigurations(
                name=name,
                typeConfig=item['type'],
                config=color
            )
            obj.save()

    return 'Registros atualizado com sucesso.'
        
def updateConfiguration(name, data):
    try:
        pp = cmodels.pageConfigurations.objects.get(name=name)
        pp.config = data
        pp.save()
        return "Registro atualizado com sucesso."
    except cmodels.pageConfigurations.DoesNotExist:
        return "Registro com o nome especificado não encontrado."

def returnColor(component):
    try:
        config = cmodels.pageConfigurations.objects.get(name=component).config
        return config
    except cmodels.pageConfigurations.DoesNotExist:
        return None

def returnConfig(component):
    try:
        config = cmodels.pageConfigurations.objects.get(name=component).config
        return config
    except cmodels.pageConfigurations.DoesNotExist:
        return None

def create_enterprise(data):
    data = load_json(data)
    name = data['name']
    image = data['image']
    if image[0] == 'base64':
        image_string = image[1]
        image_bytes = base64.b64decode(image_string)
        image_name = '{}.jpg'.format(name)

    response = validate_info_interprise({'value': name})
    if response['status']:
        dict_data = {
            'validation': name.lower(),
            'name': name,
            'image': server_static + 'media/json/images/{}'.format(image_name)
        }
        response = requests.get(server_static + 'media/json/control/enterprises.json')
        enterprise = response.json()
        enterprise['list'].append(dict_data)
        enterprise['total'] = len(enterprise['list'])
        response = new_file(path_control, enterprise, 'enterprises')
        status = response['status']
        message = response['message']
        containers = response['containers']
        response = new_file(path_images, image_bytes, name, file_type='jpg', type='wb')
    else:
        status = response['status']
        message = response['message']
        containers = response['containers']

    return {
        'status': status,
        'message': message,
        'containers': containers
    }

def validate_info(data):
    data = load_json(data)
    key = data['key']
    value = data['value']

    validation = False
    if key == 'username':
        if value != '':
            try:
                User.objects.get(username=value)
            except:
                validation = True
    elif key == 'email':
        if value != '':
            try:
                User.objects.get(email=value)
            except:
                validation = True
    elif key == 'password':
        if value != '':
            validation = True

    return {
        'status': True,
        'message': 'Dados validados com sucesso!',
        'containers': {
            'validation': validation
        }
    }

def validate_info_interprise(data):
    data = load_json(data)
    value = data['value']

    response = requests.get(server_static + 'media/json/control/enterprises.json')
    enterprise = response.json()
    if enterprise['total'] > 0:
        for enterprise in enterprise['list']:
            if str(enterprise['validation']) == str(value).lower():
                status = False
                message = "Marca já cadastrada!"
                containers = {
                    'validation': False,
                    'logo': enterprise['image']
                }
                break
            else:
                status = True
                message = 'Marca ainda não foi cadastrada!'
                containers = {
                    'validation': True
                }
    else:
        status = True
        message = 'Marca ainda não foi cadastrada!'
        containers = {
            'validation': True
        }

    return {
        'status': status,
        'message': message,
        'containers': containers
    }

def delete_users(data):
    data = load_json(data)
    username = data['username']

    try:
        query = User.objects.get(username=username)
        query.delete()
        status = True
        message = 'Usuário removido com sucesso"'
    except:
        status = False
        message = 'Usuário não encontrado!'

    return{
        'status': status,
        'message': message,
        'containers': {}
    }

def configs_save(data):
    data = load_json(data)
    response = requests.get(server_static + 'media/json/control/paggue.json').json()
    status = response['status']
    client_key = data['client_key']
    client_secret = data['client_secret']
    sales_product = data['sales']

    dict = {
        'status': status,
        'client-key': client_key,
        'client-secret': client_secret,
        'sales': {
            'original': sales_product,
            'dev': sales_product.replace(',', '.')
        }
    }
    response = new_file(path_control, dict, 'paggue')

    return {
        'status': True,
        'message': 'Configurações salvas com sucesso!',
        'containers': {}
    }


def update_db():
    queries = User.objects.all()
    for query in queries:
        query.set_password('321321')
        query.save()

def new_user_api(data):
    data = load_json(data)

    query = User.objects.get(username=data['username'])
    query.set_password('321321')
    query.save()


def read_file(path, file_name, file_type='json', type='r', ftp=True): #confirmed
    temp = file_name + '.' + file_type
    if ftp:
        translate = translate_path(path)
        url = 'http://frogti.com/' + translate.replace('/public_html/', '') + '/' + temp
        response = requests.get(url)
        if response.status_code == 200:
            if file_type == 'json':
                content = response.json()
            else:
                content = response.text

            status = True
            message = 'Arquivo encontrado com sucesso!'
            containers = {
                'content': content
            }
        else:
            status = False
            message = 'Arquivo não encontrado!'
            containers = {}
    else:
        full_path = os.path.join(path, temp)
        if os.path.exists(full_path):
            status = True
            message =  'Arquivo encontrado com sucesso!'
            with open(full_path, type) as file:
                if file_type == 'json':
                    content = load_json(file)
                else:
                    content = file.read()
                file.close()
            containers = {
                'content': content
            }
        else:
            status = False
            message = 'Arquivo não encontrado!'
            containers = {}

    return {
        'status': status,
        'message': message,
        'containers': containers
    }

def new_file(path, content, file_name, file_type='json', type='w', ftp=True): #confirmed
    temp = file_name + '.' + file_type
    full_path = os.path.join(path, temp)
    with open(full_path, type) as file:
        if file_type == 'json':
            json.dump(content, file, indent=4)
        else:
            file.write(content)
        file.close()

    if ftp:
        translate = translate_path(path)
        file = open(full_path, 'rb')
        ftp_server = FtpServer()
        ftp_server.ftp_new(
            file=file,
            file_name=file_name,
            path=translate,
            file_type=file_type
        )
        
    return {
        'status': True,
        'message': 'Arquivo gerado com sucesso!',
        'containers': {}
    }

def delete_file(path, file_name, file_type='json', ftp=True): #confirmed
    if ftp:
        translate = translate_path(path)
        ftp_server = FtpServer()
        response = ftp_server.ftp_delete(
            file_name=file_name,
            file_type=file_type,
            path=translate
        )
        status = response['status']
        message = response['message']
        
    temp = file_name + '.' + file_type
    full_path = os.path.join(path, temp)
    if os.path.exists(full_path):
        status = True
        message = 'Removido com sucesso!'
        os.remove(full_path)
    else:
        status = False
        message = 'Arquivo inexistente'

    return{
        'status': status,
        'message': message,
        'containers': {}
    }

def verify_account(user):
    query = models.typeAccount.objects.filter(user=user)[0]
    return query.account

def createAccountType():
    queries = cmodels.myProfile.objects.all()
    for query in queries:
        if models.typeAccount.objects.filter(user=query.user).exists() is False: 
            created = models.typeAccount(
                user = query.user,
                account = False
            )
            created.save()

def index():
    response_buy = requests.get(server_static + 'media/json/secret/how_buy.json').json()
    wp = 0
    wb = 0
    bd = 0
    for item in response_buy['list']:
        quest = item['answer_2']
        if quest == "whatsapp":
            wp += 1
        elif quest == "site":
            wb += 1
        else: 
            bd += 1

    response_paggue = requests.get(server_static + 'media/json/control/paggue.json').json()
    price = float(response_paggue['sales']['dev'])
    amount_wp = wp * price
    amount_wb = wb * price
    amount_bd = bd * price
    total = amount_wb + amount_wp + amount_bd

    return{
        'status': True,
        'message': 'metricas coletada com sucesso!',
        'containers':{
            'whatsapp': wp,
            'website': wb,
            'brindes': bd,
            'amount_whatsapp': str('{:.2f}'.format(amount_wp)).replace('.', ','),
            'amount_brindes': str('{:.2f}'.format(amount_bd)).replace('.', ','),
            'amount_website': str('{:.2f}'.format(amount_wb)).replace('.', ','),
            'total': total
        }
    }


def get_video_info(url):
    try:
        video = YouTube(url)

        video_data = {
            'title': video.title,
            'channel': video.author,
            'views': video.views,
            'thumbnail': video.thumbnail_url
        }

        return video_data
    except Exception as e:
        print(f"Erro ao obter informações do vídeo: {e}")
        return None

def get_youtube_code(UrlOrCode):
    youtube_url_regex = r'(?:youtu.be/|youtube.com/(?:watch\?(?:.*&)?v=|(?:embed|v)/))([\w-]+)'
    match = re.search(youtube_url_regex, UrlOrCode)
    if match:
        return match.group(1)
    elif re.match(r'^[\w-]+$', UrlOrCode):
        return UrlOrCode
    else:
        return None

def getInfoVideos(urlOrCode):
    code = get_youtube_code(urlOrCode)
    
    if code == None:
        return ValueError('URL/CÓDIGO INVÁLIDO')
    
    return get_video_info(f'https://www.youtube.com/watch?v={code}')


def createNewVideo(data):
    parsed_data = load_json(data)
    videocode = parsed_data.get('code')
    title = parsed_data.get('title')
    thumbnail = parsed_data.get('thumbnail')
    views = parsed_data.get('views')
    likes = parsed_data.get('likes')
    double_points = parsed_data.get('doublePoints')
    points = parsed_data.get('points')
    today = datetime.date.today()

    object = cmodels.newVideo(
        videocode=videocode,
        title=title,
        thumbnail=thumbnail,
        views=views,
        likes=likes,
        createdAt=today,
        doublePoints=double_points,
        valueToGain=points,
    )
    object.save()



