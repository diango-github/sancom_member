from django.core.mail import send_mail
from django.http import HttpResponse

def emailfunc(request):
    send_mail('パスワードリセット', '新しいパスワードの入力', 'info@san-com.jp', ['info@san-com.jp'], fail_silently=False,)
    return HttpResponse('')
