from datetime import datetime
from django import template

register = template.Library()

@register.filter("tsToDate")
def tsToDate(value, arg):
    return datetime.utcfromtimestamp(int(value)).strftime(arg)
    
@register.filter("divide")
def divide(value, arg):
    return float(value)/float(arg)