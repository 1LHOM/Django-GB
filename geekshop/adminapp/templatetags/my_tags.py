from django import template
from django.conf import settings


register = template.Library()


@register.filter(name='media_for_users')
def media_for_users(avatar):
    if not avatar:
        avatar = 'users/default.jpg'

    return f'{settings.MEDIA_URL}{avatar}'


@register.filter(name='media_for_products')
def media_for_products(product_img):
    if not product_img:
        product_img = 'products/default-product-image.png'

    return f'{settings.MEDIA_URL}{product_img}'

# Кроме декоратции есть и еще один способ регистации фильтров
# register.filter('media_for_products', media_for_products)

