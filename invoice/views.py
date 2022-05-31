
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .forms import ItemForm, ReceiptForm
from .models import Receipt_No, Item

from account.models import UserProfile
# Create your views here.

@login_required(login_url='login')
def generate_receipt(request):
    userprofile = UserProfile.objects.get(user_id = request.user.id)
    if not userprofile.business_name:
        messages.error(request, "You need to update your profile first")
        return redirect("update-profile")
        
    if request.method == 'POST':
        form = ReceiptForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('add_item')
    else:
        form = ReceiptForm()
    context = {
        'form': form
    }
    return render(request, 'receipt-form.html', context)

@login_required(login_url='login')
def all_invoice(request):

    userprofile = UserProfile.objects.get(user_id = request.user.id)
    if not userprofile.business_name:
        messages.error(request, "You need to update your profile first")
        return redirect("update-profile")

    all_invoice = Receipt_No.objects.filter(user = request.user).order_by('-created_at')

    context = {
        'all_invoice': all_invoice
    }

    return render(request, 'all-receipts.html', context)
    

@login_required(login_url='login')
def single_invoice(request, id, receipt_no):

    userprofile = UserProfile.objects.get(user_id = request.user.id)
    if not userprofile.business_name:
        messages.error(request, "You need to update your profile first")
        return redirect("update-profile")

    single_invoice = get_object_or_404(Receipt_No, user = request.user, id=id, receipt_no = receipt_no)
    items = Item.objects.filter(receipt_no_id = id)

    total = 0
    for item in items:
        total += item.get_sub_total()
    

    context = {
        'single_invoice': single_invoice,
        'items': items,
        'total': total,
       
    }
    return render(request, 'single_invoice_view.html', context)


@login_required(login_url='login')
def add_items(request):

    userprofile = UserProfile.objects.get(user_id = request.user.id)
    if not userprofile.business_name:
        messages.error(request, "You need to update your profile first")
        return redirect("update-profile")

    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
           
            form.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = ItemForm()
    context = {
        'form': form
    }
    return render(request, 'item-form.html', context)

@login_required(login_url='login')
def receipt_items(request, receipt_no):

    userprofile = UserProfile.objects.get(user_id = request.user.id)
    if not userprofile.business_name:
        messages.error(request, "You need to update your profile first")
        return redirect("update-profile")

    all_items = Item.objects.filter(receipt_no__receipt_no = receipt_no)
    context = {
        'all_items': all_items,
    }

    return render(request,'receipt-items.html', context)

#delete invoice
@login_required(login_url='login')
def delete_invoice(request, id):

    userprofile = UserProfile.objects.get(user_id = request.user.id)
    if not userprofile.business_name:
        messages.error(request, "You need to update your profile first")
        return redirect("update-profile")

    invoice = Item.objects.get(id=id)

    invoice.delete()
    # invoice.save()

    return redirect('all_invoice')

