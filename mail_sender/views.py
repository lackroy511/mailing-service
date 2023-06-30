from django.shortcuts import render, redirect

from mail_sender.models import Client

from django.core.exceptions import ObjectDoesNotExist

# Create your views here.


def index(request):
    """
    Главная страница. 
    """

    context = {
        'is_active_main': 'active'
    }
    return render(request, 'mail_sender/index.html', context=context)


def user_management(request):
    """
    Управление пользователями
    """

    users_list = Client.objects.all()

    context = {
        'users_list': users_list
    }

    if request.method == 'POST':
        Client.objects.create(
            email=request.POST.get('email'),
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            surname=request.POST.get('surname'),
            comment=request.POST.get('comment')
        )

    return render(request, 'mail_sender/mailing_management/user_management.html', context=context)


def del_user(request, pk):
    """
    Управление пользователями: Удалить пользователя
    """

    try:
        Client.objects.get(pk=pk).delete()
    except ObjectDoesNotExist:
        return redirect('http://127.0.0.1:8000/user_management/')

    users_list = Client.objects.all()

    context = {
        'users_list': users_list
    }

    if request.method == 'POST':
        Client.objects.create(
            email=request.POST.get('email'),
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            surname=request.POST.get('surname'),
            comment=request.POST.get('comment')
        )

    return render(request, 'mail_sender/mailing_management/user_management.html', context=context)


def edit_user(request, pk):
    """
    Управление пользователями: Редактировать пользователя.
    """
    user = Client.objects.get(pk=pk)
    
    context = {
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'surname': user.surname,
        'comment': user.comment,
    }
    
    if request.method == 'POST':
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.surname = request.POST.get('surname')
        user.comment =request.POST.get('comment')
        
        user.save()
        
        return redirect('http://127.0.0.1:8000/user_management/')
    
    return render(request, 'mail_sender/mailing_management/edit_user.html', context=context)
