from django import forms
from .models import Order

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'address', 'city', 'state', 'zip_code', 'country'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user and user.is_authenticated:
            # Pre-fill form with user profile data if available
            if hasattr(user, 'profile'):
                profile = user.profile
                self.fields['first_name'].initial = user.first_name
                self.fields['last_name'].initial = user.last_name
                self.fields['email'].initial = user.email
                if profile.phone_number:
                    self.fields['phone'].initial = profile.phone_number
                if profile.address:
                    self.fields['address'].initial = profile.address
                if profile.city:
                    self.fields['city'].initial = profile.city
                if profile.state:
                    self.fields['state'].initial = profile.state
                if profile.zip_code:
                    self.fields['zip_code'].initial = profile.zip_code
                if profile.country:
                    self.fields['country'].initial = profile.country
