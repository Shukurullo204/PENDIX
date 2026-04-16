from django import forms

from .models import Ad


class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class AdForm(forms.ModelForm):

    class Meta:
        model = Ad
        fields = (
            'title',
            'category',
            'price',
            'currency',
            'phone',
            'description',
            'latitude',
            'longitude',
        )
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Например: iPhone 15 Pro'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Введите сумму'}),
            'description': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': 'Опишите товар (мин. 80 симв.)',
                }
            ),
            'phone': forms.TextInput(attrs={'placeholder': '+998'}),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user and not self.instance.pk:
            if hasattr(user, 'phone') and user.phone:
                self.fields['phone'].initial = user.phone

        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.HiddenInput):
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f'{existing_classes} form-control'.strip()

    def clean_description(self):
        value = self.cleaned_data.get('description', '')
        normalized = ' '.join(value.split())

        if len(normalized) < 80:
            raise forms.ValidationError('Минимум 80 символов без учёта лишних пробелов')

        return value.strip()