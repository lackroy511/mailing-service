from django.shortcuts import render, redirect

from mail_sender.models import Client, MassageToSend, MailingSettings

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
    return redirect('http://127.0.0.1:8000/user_management/')


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
        user.comment = request.POST.get('comment')

        user.save()

        return redirect('http://127.0.0.1:8000/user_management/')

    return render(request, 'mail_sender/mailing_management/edit_user.html', context=context)


def mailing_management(request):
    '''
    Управление рассылкой.
    '''
    if request.method == 'POST':

        MailingSettings.objects.create(
            mailing_periodicity=f"{request.POST.get('minute')} "
                                f"{request.POST.get('hour')} "
                                f"{request.POST.get('day_month')} "
                                f"{request.POST.get('month')} "
                                f"{request.POST.get('day_week')}",
        )

        MassageToSend.objects.create(
            massage_subject=request.POST.get('massage_subject'),
            massage_text=request.POST.get('massage_text'),
            mailing_settings=MailingSettings.objects.latest('pk')
        )

    mailing_list = MassageToSend.objects.all()

    context = {
        'mailing_list': mailing_list
    }
    return render(request, 'mail_sender/mailing_management/mailing_management.html', context=context)


def del_mailing(request, pk):
    '''
    Управление рассылкой: Удаление рассылки.
    '''
    try:
        massage = MassageToSend.objects.get(pk=pk)
        MailingSettings.objects.get(pk=massage.mailing_settings.pk).delete()
        massage.delete()
    except ObjectDoesNotExist:
        return redirect('http://127.0.0.1:8000/mailing_management/')
    return redirect('http://127.0.0.1:8000/mailing_management/')


def edit_mailing(request, pk):
    '''
    Управление рассылкой: Редактирование рассылки.
    '''
    mailing = MassageToSend.objects.get(pk=pk)
    settings = MailingSettings.objects.get(pk=mailing.mailing_settings.pk)

    periodicity: str = mailing.mailing_settings.mailing_periodicity
    periodicity = periodicity.split(' ')

    context = {
        'massage_subject': mailing.massage_subject,
        'massage_text': mailing.massage_text,
        'minute': periodicity[0],
        'hour': periodicity[1],
        'day_month': periodicity[2],
        'month': periodicity[3],
        'day_week': periodicity[4],
    }

    if request.method == 'POST':
        mailing.massage_subject = request.POST.get('massage_subject')
        mailing.massage_text = request.POST.get('massage_text')
        settings.mailing_periodicity = f"{request.POST.get('minute')} {request.POST.get('hour')} {request.POST.get('day_month')} {request.POST.get('month')} {request.POST.get('day_week')}"

        mailing.save()
        settings.save()
        return redirect('http://127.0.0.1:8000/mailing_management/')

    return render(request, 'mail_sender/mailing_management/edit_mailing.html', context=context)