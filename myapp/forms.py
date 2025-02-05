from django import forms
from django.forms import inlineformset_factory, modelformset_factory
from django.core.exceptions import ValidationError
from .models import User, PaymentCard, Product, ProductImage, ProductAvatar
from django.forms.widgets import ClearableFileInput
class CustomClearableFileInput(ClearableFileInput):
    template_name = "widgets/custom_clearable_file_input.html"

class RegistrationForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Пароли не совпадают.")

        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с такой почтой уже существует.")
        return email


class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'birth_date', 'profile_picture']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['name'].initial = self.instance.name
            self.fields['email'].initial = self.instance.email
            self.fields['birth_date'].initial = self.instance.birth_date

    def save(self, commit=True):
        user = super(UserUpdateForm, self).save(commit=False)
        if 'profile_picture' in self.files:
            user.profile_picture = self.files['profile_picture']
        if commit:
            user.save()
        return user


class AddPaymentCardForm(forms.Form):
    card_number = forms.CharField(max_length=19, required=True, widget=forms.TextInput(attrs={'placeholder': '1234 5678 1234 5678', 'maxlength': '19'}))
    card_holder_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Имя держателя карты'}))
    expiration_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    cvv = forms.CharField(max_length=3, required=True, widget=forms.TextInput(attrs={'placeholder': 'CVV', 'maxlength': '3'}))


class DeletePaymentCardForm(forms.Form):
    card = forms.ModelChoiceField(queryset=PaymentCard.objects.none(), empty_label=None, label='Номер карты')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(DeletePaymentCardForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['card'].queryset = PaymentCard.objects.filter(user_id=user)
            self.fields['card'].label_from_instance = lambda obj: obj.card_number


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category']
        labels = {
            'name': 'Название товара',
            'description': 'Описание',
            'price': 'Стоимость',
            'category': 'Категория',
        }


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']
        labels = {'image': 'Изображение товара',}
        widgets = {'image': CustomClearableFileInput(), }


ProductImageFormSet = modelformset_factory(
    ProductImage,
    form=ProductImageForm,
    extra=1,

)


class ProductAvatarForm(forms.ModelForm):
    class Meta:
        model = ProductAvatar
        fields = ['image']
        labels = {'image': 'Аватарка товара',}
        widgets = {'image': CustomClearableFileInput(),}


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, label='Старый пароль')
    new_password = forms.CharField(widget=forms.PasswordInput, label='Новый пароль')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Повторите новый пароль')

    def __init__(self, user, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get("old_password")
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if not self.user.check_password(old_password):
            raise forms.ValidationError("Неверный старый пароль")

        if new_password != confirm_password:
            raise forms.ValidationError("Новый пароль и его подтверждение не совпадают")

        return cleaned_data

