from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
import datetime

from account.models import User

from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)

class Receipt_No(models.Model):
    user = models.ForeignKey(User, default=User, on_delete=models.CASCADE, null=True)
    receipt_no = models.CharField(max_length=500, unique=True)
    receive_from = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=11)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.receipt_no} - {self.receive_from}"
    
    class meta:
        ordering = ['created_at']

@receiver(post_save, sender=Receipt_No)
def create_receipt(sender, instance, created, **kwargs):
    user = User.objects.get(id = get_current_authenticated_user().id)
    r = Receipt_No.objects.get(id = instance.id)
    
    if created:
        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d = datetime.date(yr,mt,dt)
        current_date = d.strftime("%Y%m%d")
        if instance.id < 10:
            pad_no = "00"
        elif instance.id >=10 and instance.id < 100:
            pad_no = "0"
        else: 
            pad_no = ""
        receipt_no = current_date +"-"+str(get_current_authenticated_user().id)+"-"+pad_no+str(user.number_count)
        r.receipt_no = receipt_no
        r.user = get_current_authenticated_user()

       
        r.save()
    else:
        pass
    user.number_count +=1
    user.save()


class Item(models.Model):
    receipt_no = models.ForeignKey(Receipt_No, on_delete=models.CASCADE, related_name="receiptno")
    item_name = models.CharField(max_length=50)
    item_price = models.IntegerField()
    item_qty = models.IntegerField()
    # sub_total = models.IntegerField()
    def __str__(self):
        return f"{self.item_name} - {self.receipt_no}"

    def get_sub_total(self):
        return self.item_price * self.item_qty
# @receiver(pre_save, sender=Item)
# def create_sub_total(sender, instance, *args, **kwargs):
#     instance.sub_total = instance.item_price * instance.item_qty
