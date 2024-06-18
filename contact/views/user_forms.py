from django.shortcuts import render
from contact.forms import RegisterForm



def register(req):
    form = RegisterForm()
    
    if req.method == 'POST':
        form = RegisterForm(req.POST)
        
        if form.is_valid():
            user = form.save()
            
    context = {
            'form': form,
    }
        
    return render(
        req,
        'contact/register.html',
        context
    )