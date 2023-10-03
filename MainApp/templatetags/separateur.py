from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
def cutA(value, arg):
    return value.replace(arg, "")


@register.filter
# stringfilter est utilisé quand la function de contient pas d'argument, rien que la valeur
@stringfilter
def lowerA(value):
    return value.lower()

@register.filter
# stringfilter est utilisé quand la function de contient pas d'argument, rien que la valeur
@stringfilter
def sep_float(valeur):
    try:
        if valeur == "None":
            return 0
        elif valeur == "":
            return ""
        else:
            valeur = float(valeur)
            v = f"{valeur:0,.2f}"
            #v = "{:,.2f}".format(abs(valeur))
            return v.replace(',',' ').replace('.',',')
            
    except Exception as e:
        pass
    
