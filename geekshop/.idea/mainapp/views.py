import json

from django.conf import settings
from django.shortcuts import render

from mainapp.models import Product, ProductCategory


def index(request):

    products_list = Product.objects.all()[:4]
    print(products_list.query)

    context = {
        'title': 'Главная | Interior - online furniture shopping',
        'products': products_list
    }
    return render(request, 'mainapp/index.html', context)


def products(request, pk=None):

    links_menu = ProductCategory.objects.all()

    context = {
        'links_menu': links_menu,
        'title': 'Продукты | Interior - online furniture shopping'
    }
    return render(request, 'mainapp/products.html', context)


def contact(request):

    with open(f"{settings.BASE_DIR}/contacts.json", encoding='utf-8') as contacts_file:
        context = {
            'contacts': json.load(contacts_file),
            'title': 'Контакты | Interior - online furniture shopping'
        }
    return render(request, 'mainapp/contact.html', context)
