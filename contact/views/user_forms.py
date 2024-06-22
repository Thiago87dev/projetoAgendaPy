from django.shortcuts import render, redirect
from contact.forms import RegisterForm, UserUpdateForm
from django.contrib import messages, auth
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

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
            'btn_text': 'Create',
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
        {'form': form,
         'btn_text': 'Login'
        },
        
    )

@login_required(login_url='contact:login')
def logout_view(req):
    auth.logout(req)
    return redirect('contact:index')

@login_required(login_url='contact:login')
def user_update(req):
    form = UserUpdateForm(instance=req.user)
    
    if req.method != 'POST':
        return render(
            req,
            'contact/user-update.html',
            {'form': form,
             'btn_text': 'Update'
            }
        )
    
    form = UserUpdateForm(data=req.POST, instance=req.user)
    
    if not form.is_valid():
        return render(
            req,
            'contact/user-update.html',
            {'form': form,
             'btn_text': 'Update'
            }
        )
    
    form.save()
    return redirect('contact:user_update')