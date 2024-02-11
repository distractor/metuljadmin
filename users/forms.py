from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.forms import TextInput, NumberInput, CheckboxInput, FileInput, ModelForm

from .models import CustomUser, Message


class DateInput(forms.DateInput):
    input_type = 'date'


class BooleanInput:
    pass


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        social_security_number = cleaned_data.get("social_security_number")
        date_born = cleaned_data.get("date_born")
        date_born_string = "{:02d}{:02d}{}".format(date_born.day, date_born.month, str(date_born.year)[1:])
        if not (date_born_string in str(social_security_number)):
            raise ValidationError("Check your birthday and social security number (EMŠO).")
        return cleaned_data

    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name", "date_born", "street", "city", "zipcode", "phone_number",
                  "social_security_number", "has_zpls", "has_fai", "wants_valid_membership", "paid_membership",
                  "antidoping_certificate")

        widgets = {
            'first_name': TextInput(attrs={'placeholder': 'Andrej'}),
            'last_name': TextInput(attrs={'placeholder': 'Senica'}),
            'email': TextInput(attrs={'placeholder': 'andrej.senica@gmail.com'}),
            'date_born': DateInput(),
            'street': TextInput(attrs={'placeholder': 'Na hribu 6'}),
            'city': TextInput(attrs={'placeholder': 'Rimske Toplice'}),
            'zipcode': NumberInput(attrs={'placeholder': '3272'}),
            'phone_number': TextInput(attrs={'placeholder': '031 680 533'}),
            'social_security_number': TextInput(attrs={'placeholder': '2305987500184'}),
            'has_zpls': CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox', 'style': 'width:20px;'}),
            'has_fai': CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox', 'style': 'width:20px;'}),
            'wants_valid_membership': CheckboxInput(
                attrs={'class': 'form-check-input', 'type': 'checkbox', 'style': 'width:20px;'}),
            "antidoping_certificate": FileInput(),
        }


class CustomUserChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name", "date_born", "street", "city", "zipcode", "phone_number",
                  "social_security_number", "has_zpls", "has_fai", "wants_valid_membership", "antidoping_certificate")

        widgets = {
            'first_name': TextInput(attrs={'placeholder': 'Andrej'}),
            'last_name': TextInput(attrs={'placeholder': 'Senica'}),
            'email': TextInput(attrs={'placeholder': 'andrej.senica@gmail.com'}),
            'date_born': DateInput(),
            'street': TextInput(attrs={'placeholder': 'Na hribu 6'}),
            'city': TextInput(attrs={'placeholder': 'Rimske Toplice'}),
            'zipcode': NumberInput(attrs={'placeholder': '3272'}),
            'phone_number': TextInput(attrs={'placeholder': '031 680 533'}),
            'social_security_number': TextInput(attrs={'placeholder': '2305987500184'}),
            'has_zpls': CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox', 'style': 'width:20px;'}),
            'has_fai': CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox', 'style': 'width:20px;'}),
            'wants_valid_membership': CheckboxInput(
                attrs={'class': 'form-check-input', 'type': 'checkbox', 'style': 'width:20px;'}),
            'paid_membership': CheckboxInput(
                attrs={'class': 'form-check-input', 'type': 'checkbox', 'style': 'width:20px;'}),
            "antidoping_certificate": FileInput(),
        }


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ("emails", "subject", "message")

        widgets = {
            'emails': TextInput(attrs={'placeholder': 'Send to'}),
            'subject': TextInput(attrs={'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'rows': 4, 'cols': '100%', 'placeholder': 'Message'}),
        }
