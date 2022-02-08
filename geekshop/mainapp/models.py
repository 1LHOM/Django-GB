from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='Называние')
    description = models.TextField(verbose_name='Описание')
    is_active = models.BooleanField(default=True, verbose_name='Статус активности')

    def __str__(self):
        return self.name

    # Мы можем определить свой метод удаления категорий
    # мы этот метод переодределили и в views поэтому закомментируем
    # один из этих методов что бы не было конфлик между этими функчиями
    # def delete(self, *args, **kwargs):
    #     self.is_active = False
    #     self.save()


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, verbose_name='Называние')
    image = models.ImageField(upload_to='products/', blank=True)
    short_desc = models.CharField(max_length=255, blank=True)
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Цена', default=0)
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Количество')
    is_active = models.BooleanField(db_index=True, verbose_name='категория активна', default=True)

    def __str__(self):
        return f'{self.name} ({self.category})'

    # Мы можем определить свой метод удаления продуктов
    # мы этот метод переодределили и в views поэтому закомментируем
    # один из этих методов что бы не было конфлик между этими функчиями
    # def delete(self, *args, **kwargs):
    #     self.is_active = False
    #     self.save()
