import random
from django.core.mail import send_mail
from django.conf import settings
import json
import redis
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


redis_client = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB
)


def generate_verification_code():
    return str(random.randint(1000, 9999))


def send_verification_code(email, code):
    subject = "Ваш код верификации"
    message = f"Ваш код верификации: {code}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    try:
        send_mail(subject, message, from_email, recipient_list)
        print("Verification email sent successfully")
    except Exception as e:
        print(f"Failed to send verification email: {e}")


@csrf_exempt
def send_verification_code_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')

        if email:
            code = generate_verification_code()
            # Сохраняем код в Redis с TTL 5 минут
            redis_client.setex(f'verification_code:{email}', 300, code)
            send_verification_code(email, code)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Email не указан'})
    return JsonResponse({'success': False, 'error': 'Неверный метод запроса'})


def send_welcome_email(user):
    subject = "Добро пожаловать на наш сайт!"
    message = (
        f"Здравствуйте, {user.first_name},\n\n"
        "Спасибо за регистрацию на нашем сайте.\n\n"
        "С уважением,\nКоманда сайта"
    )
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]

    try:
        send_mail(subject, message, from_email, recipient_list)
        print("Welcome email sent successfully")
    except Exception as e:
        print(f"Failed to send welcome email: {e}")
