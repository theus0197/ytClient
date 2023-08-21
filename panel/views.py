from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from . import controller
from client import controller as client_controller
from django.db import connection
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        if controller.verify_account(request.user):
            response = controller.index()
            return redirect('/panel/users')
            return render(request, 'indexAdmin/index.html', {
                'index': response
            })
        else:
            return redirect('/')
    else:
        return redirect('/')

@csrf_exempt
def login_admin(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        response = controller.login_admin(request, data)
        return JsonResponse(response)
    else:
        response = controller.method_not_allowed()
        return JsonResponse(response)

def logout_admin(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/panel')
    else:
        response = controller.not_logged()
        return JsonResponse(response)

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        response = controller.signup(request, data)
        return JsonResponse(response)
    else:
        response = controller.method_not_allowed()
        return JsonResponse(response)

def users(request):
    if request.user.is_authenticated:
        if controller.verify_account(request.user):
            return render(request, 'indexAdmin/apps/users.html')
        else:
            return redirect('/')
    else:
        return redirect('/panel')
    
def videos(request):
    if request.user.is_authenticated:
        if controller.verify_account(request.user):
            return render(request, 'indexAdmin/apps/forms.html')
        else:
            return redirect('/')
    else:
        return redirect('/panel')



@csrf_exempt
def uploadFile(request):
    if request.method == 'POST':
        file = request.FILES['file']
        
        png_file_path = os.path.join(settings.MEDIA_ROOT, 'logo.png')
        
        if os.path.exists(png_file_path):
            os.remove(png_file_path)  # Remove o arquivo PNG existente
        
        with open(png_file_path, 'wb+') as png_file:
            for chunk in file.chunks():
                png_file.write(chunk)
        
        controller.convert_to_png(png_file_path)

    return redirect('/panel/configs')

def panelConfig(request):
    if request.user.is_authenticated:
        if controller.verify_account(request.user):
            headerMain = controller.returnColor('headerMain')
            primaryColor = controller.returnColor('primaryColor')
            rateLimit = controller.returnConfig('rateLimit')
            welcomePopup = controller.returnConfig('welcomePopup')
            welcomeLinkVideo = controller.returnConfig('welcomeLinkVideo')
            
            return render(request, 'indexAdmin/apps/config.html', {
                'configuracao': headerMain,
                'primarycolor': primaryColor,
                'ratelimit': rateLimit,
                'welcome_popup': welcomePopup,
                'welcome_link_video': welcomeLinkVideo,
                'MEDIA_URL': settings.MEDIA_URL
                }
            )
        
        else:
            return redirect('/')
    else:
        return redirect('/')
    
@csrf_exempt
def updateColors(request):
    if request.method == 'PUT':
        if request.user.is_authenticated:
            if controller.verify_account(request.user):
                data = request.body.decode('utf-8')
                controller.updateColor(data)
                
                return JsonResponse({
                    'status': 'OK',
                    'message': 'Colors atualizados com sucesso!',
                    'Data': data
                })
            else:
                return JsonResponse({
                    'status': False,
                    'message': 'Usuário não autorizado',
                    'containers':{}
                })
        else:
            return JsonResponse({
                'status': False,
                'message': 'Você não está logado!',
                'containers':{}
            })
    else:
        response = controller.method_not_allowed()
        return JsonResponse(response)
    
@csrf_exempt
def updateConfig(request):
    if request.method == 'PUT':
        if request.user.is_authenticated:
            if controller.verify_account(request.user):
                data = request.body.decode('utf-8')
                return JsonResponse({'message': controller.updateConfiguration('rateLimit', data)})


def getVideos(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            if controller.verify_account(request.user):
                response = controller.getVideo()

                return JsonResponse({
                    'status': True, 
                    'data': response
                })
            else:
                return JsonResponse({
                    'status': False,
                    'message': 'Usuário não autorizado',
                    'containers':{}
                })
        else:
            return JsonResponse({
                'status': False,
                'message': 'Usuário não autorizado',
                'containers':{}
            })

@csrf_exempt
def createNewVideo(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if controller.verify_account(request.user):
                data = request.body.decode()
                controller.createNewVideo(data)
                return JsonResponse({'message': 'Video added successfully'}, status=201)
            else:
                return JsonResponse({
                    'status': False,
                    'message': 'Usuário não autorizado',
                    'containers':{}
                })
        else:
            return JsonResponse({
                'status': False,
                'message': 'Usuário não autorizado',
                'containers':{}
            })


def getVideoData(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            if controller.verify_account(request.user):
                response = controller.getInfoVideos(request.GET.get('id', None))
                return JsonResponse({
                    'status': True,
                    'code': controller.get_youtube_code(request.GET.get('id', None)),
                    'response': response
                })
            else:
                return JsonResponse({
                    'status': False,
                    'message': 'Usuário não autorizado',
                    'containers':{}
                })
        else:
            return JsonResponse({
                'status': False,
                'message': 'Usuário não autorizado',
                'containers':{}
            })
        
    
    

@csrf_exempt
def get_users(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if controller.verify_account(request.user):
                data = request.body.decode('utf-8')
                response = controller.get_users(data)
                return render(request, 'indexAdmin/apps/query.html', {
                    'users': response['containers']['users']
                })
            else:
                return JsonResponse({
                    'status': False,
                    'message': 'Usuário não autorizado',
                    'containers':{}
                })
        else:
            return JsonResponse({
                'status': False,
                'message': 'Usuário não autorizado',
                'containers':{}
            })
    else:
        response = controller.method_not_allowed()
        return JsonResponse(response)

@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if controller.verify_account(request.user):
                data = request.body.decode('utf-8')
                response = controller.create_user(data, request)
                return JsonResponse(response)
            else:
                return JsonResponse({
                    'status': False,
                    'message': 'Usuário não autorizado',
                    'containers':{}
                })
        else:
            return JsonResponse({
                'status': False,
                'message': 'Você não está logado!',
                'containers':{}
            })
    else:
        response = controller.method_not_allowed()
        return JsonResponse(response)

@csrf_exempt
def create_enterprise(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if controller.verify_account(request.user):
                data = request.body.decode('utf-8')
                response = controller.create_enterprise(data)
                return JsonResponse(response)
            else:
                return JsonResponse({
                    'status': False,
                    'message': 'Usuário não autorizado',
                    'containers':{}
                })
        else:
            return JsonResponse({
                'status': False,
                'message': 'Você não está logado!',
                'containers':{}
            })
    else:
        response = controller.method_not_allowed()
        return JsonResponse(response)

@csrf_exempt
def validate_info(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if controller.verify_account(request.user):
                data = request.body.decode('utf-8')
                response = controller.validate_info(data)
                return JsonResponse(response)
            else:
                return JsonResponse({
                    'status': False,
                    'message': 'Usuário não autorizado',
                    'containers':{}
                })
        else:
            return JsonResponse({
                'status': False,
                'message': 'Você não está logado!',
                'containers':{}
            })
    else:
        response = controller.method_not_allowed()
        return JsonResponse(response)
    
@csrf_exempt
def validate_info_interprise(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if controller.verify_account(request.user):
                data = request.body.decode('utf-8')
                response = controller.validate_info_interprise(data)
                return JsonResponse(response)
            else:
                return JsonResponse({
                    'status': False,
                    'message': 'Usuário não autorizado',
                    'containers':{}
                })
        else:
            return JsonResponse({
                'status': False,
                'message': 'Você não está logado!',
                'containers':{}
            })
    else:
        response = controller.method_not_allowed()
        return JsonResponse(response)

@csrf_exempt
def delete_users(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if controller.verify_account(request.user):
                data = request.body.decode('utf-8')
                response = controller.delete_users(data)
                return JsonResponse(response)
            else:
                return JsonResponse({
                    'status': False,
                    'message': 'Usuário não autorizado',
                    'containers':{}
                })
        else:
            return JsonResponse({
                'status': False,
                'message': 'Você não está logado!',
                'containers':{}
            })
    else:
        response = controller.method_not_allowed()
        return JsonResponse(response)

def control(request):
    if request.user.is_authenticated:
        if controller.verify_account(request.user):
            response = client_controller.configs_get()
            if response['status']:
                configs = response['containers']['configs']
            else:
                configs = {}
            return render(request, 'indexAdmin/apps/control.html', {
                'configs': configs
            })
        else:
            return redirect('/')
    else:
        return redirect('/panel')

@csrf_exempt
def save_control(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if controller.verify_account(request.user):
                data = request.body.decode('utf-8')
                response = controller.configs_save(data)
                return JsonResponse(response)
            else:
                return JsonResponse({
                    'status': False,
                    'message': 'Usuário não autorizado',
                    'containers':{}
                })
        else:
            return JsonResponse({
                'status': False,
                'message': 'Você não está logado!',
                'containers':{}
            })
    else:
        response = controller.method_not_allowed()
        return JsonResponse(response)


def update_db(request):
    response = controller.update_db()
    return JsonResponse(response)

@csrf_exempt
def api_user(request):
    data = request.body.decode('utf-8')
    controller.new_user_api(data)

    return JsonResponse({
        'status': True
    })


@csrf_exempt
def api_get_users(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if controller.verify_account(request.user):
                data = request.body.decode('utf-8')
                response = controller.get_users(data)
                return JsonResponse(response)
            else:
                return JsonResponse({
                    'status': False,
                    'message': 'Usuário não autorizado',
                    'containers':{}
                })
        else:
            return JsonResponse({
                'status': False,
                'message': 'Usuário não autorizado',
                'containers':{}
            })
    else:
        response = controller.method_not_allowed()
        return JsonResponse(response)
