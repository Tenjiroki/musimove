from django import forms
from musimi.models import User
from .models import Offer



class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Підтвердіть пароль")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Паролі не збігаються.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    

    
class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['instrument', 'price', 'status']  

    def save(self, commit=True):
        offer = super().save(commit=False)
        if commit:
            offer.save()
        return offer