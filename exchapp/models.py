from django.db import models
from django.contrib.auth.models import User
from filex import settings

# Create your models here.

class Document(models.Model):
    '''
    Модель для хранения данных об имени файла и том, кто загрузил.
    duration - длительность хранения файла на сервере, 0 - бессрочно
    '''
    name = models.FileField(verbose_name='Имя файла (до 255 букв) (*)',
                            max_length=255)
    author = models.ForeignKey(User, verbose_name='Кто загрузил (*)')
    duration = models.IntegerField(verbose_name='Сколько дней хранить ('
                                                '0-бессрочно) (*)', default=0)
    comm = models.CharField(verbose_name='Комментарий к файлу', max_length=500, null=True, blank=True)
    is_public = models.BooleanField(verbose_name='Публичный доступ',
                                    default=True)
    readers = models.ManyToManyField(User, related_name='reader',
                                     verbose_name='Читатели (для '
                                                  'непубличного доступа)',
					blank=True, null=True)

    def __str__(self):
        return self.name.name + ' от ' + self.author.username

    def filename(self):
        import re
        return re.sub(r'^\./', '', self.name.name)

    def href(self):
        import re
        return settings.DOCS_URL + re.sub('^\./', '', self.name.name)

    def privref(self):
        import re
        return settings.PRIVATE_URL + re.sub('^\./', '', self.name.name)

    def get_readers(self):
        list = ''
        i = 0
        for reader in self.readers.all():
            if i>0:
                list += ',<br>'
            list += reader.username
            i += 1
        return list



