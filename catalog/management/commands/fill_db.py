from django.core.management import BaseCommand
from catalog.models import*
from catalog.auxfunc import translit, plugs


class Command(BaseCommand):
    def handle(self, *args, **options):
        Product.objects.all().delete()
        Category.objects.all().delete()

        categories = [
            {'category_name': 'Автоматизация', 'description_for_products': f'Полное описание категории для каталога Программы для автоматизации различных бизнес-процессов\n{plugs.text()}',
             'annotation_products': 'Аннотация для каталога Программы для автоматизации различных бизнес-процессов',
             'annotation_posts': 'Аннотация для блога Программы для автоматизации различных бизнес-процессов',
             'description_for_posts': f'Полное описание категории для блога Программы для автоматизации различных бизнес-процессов\n{plugs.text()}'},

            {'category_name': 'Парсинг', 'description_for_products': f'Полное описание категории для каталога Программы для парсинга больших баз данных{plugs.text()}',
             'annotation_products': 'Аннотация для каталога Программы для парсинга больших баз данных',
             'annotation_posts': 'Аннотация для блога Программы для парсинга больших баз данных',
             'description_for_posts': f'Полное описание категории для блога Программы для парсинга больших баз данных\n{plugs.text()}'},

            {'category_name': 'Нейронные сети', 'description_for_products': f'Полное описание категории для каталога Программы, использующие в своей работе технологии искусственного интеллекте\n{plugs.text()}',
             'annotation_products': 'Аннотация для каталога Программы, использующие в своей работе технологии искусственного интеллекте',
             'annotation_posts': 'Аннотация для блога Программы, использующие в своей работе технологии искусственного интеллекте}',
             'description_for_posts': f'Полное описание категории для блога Программы, использующие в своей работе технологии искусственного интеллекте\n{plugs.text()}'}
        ]

        categories_list = []

        for item in categories:
            categories_list.append(Category(category_name=item['category_name'], slug=translit.do(item['category_name']),
                                            annotation_for_products=item['annotation_products'],
                                            annotation_for_posts=item['annotation_posts'],
                                            description_for_posts=item['description_for_posts'],
                                            description_for_products=item['description_for_products'],
                                            )
                                   )

        Category.objects.bulk_create(categories_list)

        id_auto = Category.objects.get(category_name='Автоматизация')
        id_parsing = Category.objects.get(category_name='Парсинг')
        id_art_int = Category.objects.get(category_name='Нейронные сети')

        products = [
            {'product_name': 'Продажи для агентств недвижимости', 'description': plugs.text(), 'user': User.objects.all().get(id=1),
             'category': id_auto, 'unit_price': '85000', 'slug': translit.do('Продажи для агентств недвижимости'), 'annot': f'''Аннотация {plugs.text()[:140]}'''},
            {'product_name': 'Клиентская поддержка для веб-студий', 'description': plugs.text(), 'user': User.objects.all().get(id=1),
             'category': id_auto, 'unit_price': '3500', 'slug': translit.do('Клиентская поддержка для веб-студий'), 'annot': f'''Аннотация {plugs.text()[:140]}'''},
            {'product_name': 'Тендерная площадка для агрохолдингов', 'description': plugs.text(), 'user': User.objects.all().get(id=1),
             'category': id_auto, 'unit_price': '55000', 'slug': translit.do('Тендерная площадка для агрохолдингов'), 'annot': f'''Аннотация {plugs.text()[:140]}'''},
            {'product_name': 'Поиск вакансий по ключу', 'description': plugs.text(), 'user': User.objects.all().get(id=2),
             'category': id_parsing, 'unit_price': '150', 'slug': translit.do('Поиск вакансий по ключу'), 'annot': f'''Аннотация {plugs.text()[:140]}'''},
            {'product_name': 'Поиск аккаунтов Вконтакте', 'description': plugs.text(), 'user': User.objects.all().get(id=2),
             'category': id_parsing, 'unit_price': '300', 'slug': translit.do('Поиск аккаунтов Вконтакте'), 'annot': f'''Аннотация {plugs.text()[:140]}'''},
            {'product_name': 'Поиск недвижимости', 'description': plugs.text(), 'user': User.objects.all().get(id=2),
             'category': id_parsing,'unit_price': '540', 'slug': translit.do('Поиск недвижимости'), 'annot': f'''Аннотация {plugs.text()[:140]}'''},
            {'product_name': 'Бизнес рассылки с ИИ', 'description': plugs.text(), 'user': User.objects.all().get(id=3),
             'category': id_art_int, 'unit_price': '5000', 'slug': translit.do('Бизнес рассылки с ИИ'), 'annot': f'''Аннотация {plugs.text()[:140]}'''},
            {'product_name': 'Создание рекламных объявлений ИИ', 'description': plugs.text(), 'user': User.objects.all().get(id=3),
             'category': id_art_int, 'unit_price': '3500', 'slug': translit.do('Создание рекламных объявлений ИИ'), 'annot': f'''Аннотация {plugs.text()[:140]}'''},
            {'product_name': 'Расчет сопромата с ИИ', 'description': plugs.text(), 'user': User.objects.all().get(id=3),
             'category': id_art_int, 'unit_price': '3500', 'slug': translit.do('Расчет сопромата с ИИ'), 'annot': f'''Аннотация {plugs.text()[:140]}'''},
        ]

        products_list = []
        for i in range(11):
            for item in products:
                products_list.append(
                    Product(product_name=f'''{item['product_name']}-{i}''', description=item['description'], user=item['user'],
                            category=item['category'], unit_price=item['unit_price'],  slug=f'''{item['slug']}-{i}''', prod_annotation=item['annot']))

        Product.objects.bulk_create(products_list)

        posts = [
            {'title': 'Сколько средств вы должны выделить на ERP?', 'user': User.objects.all().get(id=1), 'category': Category.objects.all().get(id=1),
             'slug': translit.do('Сколько средств вы должны выделить на ERP?'), 'content': plugs.text()},
            {'title': '5 лучших программ для управления бухгалтерскими документами', 'user': User.objects.all().get(id=1), 'category': Category.objects.all().get(id=1),
             'slug': translit.do('5 лучших программ для управления бухгалтерскими документами'), 'content': plugs.text()},
            {'title': 'Топ-5 программных продуктов ERP с открытым исходным кодом', 'user': User.objects.all().get(id=1), 'category': Category.objects.all().get(id=1),
             'slug': translit.do('Топ-5 программных продуктов ERP с открытым исходным кодом'), 'content': plugs.text()},
            {'title': 'Электронный документооборот (ЭДО): какие бывают виды, как работает, особенности, функции', 'user': User.objects.all().get(id=2), 'category': Category.objects.all().get(id=2),
             'slug': translit.do('Электронный документооборот (ЭДО): какие бывают виды, как работает, особенности, функции'), 'content': plugs.text()},
            {'title': 'CRM-системы для малого бизнеса: какую выбрать, обзор лучших', 'user': User.objects.all().get(id=2), 'category': Category.objects.all().get(id=2),
             'slug': translit.do('CRM-системы для малого бизнеса: какую выбрать, обзор лучших'), 'content': plugs.text()},
            {'title': 'Как перейти на электронный документооборот (ЭДО)', 'user': User.objects.all().get(id=2), 'category': Category.objects.all().get(id=2),
             'slug': translit.do('Как перейти на электронный документооборот (ЭДО)'), 'content': plugs.text()},
            {'title': 'CRM-системы для агентства недвижимости: лучшие программы для риэлторов', 'user': User.objects.all().get(id=3), 'category': Category.objects.all().get(id=3),
             'slug': translit.do('CRM-системы для агентства недвижимости: лучшие программы для риэлторов'), 'content': plugs.text()},
            {'title': 'Система электронного документооборота EDI: платформа для обмена данными', 'user': User.objects.all().get(id=3), 'category': Category.objects.all().get(id=3),
             'slug': translit.do('Система электронного документооборота EDI: платформа для обмена данными'), 'content': plugs.text()},
            {'title': 'Бухгалтерские программы: список программного обеспечения для ведения бухгалтерии', 'user': User.objects.all().get(id=3), 'category': Category.objects.all().get(id=3),
             'slug': translit.do('Бухгалтерские программы: список программного обеспечения для ведения бухгалтерии'), 'content': plugs.text()},
        ]
        post_list = []
        for i in range(11):
            for item in posts:
                post_list.append(
                    Post(title=f'''{item['title']}-{i}''', content=item['content'],
                         slug=f'''{item['slug']}-{i}''', user=item['user'], category=item['category']))

        Post.objects.bulk_create(post_list)
