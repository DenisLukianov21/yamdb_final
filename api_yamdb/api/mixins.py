from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import PageNumberPagination

from .permissions import IsAuthorModeratorAdminOrReadOnly


class CreateListDestroyMixin(mixins.CreateModelMixin,
                             mixins.ListModelMixin,
                             mixins.DestroyModelMixin,
                             viewsets.GenericViewSet,):
    """Вьюсет для осуществления GET, POST и DELETE запросов."""
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)
    pagination_class = PageNumberPagination
