from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse


def send_email(request):
    if request.method == 'POST':
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        recipient_email = request.POST.get('recipient_email', '')

        send_mail(subject, message, 'nikhilkalkhanda@gmail.com', [recipient_email])
        return HttpResponse('Email sent successfully!')
    return render(request, 'send_email.html')
