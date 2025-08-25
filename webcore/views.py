from base64 import urlsafe_b64encode, urlsafe_b64decode

from django.core.signing import TimestampSigner, dumps, loads
from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Rubric
from .serializers import RubricSerializer


# Create your views here.
def home(request):
    return render(request, 'webcore/home.html')


def cookie_demo(request):
    ctx = {
        'raw_cookies': request.COOKIES,
    }
    return render(request, 'webcore/cookie_demo.html', ctx)


def cookie_set(request):
    resp = redirect('cookie_demo')
    resp.set_cookie("theme", "dark", max_age=60 * 60 * 24 * 30, httponly=True)  # 30 days
    return resp


def cookie_delete(request):
    resp = redirect('cookie_demo')
    resp.delete_cookie("theme")
    return resp


def session_demo(request):
    ctx = {
        'session_key': request.session.session_key,
        'session_data': request.session.items(),
        'cookie_age': request.session.get_expiry_age(),
        'cookie_date': request.session.get_expiry_date(),

    }
    return render(request, 'webcore/session_demo.html', ctx)


def session_counter(request):
    n = request.session.get('visits', 0) + 1
    request.session['visits'] = n
    return HttpResponse(f'visit number: {n}')


def session_set_expiry(request):
    request.session.set_expiry(60 * 60)  # 1 hour
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


# debug
# info
# warning
# error
# success
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
    signer = TimestampSigner(salt='email')
    token = signer.sign('user_id = 12342')  # Только строка
    return HttpResponse(token)


def signing_pack_payload(request):
    signed = dumps(12345, salt='api')
    data = loads(signed, salt='api')
    return HttpResponse(f"Signed data: {signed}<br>Unpacked data: {data}")


def cookie_set_signed(request):
    resp = redirect('cookie_demo')
    resp.set_signed_cookie("promo_code", "summer2021", salt="hi", max_age=60 * 60 * 24 * 30, httponly=True)
    return resp


from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.core.mail import *


def test_email(request):
    subject = "Проверка test_email"
    plain = "Текстовая часть письма"
    html = "<h1>HTML часть письма</h1>"
    to = settings.DEFAULT_FROM_EMAIL
    sent = send_mail(subject, plain, settings.DEFAULT_FROM_EMAIL, [to], html_message=html, fail_silently=False)
    return JsonResponse({"sent": sent, to: "to"})


def send_low_code_email_v1(request):
    email = EmailMessage(
        subject="Проверка send_low_code_email",
        body="Текстовая часть письма",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.DEFAULT_FROM_EMAIL]
    )
    email.send(fail_silently=False)
    return JsonResponse({"sent": True})


def send_low_code_email_v2(request):
    content = "1234567890"
    email = EmailMessage(
        subject="Проверка EmailMessage с файлом",
        body="Прикрепленный код",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.DEFAULT_FROM_EMAIL]
    )
    email.attach("code.txt", content, "text/plain")
    email.send(fail_silently=False)
    return JsonResponse({"status": True})


def send_low_code_email_v3(request):
    email = EmailMultiAlternatives(
        subject="Проверка EmailMessage с html",
        body="Прикрепленный код",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.DEFAULT_FROM_EMAIL]
    )
    email.attach_alternative("""
    <h1>Проверка EmailMessage с html</h1>
    <h2>Прикрепленный код</h2>""",
                             "text/html")
    email.send(fail_silently=False)
    return JsonResponse({"status": True})


def send_many_emails(request):
    with get_connection() as conn:
        messages = []
        for i in range(3):
            m = EmailMessage(
                subject=f"Проверка send_many_emails {i}",
                body="Текстовая часть письма",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.DEFAULT_FROM_EMAIL],
                connection=conn,
            )
            messages.append(m)
        sent = conn.send_messages(messages)
        return JsonResponse({"sent": sent})


def notify_admins(request):
    mail_admins("Письмо для админов", "Все работает", fail_silently=False)
    return JsonResponse({"status": "ok"})


def contact_form(request):
    if request.method == "GET":
        return render(request, "webcore/contact_form.html")
    else:
        email = request.POST.get("email", "".strip())
        subject = request.POST.get("tema", "".strip())
        message = request.POST.get("message", "".strip())

        em = EmailMessage(
            subject=subject,
            body=f"Сообщение от {email}:\n \n {message}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
        )

        if hasattr(request, "FILES") and "file" in request.FILES:
            f = request.FILES["file"]
            em.attach(f.name or "attachment.bin", f.read(), "application/octet-stream")

        with get_connection() as conn:
            conn.send_messages([em])
            sent = em.send(fail_silently=False)

            token = make_token(email)
            verify_url = f"{get_site_url()}/webcore/verify/{token}/"
            send_mail(
                subject="Подтверждение email",
                message=f"Для подтверждения email перейдите по ссылке: {verify_url}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )

    return JsonResponse({"sent": sent})


def get_site_url():
    return getattr(settings, "SITE_URL", "http://127.0.0.1:8000")


from django.utils.crypto import salted_hmac


def make_token(email):
    sig = salted_hmac('verify', email).hexdigest()
    raw = f"{email}:{sig}".encode("utf-8")
    return urlsafe_b64encode(raw).decode("utf-8")


def verify_token(request,token):
    try:
        raw = urlsafe_b64decode(token.encode()).decode("utf-8")
        email, sig = raw.split(":", 1)
        if salted_hmac('verify', email).hexdigest() != sig:
            return HttpResponse("Invalid token", status=400)
    except Exception:
        return HttpResponse("Invalid token", status=400)

    return HttpResponse(f"Token is valid for {email}", status=200)

@api_view(['GET'])
def rubrics_api(request):
    qs = Rubric.objects.order_by("name")
    data = RubricSerializer(qs, many=True).data
    return Response(data,status=200)

