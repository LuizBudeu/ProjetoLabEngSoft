import django_filters
from .models import Voos, Chegadas, Partidas


class VoosFilter(django_filters.FilterSet):  # TODO mudar fields para id?
    # codigo = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Voos
        fields = ['codigo', 'id']

class ChegadasFilter(django_filters.FilterSet):
    # codigo = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Chegadas
        fields = ['codigo']
    
class PartidasFilter(django_filters.FilterSet):
    # codigo = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Partidas
        fields = ['codigo']
    
