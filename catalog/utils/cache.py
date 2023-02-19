from django.core.cache import cache
from django.conf import settings


def cache_object_detail(obj, model):
    queryset = model.objects.get(id=obj.pk)

    if settings.CACHE_ENABLED:
        if model.__сlass__.__name__ == 'Product':
            key = f'product_{obj.pk}'

        if model.__сlass__.__name__ == 'Post':
            key = f'post_{obj.pk}'

        cache_data = cache.get(key)

        if cache_data is None:
            cache_data = queryset
            cache.set(key, cache_data)
            print(f'занесен объект{key} в кэш')

            return cache_data

        print(f'вернулись закэшированные данные объекта {obj}')
        return queryset


def cache_all_object_list(model):
    queryset = model.objects.all().filter(id=self.object.pk)

    if settings.CACHE_ENABLED:

        if model.__сlass__.__name__ == 'Product':
            key = f'product_list_{obj.pk}'

        if model.__сlass__.__name__ == 'Post':
            key = f'post_list_{obj.pk}'

        cache_data = cache.get(key)

        if cache_data is None:
            cache_data = queryset
            cache.set(key, cache_data)
            print(f'занесен объект{key} в кэш')

            return cache_data

        print(f'вернулись закэшированные данные объекта {self.object.pk}')
        return queryset


def cache__user_object_list(self):
    queryset = self.model.objects.get(id=self.object.pk)

    if settings.CACHE_ENABLED:
        key = f'product_{self.object.pk}'
        cache_data = cache.get(key)

        if cache_data is None:
            cache_data = queryset
            cache.set(key, cache_data)
            print(f'занесен объект{key} в кэш')

            return cache_data

        print(f'вернулись закэшированные данные объекта {self.object.pk}')
        return queryset