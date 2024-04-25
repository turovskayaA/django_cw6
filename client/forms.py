from django import forms

from client.models import ServiceClient, Message, Newsletter


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class NewsletterForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Newsletter
        fields = '__all__'


class ServiceClientForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = ServiceClient
        fields = '__all__'


class MessageForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Message
        fields = '__all__'


class NewsletterModeratorForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Newsletter
        fields = ('is_activated',)
