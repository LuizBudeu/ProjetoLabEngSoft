import django_filters
from .models import Voos


class VoosFilter(django_filters.FilterSet):  
    # codigo = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Voos
        fields = ['codigo', 'id']

class VoosFilterRead(django_filters.FilterSet):  
    # codigo = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Voos
        fields = ['codigo', 'id']
