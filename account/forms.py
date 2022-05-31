from django import forms
from .models import User, UserProfile
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UserLoginForm(forms.Form):
    account_number = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Account Number"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}))

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['account_number', 'email', 'password','password_2', 'phone']

    def clean_account_number(self):

        account_number = self.cleaned_data.get('account_number')
        qs = User.objects.filter(account_number=account_number)

        if qs.exists():
            raise forms.ValidationError("account number already exists")
            
        return account_number

    def clean(self):

        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")

        if password is not None and password != password_2:
            self.add_error("password_2", "Your password must match")
        return cleaned_data

    def save(self,commit=True):
        user = super().save(commit=False)
        
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['account_number', 'email', 'phone', 'is_admin', 'is_staff', 'is_active']

    def clean_account_number(self):

        account_number = self.cleaned_data.get('account_number')
        qs = User.objects.filter(account_number=account_number)

        if qs.exists():
            raise forms.ValidationError("account number already exists")
        return account_number

    def clean_email(self):

        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)

        if qs.exists():
            raise forms.ValidationError("email already exists")
        return email

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['account_number','email', 'password', 'phone', 'is_admin', 'is_active', 'is_staff']

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']
        fields = "__all__"
