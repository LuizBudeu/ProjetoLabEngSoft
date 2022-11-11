import django_filters
from .models import Voos, Chegadas, Partidas


class VoosFilter(django_filters.FilterSet):  # TODO mudar fields para id?
    # codigo = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Voos
        fields = ['codigo', 'id']
