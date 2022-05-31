from django import forms
from .models import Receipt_No, Item
from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['receipt_no','item_name', 'item_price', 'item_qty']
    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args,**kwargs)    
        self.fields['receipt_no'].queryset = Receipt_No.objects.filter(user_id = get_current_authenticated_user().id).order_by('-created_at')
        self.fields['item_name'].widget.attrs['placeholder'] = 'item Name'
        self.fields['item_price'].widget.attrs['placeholder'] = 'Item Price'
        self.fields['item_qty'].widget.attrs['placeholder'] = 'Item Quantity'     
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == "receipt_no":
    #         kwargs["queryset"] = Receipt_No.objects.filter(user_id = get_current_authenticated_user().id)
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)

class ReceiptForm(forms.ModelForm):
    class Meta:
        model = Receipt_No
        
        fields = ['receive_from', 'address', 'phone']

    def __init__(self, *args, **kwargs):
        super(ReceiptForm, self).__init__(*args,**kwargs)
        
        self.fields['receive_from'].widget.attrs['placeholder'] = 'Received From'
        self.fields['address'].widget.attrs['placeholder'] = 'address'
        self.fields['phone'].widget.attrs['placeholder'] = 'phone'
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'