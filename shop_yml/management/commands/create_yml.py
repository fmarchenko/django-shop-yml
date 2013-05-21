# -*- coding: utf-8 -*-
from lxml import etree
import progressbar
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from django.utils.importlib import import_module
from django.conf import settings
from shop.models.productmodel import Product


YML_CONFIG = settings.YML_CONFIG

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        count = Product.objects.filter(active=True).count()
        self.bar = progressbar.ProgressBar(maxval=count, widgets=['Creating:', progressbar.Percentage()]).start()
        root = etree.Element('yml_catalog', date=datetime.today().strftime("%Y-%m-%d %H-%M"))
        shop = etree.SubElement(root, 'shop')
        
        etree.SubElement(shop, 'name').text = YML_CONFIG['name']
        etree.SubElement(shop, 'company').text = YML_CONFIG['company']
        etree.SubElement(shop, 'url').text = YML_CONFIG['url']
        
        currencies = etree.SubElement(shop, 'currencies')
        for currency in YML_CONFIG['currencies']:
            etree.SubElement(currencies, 'currency', rate=currency['rate'], id=currency['id'])

        self.set_categories(shop)

        etree.SubElement(shop, 'local_delivery_cost').text = YML_CONFIG['local_delivery_cost']
        
        self.set_products(shop)
        
        print etree.tostring(root)

    def set_categories(self, shop):
        class_path = YML_CONFIG['category_model']
        
        class_module, class_name = class_path.rsplit('.', 1)
        mod = import_module(class_module)
        clazz = getattr(mod, class_name)
        categories_tag = etree.SubElement(shop, 'categories')
        for category in clazz.objects.all():
            etree.SubElement(categories_tag, 'category', id=str(category.id)).text = category.get_name()

    def set_products(self, shop):
        offers = etree.SubElement(shop,'offers')
        i = 0
        for product in Product.objects.filter(active=True):
            offer = etree.SubElement(offers,'offer', id=str(product.id), available="true")
            etree.SubElement(offer,'url').text =  YML_CONFIG['url'] + product.get_absolute_url()
            etree.SubElement(offer,'price').text =  str(product.get_price())
            etree.SubElement(offer,'currencyId').text =  product.get_currency()
            etree.SubElement(offer,'categoryId').text =  str(product.category.id)
            etree.SubElement(offer,'picture').text = YML_CONFIG['url'] + product.head_image.url
            etree.SubElement(offer,'delivery').text = "true"
            etree.SubElement(offer,'name').text = product.get_name()
            i += 1
            self.bar.update(i)