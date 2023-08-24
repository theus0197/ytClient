from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from . import controller
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from panel import controller as pcontroller
from django.db import connection
import json
from django.conf import settings

# Create your views here.
def index(request, page_id=None):
    if request.user.is_authenticated:
        data = controller.returnColor('headerMain')
        primaryColor = controller.returnColor('primaryColor')
        response_welcome_popup = controller.info_popup_welcome()
        response = controller.main(request.user)

        amount_draw = response['containers']['amount'].replace('.', '')
        amount_draw = float(amount_draw.replace(',', '.').replace('R$', '').replace(' ', ''))

        min_draw = pcontroller.returnConfig('minDraw')
        min_draw = min_draw.replace('.', '')
        min_draw = float(min_draw.replace(',', '.').replace('R$', '').replace(' ', ''))

        video_reedem = pcontroller.returnConfig('linkVideoReedem')
        video_reedem = video_reedem.split('?v=')[1] if '?v=' in video_reedem else video_reedem

        return render(request, 'index/main.html', {
            'amount': response['containers']['amount'],
            'amount_is': response['containers']['amount_is'],
            'amount_draw': amount_draw,
            'min_draw': min_draw,
            'first': response['containers']['first'],
            'headerMainColor': data,
            'primarycolor': primaryColor,
            'auth': pcontroller.verify_account(request.user),
            'welcome_popup': response_welcome_popup['welcome_popup'],
            'welcome_link_video': response_welcome_popup['welcome_link_video'],
            'url_reedem': pcontroller.returnConfig('urlReedem'),
            'video_reedem': video_reedem,
            'username': request.user.username
        })
    else:
        return render(request, 'index/login.html')

def login_template(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        return render(request, 'index/login.html', {
            'MEDIA_URL': settings.MEDIA_ROOT
        })

def signup_template(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        return render(request, 'index/signup.html')

def signup_template_farias(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        return render(request, 'index/signup_farias.html')

@csrf_exempt
def api_login(request):
    if request.method  == 'POST':
        if not request.user.is_authenticated:
            data = request.body.decode('utf-8')
            response = controller.api_login(request, data)
            if response['status']:
                return JsonResponse(response)
            else:
                return render(request, 'alerts/notification.html', {
                    'message': response['message']
                })
        else:
            return JsonResponse({
                'status': False,
                'message': 'Usuário já logado!',
                'containers': {}
            })
    else:
        response = controller.method_not_allowed()
        return JsonResponse(response)
    
def api_login_params(request, email, password):
    if not request.user.is_authenticated:
        data = {
            'email': email,
            'password': password
        }
        response = controller.api_login(request, data)
        
    return redirect('/')

def api_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')
    else:
        return redirect('/')
        

def lp(request):
    response = controller.configs_get()
    if response['status']:
        configs = response['containers']['configs']
    else:
        configs = {}
    return render(request, 'lp/index.html', {
        'configs': configs
    })


@csrf_exempt
def confirm_play(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            response = controller.confirm_play(request.user)
            return JsonResponse(response)
        else:
            response = controller.not_logged()
            return JsonResponse(response)
    else:
        response = controller.method_not_allowed()
        return JsonResponse(response)


def draw(request):
    if request.user.is_authenticated:
        response = controller.main(request.user)
        if pcontroller.verify_account(request.user):
            return render(request, 'index/draw_super.html', {
                'amount': response['containers']['amount'],
                'auth': pcontroller.verify_account(request.user),
                'min_draw': pcontroller.returnConfig('minDraw'),
                'first': response['containers']['first']
            })
        else:
            return render(request, 'index/draw.html', {
                'amount': response['containers']['amount'],
                'auth': pcontroller.verify_account(request.user),
                'min_draw': pcontroller.returnConfig('minDraw'),
                'first': response['containers']['first']
            })
    else:
        response = controller.not_logged()
        return JsonResponse(response)

@csrf_exempt
def api_draw(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            data = request.body.decode('utf-8')
            if pcontroller.verify_account(request.user):
                response = controller.draw_super(data, request.user)
            else:
                response = controller.draw_super(data, request.user)
                
            return JsonResponse(response)
        else:
            response = controller.not_logged()
            return JsonResponse(response)
    else:
        response = controller.method_not_allowed()
        return JsonResponse(response)

@csrf_exempt
def signup(request):
    if request.method  == 'POST':
        if not request.user.is_authenticated:
            data = request.body.decode('utf-8')
            response = controller.signup(data)
            return JsonResponse(response)
            
        else:
            return JsonResponse({
                'status': False,
                'message': 'Usuário já logado!',
                'containers': {}
            })
    else:
        response = controller.method_not_allowed()
        return JsonResponse(response)

@csrf_exempt
def api_confirm_forms(request):
    if request.method  == 'POST':
        if request.user.is_authenticated:
            data = request.body.decode('utf-8')
            response = controller.confirm_forms(request.user, data)
            return JsonResponse(response)
        else:
            return JsonResponse({
                'status': False,
                'message': 'Você precisa logar ou cadastrar uma conta',
                'containers': {}
            })
    else:
        response = controller.method_not_allowed()
        return JsonResponse(response)

@csrf_exempt
def api_forms_how(request):
    if request.method  == 'POST':
        if request.user.is_authenticated:
            data = request.body.decode('utf-8')
            response = controller.api_forms_how(data, request.user)
            return JsonResponse(response)
        else:
            return JsonResponse({
                'status': False,
                'message': 'Você precisa logar ou cadastrar uma conta',
                'containers': {}
            })
    else:
        response = controller.method_not_allowed()
        return JsonResponse(response)
@csrf_exempt
def webhook(request):
    if request.method  == 'POST':
        data = request.body.decode('utf-8')
        response = controller.status_webhook(data)
        return JsonResponse(response)
    else:
        response = controller.method_not_allowed()
        return JsonResponse(response)

@csrf_exempt
def confirm_payment(request):
    if request.method  == 'POST':
        if request.user.is_authenticated is False:
            data = request.body.decode('utf-8')
            response = controller.confirm_payment(request, data)
            return JsonResponse(response)
        else:
            return JsonResponse({
                'status': False,
                'message': 'Você já está logado na sua conta!',
                'containers': {}
            })
    else:
        response = controller.method_not_allowed()
        return JsonResponse(response)
    
def test_webhook(request):
    response = controller.test_webhook()
    return HttpResponse(response)

def handler_not_found(request, exception):
    return redirect('/')

def reset_password(request, email):
    data = {
        'email': email
    }
    response = controller.reset_login(data)
        
    return redirect('/')

def renderColorsHeader(request):
    ...

def getAllVideos(request):
    if request.method  == 'GET':
        if request.user.is_authenticated:
            response = controller.getVideos(request.user.id)
            return JsonResponse(response, safe=False)
        else:
            return JsonResponse({
                'status': False,
                'message': 'Você não está logado na sua conta!',
                'containers': {}
            })
    else:
        response = controller.method_not_allowed()
        return JsonResponse(response)

def getVideo(request, id):
    if request.method  == 'GET':
        if request.user.is_authenticated:
            response = controller.getVideoById(request.user.id, id)
            return JsonResponse(response, safe=False)
        else:
            return JsonResponse({
                'status': False,
                'message': 'Você não está logado na sua conta!',
                'containers': {}
            })
    else:
        response = controller.method_not_allowed()
        return JsonResponse(response)
    
@csrf_exempt
def likeVideo(request, id):
    if request.method  == 'POST':
        if request.user.is_authenticated:
            response = controller.likeVideo(request.user, request.user.id, id)
            return JsonResponse(response, safe=False)
        else:
            return JsonResponse({
                'status': False,
                'message': 'Você não está logado na sua conta!',
                'containers': {}
            })
    else:
        response = controller.method_not_allowed()
        return JsonResponse(response)
        
def webhook_handler(request):
    if request.method == 'POST' or request.method == 'PUT':
        data = request.body.decode('utf-8')
        response = controller.hotmart_webhook(data)
        return JsonResponse({'message': 'Webhook received successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})

@csrf_exempt   
def first_access(request):
    if request.method  == 'POST':
        if request.user.is_authenticated:
            response = controller.first_acesss(request)
            return JsonResponse(response)
        else:
            return JsonResponse({
                'status': False,
                'message': 'Você não está logado na sua conta!',
                'containers': {}
            })
    else:
        response = controller.method_not_allowed()
        return JsonResponse(response)