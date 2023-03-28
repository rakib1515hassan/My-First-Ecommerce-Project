from django import template

register = template.Library()

@register.simple_tag
def Save_Price(Regular_Price, Special_Price):
    save = Regular_Price - Special_Price
    return save

@register.simple_tag
def Product_Price(Special_Price, Quentity):
    price = Special_Price * Quentity
    return price