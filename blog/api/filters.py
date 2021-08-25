from django_filters.rest_framework import DjangoFilterBackend


class BlogCustomFilter(DjangoFilterBackend):
    pass

    # def get_filterset_kwargs(self, view, request, *args, **kwargs):
    #     print(kwargs)
    #     filter_kwargs = super().get_filterset_kwargs(view, request, **kwargs)
    #     print(filter_kwargs)
    #     if filter_kwargs.get('category__name'):
    #         filter_kwargs['category__name'] = 'category'

    #     if filter_kwargs.get('user__username'):
    #         filter_kwargs['category__name'] = 'username'

    #     return filter_kwargs
