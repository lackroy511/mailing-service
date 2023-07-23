from django import forms

from mail_sender.models import Mailing, MailingSettings


class MailingForm(forms.ModelForm):

    massage_subject = forms.CharField(
        label='Тема', widget=forms.TextInput(attrs={'class': 'form-control'}))
    massage_text = forms.CharField(label='Текст', widget=forms.Textarea(
        attrs={'class': 'form-control', 'rows': 3}))

    class Meta:
        model = Mailing
        fields = ('massage_subject', 'massage_text')


class MailingSettingsForm(forms.ModelForm):

    mailing_time = forms.TimeField(label='Время рассылки',
                                   widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}))
    mailing_periodicity = forms.ChoiceField(label='Периодичность рассылки',
                                            choices=MailingSettings.MAILING_PERIODICITY_CHOICES,
                                            widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = MailingSettings
        fields = ('mailing_time', 'mailing_periodicity')
