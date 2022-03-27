from django import forms


class EmailForm(forms.Form):
    email = forms.EmailField(required=True, label='',widget=forms.EmailInput(attrs={'placeholder': 'Email',
                                                                                    'style': 'width: 300px',
                                                                                    'class': 'form-control'}))
