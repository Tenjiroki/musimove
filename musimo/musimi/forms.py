from django import forms
from musimi.models import User
from .models import Offer



class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User  
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
    

    
class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['instrument', 'price', 'status']  

    def save(self, commit=True):
        offer = super().save(commit=False)
        if commit:
            offer.save()
        return offer