from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def currency_email(x, autoescape=None):
    result = {
            'AGR': '$ ',
            'AUD': 'A$',
            'BRL': 'R$',
            'CAD': '$ ',
            'CHF': 'CHF',
            'CLP': '$ ',
            'DKK': 'kr',
            'HKD': '$ ',
            'HRK': 'kn',
            'IDR': 'Rp',
            'INR': 'Rs',
            'ISK': 'kr',
            'MXN': '$ ',
            'MYR': 'RM',
            'NOK': 'kr',
            'NZD': '$ ',
            'PEN': 'S/.',
            'RON': 'lei',
            'SEK': 'kr',
            'SGD': 'S$',
            'TWD': 'NT$',
            'USD': '$ ',
            'VEB': 'Bs',
            'ZAR': 'R ',
            }.get(x, x)
    return mark_safe(result);

currency_email.needs_autoescape = True

@register.filter
def currency_amount(x, autoescape=None):
    if x < 0:
        return x*(-1)
    else:
        return x

currency_amount.needs_autoescape = True
