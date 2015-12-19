import uuid

from django.shortcuts import render
from django.core.mail import send_mail

import django.contrib.auth.models
import django.forms as forms

from django.contrib.auth.models import User
from django.shortcuts import render
from django.shortcuts import HttpResponse, render_to_response, redirect, \
    RequestContext
from django.core.context_processors import csrf
from django.forms import ValidationError
from django.contrib.sites.shortcuts import get_current_site

from ureg.models import RegVerificationKey
from filex import settings


# Create your views here.
def validate_username(username):
    '''
    Checks uniqueness
    :param username:
    :return:
    '''
    usrs = User.objects.filter(username=username)
    if usrs:
        raise ValidationError('Такой пользователь уже есть.', code='user_not_unique')

class RegForm(forms.Form):
    username = forms.CharField(max_length=30, label='Логин (*):', validators=[
        validate_username])
    email = forms.EmailField(label='Эл. почта (*):')
    first_name = forms.CharField(label='Имя', max_length=30, required=False)
    last_name = forms.CharField(label='Фамилия', max_length=30, required=False)
    pwd1 = forms.CharField(max_length=128, label='Парол (*):',
                           widget=forms.PasswordInput)
    pwd2 = forms.CharField(max_length=128, label='Еще раз парол (*):',
                           widget=forms.PasswordInput)
    def clean(self):
        cleaned_data = super(RegForm, self).clean()
        pwd1 = cleaned_data.get('pwd1')
        pwd2 = cleaned_data.get('pwd2')
        if pwd1 != pwd2:
            raise ValidationError('Введенные паролы не совпадают.', code='passw_not_equal')


def reg(request, reg_slug=''):
    form = None
    user = None
    if request.method == 'POST':
        form = RegForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'],
                                            email=form.cleaned_data['email'],
                                            password=form.cleaned_data['pwd1'])
            user.is_active = False
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            notif_subj = 'Требуется подтверждение регистрации.'
            verify_obj = RegVerificationKey.objects.create(user=user, key=str(uuid.uuid4()))
            verify_obj.save()
            if reg_slug:
                notif_body = 'Перейдите по ссылке: http://' + get_current_site(request).domain + '/' + reg_slug + \
                             '/verify/' + verify_obj.key
            else:
                notif_body = 'Перейдите по ссылке: http://' + get_current_site(request).domain + \
                             '/verify/' + verify_obj.key
            em_from_address = ''
            try:
                if settings.UREG_NOTIF_FROM_ADDRESS:
                    em_from_address = settings.UREG_NOTIF_FROM_ADDRESS
            except:
                em_from_address = 'some@any.com'
            send_mail(notif_subj, notif_body, em_from_address, [user.email], fail_silently=True)
            if reg_slug:
                return redirect('/' + reg_slug + '/done/')
            return redirect('/done/')
    else:
        form = RegForm()
    return render_to_response('user_register.html',context={
                                        'form':form,
                                        'action':request.get_full_path()},
                              context_instance=RequestContext(request,
                                                              {}.update(
                                  csrf(request))))

def verify(request, key, reg_slug=''):
    try:
        ver = RegVerificationKey.objects.get(key=key)
        #user = User.objects.get(pk=ver.user.user_id)
        ver.user.is_active = True
        ver.user.save()
        if reg_slug:
            return redirect('/' + reg_slug + '/verified/')
        return redirect('/verified/')
    except RegVerificationKey.DoesNotExist:
        if reg_slug:
            return redirect('/' + reg_slug + '/verification_failed/')
        return redirect('/verification_failed/')


def done(request, title, body, reg_slug=''):
    return render_to_response('redirect_notification.html', {'notif_title':title, 'notif_body':body, 'home_url':'/'})