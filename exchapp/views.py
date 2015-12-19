import mimetypes
import urllib
import re

import django.contrib.auth.models
import django.forms as forms

from django.contrib.auth.models import User
from django.shortcuts import render
from django.shortcuts import HttpResponse, render_to_response, redirect, \
    RequestContext
from django.http import StreamingHttpResponse
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.core.servers.basehttp import FileWrapper
from django.forms import ValidationError
from django.db.models import Q
from django.forms import Form
from django.forms import ModelForm

from filex import settings
from exchapp import models

# Create your views here.


class FileUploadForm(ModelForm):
    class Meta:
        model = models.Document
        fields =    ('name', #'author',
                    'duration',
                    'comm',
                     'is_public',
                     'readers')


def delete_from_public(doc_id):
    try:
        doc = models.Document.objects.get(pk=int(doc_id))
        import os
        try:
            os.remove(settings.MEDIA_ROOT + doc.name.name)
        except OSError:
            pass
    except doc.DoesNotExist:
        pass

def upload_private_file(f, name):
    with open(settings.PRIVATE_ROOT + name.name[2:], 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

@login_required
def serve_file(request, name):
    # контроль доступа
    doc = None
    try:
        doc = models.Document.objects.get(name='./' + name)
    except models.Document.DoesNotExist:
        return HttpResponse('Файл не найден или не существует.')
    if request.user not in doc.readers.all() and request.user!=doc.author:
        return HttpResponse('У Вас нет прав на скачивание данного файла.')
    # скачивание файла
    ctype = mimetypes.guess_type(name)
    f = None
    f = open(settings.PRIVATE_ROOT + name, 'rb')
    #except FileNotFoundError:
    #    return HttpResponse('Файл не найден')
    if not f:
        return HttpResponse('Файл не найден или не существует.')
    data = File(f)
    response = HttpResponse(data, content_type=ctype)
    # todo: Сделать на Streaming response
    #chunk_size = 8192
    #response = StreamingHttpResponse(FileWrapper(f, chunk_size),
    #                       content_type=mimetypes.guess_type(f)[0])
    #response['Content-Length'] = os.path.getsize(the_file)
    response['Content-Disposition'] = 'attachment; filename=' + urllib.parse.quote(name.encode('utf-8'))
    return response


@login_required
def home(request):
    form = None
    if request.method=='POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            doc = None
            doc_name = form.cleaned_data['name']
            doc = form.save(commit=False)
            doc.author = request.user
            doc.save()
            doc.readers = form.cleaned_data['readers']
            doc.save()
            if form.cleaned_data['is_public']==False:
                # Проверка на дублирование имени
                # Блок проверки для Linux - в Windows не нужен!!!
                delete_from_public(doc.id)
                name_tmp = doc.name.name
                name_indexed = name_tmp
                #return HttpResponse(doc.name.name)
                # TODO: Переделать на явную запись файлов без FileField
                found = True
                index = 0
                while found:
                    doc_tmp = models.Document.objects.filter(name=name_indexed)
                    if doc_tmp:
                        index += 1
                        name_indexed_parts = re.split('[.](?=[^.]+$)', name_indexed)
                        name_indexed = ''
                        for i in range(len(name_indexed_parts)):
                            if i<len(name_indexed_parts)-1:
                                name_indexed += name_indexed_parts[i]
                            else:
                                name_indexed += str(index) + '.' + name_indexed_parts[i]
                    else:
                        found = False
                #return HttpResponse(name_indexed)
                # Загрузка
                doc.name.name = name_indexed
                doc.save()
                #return HttpResponse(doc.name.name)
                # конец блока проверки для Windows
                upload_private_file(f=request.FILES['name'],
                                    #name=form.cleaned_data['name']
                                    name=doc.name)
            return redirect('/')
    else:
        form = FileUploadForm()
    uploaded_files = models.Document.objects.filter(author=request.user)
    available_files = models.Document.objects.filter(Q(readers=request.user)|Q(author=request.user), is_public=False)
    return render_to_response('home.html',context={
                                        'form':form,
                                        'docs':uploaded_files,
                                        'available_docs':available_files},
                              context_instance=RequestContext(request,
                                                              {}.update(
                                  csrf(request))))

def startpage(request):
    if request.user.is_authenticated():
        return redirect('/home/')
    return render_to_response('home.html')

def delete(request, doc_id=None):
    if doc_id:
        try:
            doc = models.Document.objects.get(pk=int(doc_id))
            pref = ''
            if doc.is_public:
                pref = settings.MEDIA_ROOT
            else:
                pref = settings.PRIVATE_ROOT
            #return HttpResponse(settings.MEDIA_ROOT + doc.name.name)
            import os
            try:
                os.remove(pref + doc.name.name)
            except OSError:
                pass
            doc.delete()
        except doc.DoesNotExist:
            pass
    return redirect('/')

