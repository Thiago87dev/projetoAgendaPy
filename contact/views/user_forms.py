from django.shortcuts import render, redirect
from contact.forms import RegisterForm
from django.contrib import messages, auth
from django.contrib.auth.forms import AuthenticationForm

def register(req):
    form = RegisterForm()
    
    if req.method == 'POST':
        form = RegisterForm(req.POST)
        
        if form.is_valid():
            user = form.save()
            messages.success(req, 'Successfully registered user')
            return redirect('contact:login')
            
    context = {
            'form': form,
    }
        
    return render(
        req,
        'contact/register.html',
        context
    )
    
def login_view(req):
    form = AuthenticationForm(req)
    
    if req.method == 'POST':
        form = AuthenticationForm(req, data=req.POST)
        
        if form.is_valid():
            user = form.get_user()
            auth.login(req, user)
            messages.success(req, 'login successful')
            return redirect('contact:index')
        
        messages.error(req, 'Invalid username or password')
    return render(
        req,
        'contact/login.html',
        {'form': form},
    )
    
def logout_view(req):
    auth.logout(req)
    return redirect('contact:login')