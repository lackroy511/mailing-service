from django import forms

from client_management.models import Client


class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'surname', 'email', 'comment')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя клиента',
                }),

            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Фамилия клиента',
                }),

            'surname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Отчество клиента',
                }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Электронная почта клиента',
                }),

            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ваш комментарий',
                'rows': 2,
                }),
        }
