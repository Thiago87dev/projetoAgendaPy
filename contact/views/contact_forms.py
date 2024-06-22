from django.shortcuts import redirect, render, get_object_or_404
from contact.forms import ContactForm
from django.urls import reverse
from contact.models import Contact
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required(login_url='contact:login')
def create(req):
    form_action = reverse('contact:create')
    if req.method == 'POST':
        form = ContactForm(req.POST, req.FILES)
        
        context = {
        'form': form,
        'form_action': form_action,
        }
        
        if form.is_valid():
            # form.save()
            contact = form.save(commit=False)
            contact.owner = req.user
            contact.save()
            if req.headers.get('x-requested-with') == 'XMLHttpRequest':
               return JsonResponse({'status': 'success', 'contact_id': contact.pk}) 
            # contact.show = False
            # contact.save()
            return redirect('contact:contact', contact_id=contact.pk)
        
        if req.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'errors': form.errors})
    
        return render(
            req,
            'contact/create.html',
            context
        )
    
    context = {
        'form': ContactForm(),
        'form_action': form_action,
        }
    
    return render(
        req,
        'contact/create.html',
        context
    )
@login_required(login_url='contact:login')  
def update(req, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id, show=True, owner=req.user)
    form_action = reverse('contact:update', args=(contact_id,))
    if req.method == 'POST':
        form = ContactForm(req.POST, req.FILES, instance=contact)
        
        context = {
        'form': form,
        'form_action': form_action,
        }
        
        if form.is_valid():
            # form.save()
            contact = form.save()
            if req.headers.get('x-requested-with') == 'XMLHttpRequest':
               return JsonResponse({'status': 'success', 'contact_id': contact.pk}) 
            # contact.show = False
            # contact.save()
            return redirect('contact:contact', contact_id=contact.pk)
        
        if req.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'errors': form.errors})
    
        return render(
            req,
            'contact/create.html',
            context
        )
    
    context = {
        'form': ContactForm(instance=contact),
        'form_action': form_action,
        }
    
    return render(
        req,
        'contact/create.html',
        context
    )
@login_required(login_url='contact:login')   
def delete(req, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id, show=True, owner=req.user)
    # confirmation = req.POST.get('confirmation', 'no')
    
    # context = {
    #     'contact':contact,
    #     'confirmation':confirmation,
    # }
    
    # if confirmation == 'yes':
    contact.delete()
    return redirect('contact:index')
    

