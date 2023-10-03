from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.simple_tag
def mois_to_lettre(mois):
    
    mois = int(mois)
    lettre = None
    
    if mois == 1:
        lettre = "Janvier"
    elif mois == 2:
        lettre = "Février"
    elif mois == 3:
        lettre = "Mars"
    elif mois == 4:
        lettre = "Avril"
    elif mois == 5:
        lettre = "Mai"
    elif mois == 6:
        lettre = "Juin"
    elif mois == 7:
        lettre = "Juillet"
    elif mois == 8:
        lettre = "Août"
    elif mois == 9:
        lettre = "Septembre"
    elif mois == 10:
        lettre = "Octobre"
    elif mois == 11:
        lettre = "Novembre"
    elif mois == 12:
        lettre = "Décembre"
    
    return lettre
