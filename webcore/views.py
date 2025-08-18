from django.core.signing import TimestampSigner, dumps, loads
from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.
def home(request):
    return render(request, 'webcore/home.html')


def cookie_demo(request):
    ctx={
        'raw_cookies': request.COOKIES,
    }
    return render(request, 'webcore/cookie_demo.html', ctx)

def cookie_set(request):
    resp=redirect('cookie_demo')
    resp.set_cookie("theme","dark",max_age=60*60*24*30,httponly=True)  # 30 days
    return resp

def cookie_delete(request):
    resp=redirect('cookie_demo')
    resp.delete_cookie("theme")
    return resp


def session_demo(request):
    ctx={
        'session_key': request.session.session_key,
        'session_data': request.session.items(),
        'cookie_age': request.session.get_expiry_age(),
        'cookie_date': request.session.get_expiry_date(),

    }
    return render(request, 'webcore/session_demo.html', ctx)


def session_counter(request):
    n=request.session.get('visits',0) + 1
    request.session['visits'] = n
    return  HttpResponse(f'visit number: {n}')

def session_set_expiry(request):
    request.session.set_expiry(60*60)  # 1 hour
    return HttpResponse('Session expiry set to 1 hour')

def session_flush(request):
    request.session.flush()
    return HttpResponse('Session flushed')


def session_cycle(request):
    request.session.cycle_key()
    return redirect('session_demo')


def session_test_cookie(request):
    request.session.set_test_cookie()
    return HttpResponse('Test cookie set, please reload the page.')

#debug
#info
#warning
#error
#success
from django.contrib import messages

def message_demo(request):
    return render(request, 'webcore/message_demo.html')


def message_success(request):
    messages.success(request, 'This is a success message!')
    return redirect('message_demo')

def message_error(request):
    messages.error(request, 'This is a error message!')
    return redirect('message_demo')

def message_custom(request):
    messages.add_message(request, 25, 'This is a custom message!')
    return redirect('message_demo')


def signing_demo(request):
    return render(request, 'webcore/signing_demo.html')


def signing_make_token(request):
    signer=TimestampSigner(salt='email')
    token=signer.sign('user_id = 12342') #Только строка
    return HttpResponse(token)


def signing_pack_payload(request):
    signed=dumps(12345,salt='api')
    data=loads(signed, salt='api')
    return HttpResponse(f"Signed data: {signed}<br>Unpacked data: {data}")

def cookie_set_signed(request):
    resp=redirect('cookie_demo')
    resp.set_signed_cookie("promo_code","summer2021",salt="hi", max_age=60*60*24*30, httponly=True)
    return resp

