from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def currency(x, autoescape=None):
    result = {
            'AGR': '$ ',
            'AUD': 'A$',
            'BRL': 'R$',
            'CAD': '$ ',
            'CHF': 'CHF',
            'CLP': '$ ',
            'CNY': '&#165; ',
            'CRC': '&#8353; ',
            'CZK': 'K&#269; ',
            'DKK': 'kr',
            'EUR': '&#8364; ',
            'GBP': '&#163; ',
            'HKD': '$ ',
            'HRK': 'kn',
            'IDR': 'Rp',
            'ILS': '&#8362; ',
            'INR': 'Rs',
            'ISK': 'kr',
            'JPY': '&#165; ',
            'KRW': '&#8361; ',
            'MXN': '$ ',
            'MYR': 'RM',
            'NOK': 'kr',
            'NZD': '$ ',
            'PEN': 'S/.',
            'PHP': '&#8369; ',
            'PKR': '&#8360;',
            'PLN': '&#122;&#322;',
            'RON': 'lei',
            'RUB': '&#1088;&#1091;&#1073;',
            'SEK': 'kr',
            'SGD': 'S$',
            'THB': '&#3647; ',
            'TWD': 'NT$',
            'UAH': '&#8372; ',
            'USD': '$ ',
            'VEB': 'Bs',
            'VND': '&#8363; ',
            'ZAR': 'R ',
            }.get(x, '$')
    return mark_safe(result);

currency.needs_autoescape = True
