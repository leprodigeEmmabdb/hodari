from django import template
from django.template.defaultfilters import stringfilter
from MainApp.Utils.auth import auth
#from App_GestionStock.models import Model_Emplacement, Model_Article

register = template.Library()

@register.simple_tag
def add(a, b):
    a = float(a)
    b = float(b)
    valeur = a + b
    v = f"{valeur:0,.2f}"
    #v = "{:,.2f}".format(abs(valeur))
    return v.replace(',',' ').replace('.',',')

@register.simple_tag
def sous(a, b):
    a = float(a)
    b = float(b)
    valeur = a - b
    v = f"{valeur:0,.2f}"
    #v = "{:,.2f}".format(abs(valeur))
    return v.replace(',',' ').replace('.',',')


@register.simple_tag
def multiply(a, b):
    a = float(a)
    b = float(b)
    valeur = a * b
    v = f"{valeur:0,.2f}"
    #v = "{:,.2f}".format(abs(valeur))
    return v.replace(',',' ').replace('.',',')

@register.simple_tag
def stock_empl(user_id, article_id):
    employe = auth.getEmployeFromId(user_id)
    #emplacement = Model_Emplacement.objects.get(employe.pos.emplacement.id)
    article = Model_Article.objects.get(pk=article_id)
    
    return article.disponible_emplacement(employe.pos.emplacement.id)
    

"""
@register.simple_tag
def bal_wu(a, b, c, d):
    a = float(a)
    b = float(b)
    c = float(c)
    d = float(d)
    
    s1 = a-b
    s2 = c-d
    valeur = s1 + s2
    v = f"{valeur:0,.2f}"
    #v = "{:,.2f}".format(abs(valeur))
    return v.replace(',',' ').replace('.',',')
"""
@register.simple_tag
def add_solde_wu_report(a):
    valeur = 0.0
    
    for i in a:
        valeur += float(i['solde'])
    
    v = f"{valeur:0,.2f}"
    #v = "{:,.2f}".format(abs(valeur))
    return v.replace(',',' ').replace('.',',')

@register.simple_tag
def solde_clot_wu_report(a):
    valeur = 0.0
    
    for i in a:
        valeur += float(i['clot'])
    
    v = f"{valeur:0,.2f}"
    #v = "{:,.2f}".format(abs(valeur))
    return v.replace(',',' ').replace('.',',')


@register.simple_tag
def bal_wu(a):
    
    valeur = 0.0
    
    for i in a:
        v = float(i['clot']) - float(i['solde'])
        valeur += v
        
    v = f"{valeur:0,.2f}"
    #v = "{:,.2f}".format(abs(valeur))
    return v.replace(',',' ').replace('.',',')

@register.filter(name='multiply')
def multiply(value, arg):
    return value*arg