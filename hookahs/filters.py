import django_filters
from django_filters import CharFilter
from .models import Hookah, Category, Flavor


class ProductFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())
    flavors = django_filters.ModelMultipleChoiceFilter(queryset=Flavor.objects.all(), method='filter_flavors')

    class Meta:
        model = Hookah
        fields = ['category', 'flavors', 'name']

    def filter_flavors(self, queryset, name, value):
        if 'category' in self.data and self.data['category']:
            category = Category.objects.get(pk=self.data['category'])
            if 'Табак' in category.name:
                if not value:
                    return queryset.filter(category=category).distinct()
                return queryset.filter(flavors__in=value).distinct()
        return queryset
