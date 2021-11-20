from django.shortcuts import render


def index(request):
    context = {
        'custom_user': [
            {
                'name': 'Ilhomjon',
                'age': 25
            },
            {
                'name': 'Akhrorbek',
                'age': 22
            }
        ],
        'title': 'Главная | Interior - online furniture shopping'
    }
    return render(request, 'mainapp/index.html', context)


links_menu = [
    {'href': 'products', 'name': 'Все'},
    {'href': 'products_home', 'name': 'Дом'},
    {'href': 'products_modern', 'name': 'Модерн'},
    {'href': 'products_office', 'name': 'Оффис'},
    {'href': 'products_classic', 'name': 'Классика'},
]


def products(request):
    context = {
        'links_menu': links_menu,
        'title': 'Продукты | Interior - online furniture shopping'
    }
    return render(request, 'mainapp/products.html', context)


def products_home(request):
    context = {
        'links_menu': links_menu,
        'title': 'Дом | Interior - online furniture shopping'
    }
    return render(request, 'mainapp/products.html', context)


def products_modern(request):
    context = {
        'links_menu': links_menu,
        'title': 'Модерн | Interior - online furniture shopping'
    }
    return render(request, 'mainapp/products.html', context)


def products_office(request):
    context = {
        'links_menu': links_menu,
        'title': 'Оффис | Interior - online furniture shopping'
    }
    return render(request, 'mainapp/products.html', context)


def products_classic(request):
    context = {
        'links_menu': links_menu,
        'title': 'Классика | Interior - online furniture shopping'
    }
    return render(request, 'mainapp/products.html', context)


def contact(request):
    context = {
        'title': 'Контакты | Interior - online furniture shopping'
    }
    return render(request, 'mainapp/contact.html', context)
