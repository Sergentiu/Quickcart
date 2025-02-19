from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UsernameChangeForm, EmailChangeForm
from cart.models import Order

@login_required
def profile_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-date').prefetch_related('items')  # Fetch user's order history
    context = {
        "user": request.user,
        "orders": orders,
    }
    
    return render(request, "profile.html", context)

def register_view(request):
    pass

@login_required
def change_username(request):
    if request.method == 'POST':
        form = UsernameChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()  # Save the new username
            return redirect('profile_url')
    else:
        form = UsernameChangeForm(instance=request.user)
    
    return render(request, 'change_username.html', {'form': form})

@login_required
def change_email(request):
    if request.method == 'POST':
        form = EmailChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()  # Save the new email
            return redirect('profile_url')
    else:
        form = EmailChangeForm(instance=request.user)
    
    return render(request, 'change_email.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep the user logged in after password change
            return redirect('profile_url')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'change_password.html', {'form': form})