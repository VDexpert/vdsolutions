from django.core.cache import cache
from django.conf import settings


def cache_object(self):
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

def cache_object_list(self):
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