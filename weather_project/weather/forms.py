from django import forms

from .models import SearchHistory


class SearchCityForm(forms.ModelForm):
    """Форма поиска города по названию."""

    class Meta:
        model = SearchHistory
        fields = ('city_name',)
