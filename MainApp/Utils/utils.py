import datetime
from django.utils import timezone
from django.core import serializers

from random import randint

import random
import string
import time
# from App_Vente.models import Model_Marchand

class utils(object):

    @staticmethod
    def toFloat(data):
        return (0.0 if data is None else float(data))

    @staticmethod
    def toDate(date):
        day = date[0:2]
        month = date[3:5]
        year = date[6:10]

        today = month + '-' + day + '-' + year
        today = datetime.datetime.strptime(today, '%m-%d-%Y')

        return today

    @staticmethod
    def toGenerateNumero(prefixe):

        annee = str(timezone.now().year)
        annee = annee[2:5]
        print(annee)
        temp_numero = prefixe + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8)) + "-" + annee
        return temp_numero

    @staticmethod
    def toGenerateNumeroNull():
        temp_numero =  ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
        return temp_numero

    # @staticmethod
    # def toGenerateNumeroRef():
    #     temp_numero = 0
    #     count = Model_Marchand.objects.all().count()
    #     if count > 0:
    #         last = Model_Marchand.objects.all().last()
    #         last = int(last.numero)
    #         temp_numero = last + 1
    #     else:
    #         temp_numero = 100

    #     return temp_numero





