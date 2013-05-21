Простое приложение для django-shop которое генерит YML файл, для Яндекс.Маркета

Использование:
python manage.py create_yml > market.xml

Настройки:
В settings.py добавить

YML_CONFIG = {
    'name':'Название магазина',
    'company':u'Название компании',
    'url':'http://example.com',
    'currencies':(
                    {'id':"RUR", 'rate':"1"},
        ),
    'category_model':'tshirt.tshop.models.Category',
    'local_delivery_cost':u'Бесплатно в Москве',
}

