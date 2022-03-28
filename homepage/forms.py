from django import forms


class EmailForm(forms.Form):
    email = forms.EmailField(required=True, label='', widget=forms.EmailInput(attrs={'placeholder': 'Email',
                                                                                     'class': 'form-control'}))
