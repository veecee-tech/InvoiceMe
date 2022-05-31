from django.shortcuts import redirect, render
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
from account.models import User
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse
from .forms import UserProfileForm
# Create your views here.


def login(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        account_number = request.POST.get('account_number')
        password = request.POST.get('password')

        user = auth.authenticate(account_number = account_number, password = password)

        if user is not None:
            auth.login(request,user)
            return redirect('dashboard')
        else:
            messages.error(request, 'invalid username or password')
            return redirect('login')
    return render(request, 'auth/login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('home')

@login_required(login_url='login')
def change_password(request):

    user = User.objects.get(account_number__exact = request.user.account_number)

    if request.method == 'POST':

        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        success = user.check_password(old_password)

        if success:
            if new_password == confirm_password:
                user.set_password(new_password)
                update_session_auth_hash(request, user)
                user.save()
                messages.error(request, "password changed successfully")
                return redirect('change_password')
            else:
                messages.error(request, "password mismatch")
                return redirect('change_password')

        else:
            messages.error(request, "invalid old password")
            return redirect('change_password')
    return render(request, 'auth/change_password.html')



@login_required 
def user_profile_view(request):
    forms = UserProfileForm(instance=request.user.userprofile)
    
    if request.method == "POST":
        forms =UserProfileForm(request.POST, request.FILES or None, instance=request.user.userprofile)

        if forms.is_valid():
            forms.save()
            messages.success(request, "Profile Updated successfully")
            return redirect("update-profile")

    context = {
        "forms": forms,
    }
    return render(request, "userprofile.html", context)
