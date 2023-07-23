from django import forms

from mailing_management.models import Mailing, MailingSettings


class MailingForm(forms.ModelForm):

    class Meta:
        model = Mailing
        fields = ('massage_subject', 'massage_text')
        widgets = {
            'massage_subject': forms.TextInput(attrs={
                'class': 'form-control',
            }),

            'massage_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
            }),
        }


class MailingSettingsForm(forms.ModelForm):

    class Meta:
        model = MailingSettings
        fields = ('mailing_time', 'mailing_periodicity')
        widgets = {
            'mailing_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control',
            }),

            'mailing_periodicity': forms.Select(attrs={
                'class': 'form-control',
            }),
        }
