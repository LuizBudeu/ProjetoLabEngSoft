import django_filters
from .models import Voos, Chegadas, Partidas


class VooFilter(django_filters.FilterSet):
    # codigo = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Voos
        fields = ['codigo']
