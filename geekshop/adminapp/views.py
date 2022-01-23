from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from adminapp.forms import ShopUserAdminEditForm, ProductCategoryForm, ProductForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import Product, ProductCategory


class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users_list.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # Это функция для того что бы показать только обычные пользователи
    # def get_queryset(self):
    #     return ShopUser.objects.filter(is_superuser=True)


class UsersCreateView(CreateView):
    model = ShopUser
    template_name = 'adminapp/user_form.html'
    # fields = '__all__'
    form_class = ShopUserRegisterForm
    success_url = reverse_lazy('adminapp:users')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UsersUpdateView(UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_form.html'
    # fields = '__all__'
    form_class = ShopUserAdminEditForm
    success_url = reverse_lazy('adminapp:users')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UsersDeleteView(DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('adminapp:users')

    # def delete(self, *args, **kwargs):
    #     self.object = self.get_object()
    #     self.object.is_active = False
    #     self.object.save()
    #
    #     return HttpResponseRedirect(self.success_url)

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class ProductCategoryListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/categories_list.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_form.html'
    # fields = '__all__'
    form_class = ProductCategoryForm
    success_url = reverse_lazy('adminapp:categories')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_form.html'
    # fields = '__all__'
    form_class = ProductCategoryForm
    success_url = reverse_lazy('adminapp:categories')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('adminapp:categories')

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.success_url)

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):
    category_item = get_object_or_404(ProductCategory, pk=pk)
    context = {
        'object_list': Product.objects.filter(category__pk=pk),
        'object': category_item
    }

    return render(request, 'adminapp/products_list.html', context)


# class ProductListView(ListView):
#     model = Product
#     template_name = 'adminapp/products_list.html'
#
#     def get_success_url(self):
#         product_id = self.kwargs.get('pk')
#         product = get_object_or_404(Product, pk=product_id)
#         return reverse_lazy('adminapp:products', args=[product.category.pk])
#
#     @method_decorator(user_passes_test(lambda u: u.is_superuser))
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)

class ProductCreateView(CreateView):
    model = Product
    template_name = 'adminapp/product_form.html'
    form_class = ProductForm

    def get_success_url(self):
        product_pk = self.kwargs.get('pk')
        product = get_object_or_404(Product, pk=product_pk)
        return reverse_lazy('adminapp:products', args=[product.category.pk])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if self.request.method == 'GET':
            pk = self.kwargs.get('pk')
            category_item = get_object_or_404(ProductCategory, pk=pk)
            context_data['category'] = category_item
        return context_data

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'adminapp/product_form.html'
    # fields = '__all__'
    form_class = ProductForm

    def get_success_url(self):
        product_pk = self.kwargs.get('pk')
        product = get_object_or_404(Product, pk=product_pk)
        return reverse_lazy('adminapp:products', args=[product.category.pk])

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'

    def get_success_url(self):
        product_id = self.kwargs.get('pk')
        product = get_object_or_404(Product, pk=product_id)
        return reverse_lazy('adminapp:products', args=[product.category.pk])

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'
