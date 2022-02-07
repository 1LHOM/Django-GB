import json
import random

from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.models import Product, ProductCategory


def get_hot_product():
    products_list = Product.objects.all()

    return random.sample(list(products_list), 1)[0]


def get_same_products(hot_product):
    same_products_list = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)

    return same_products_list[:3]


def index(request):

    products_list = Product.objects.all()[:4]
    print(products_list.query)

    context = {
        'title': 'Главная | Interior - online furniture shopping',
        'products': products_list
    }
    return render(request, 'mainapp/index.html', context)


def products(request, pk=None, page=1):

    links_menu = ProductCategory.objects.all()

    if pk is not None:
        if pk == 0:
            products_list = Product.objects.all()
            category_item = {'name': 'Все', 'pk': 0}
            title = 'Все продукты | Interior - online furniture shopping'
        else:
            category_item = get_object_or_404(ProductCategory, pk=pk)
            products_list = Product.objects.filter(category__pk=pk)
            title = f'{str(category_item).title()} | Interior - online furniture shopping'

        # page = request.GET('page', 1)
        paginator = Paginator(products_list, 6)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(page)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        context = {
            'title': title,
            'links_menu': links_menu,
            'products': products_paginator,
            'category': category_item
        }

        return render(request, 'mainapp/products_list.html', context)
    hot_product = get_hot_product()
    context = {
        'links_menu': links_menu,
        'title': 'Товары | Interior - online furniture shopping',
        'hot_product': hot_product,
        'same_products': get_same_products(hot_product)
    }
    return render(request, 'mainapp/products.html', context)


def contact(request):

    with open(f"{settings.BASE_DIR}/contacts.json", encoding='utf-8') as contacts_file:
        context = {
            'contacts': json.load(contacts_file),
            'title': 'Контакты | Interior - online furniture shopping'
        }
    return render(request, 'mainapp/contact.html', context)


def product(request, pk):
    links_menu = ProductCategory.objects.all()
    context = {
        'product': get_object_or_404(Product, pk=pk),
        'links_menu': links_menu
    }
    return render(request, 'mainapp/product.html', context)
