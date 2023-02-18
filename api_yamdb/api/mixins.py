from rest_framework import mixins, viewsets


class RetrieveDisabledMixin(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    Кастомный mixin,
    отключающий возможность получения и обновления
    одного объекта (retrieve и patch).
    """
    pass
