from django.shortcuts import redirect, render, get_object_or_404
from contact.forms import ContactForm
from django.urls import reverse
from contact.models import Contact

def create(req):
    form_action = reverse('contact:create')
    if req.method == 'POST':
        form = ContactForm(req.POST)
        
        context = {
        'form': form,
        'form_action': form_action,
        }
        
        if form.is_valid():
            # form.save()
            contact = form.save()
            # contact.show = False
            # contact.save()
            return redirect('contact:contact', contact_id=contact.pk)
    
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
    
def update(req, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id, show=True)
    form_action = reverse('contact:update', args=(contact_id,))
    if req.method == 'POST':
        form = ContactForm(req.POST, instance=contact)
        
        context = {
        'form': form,
        'form_action': form_action,
        }
        
        if form.is_valid():
            # form.save()
            contact = form.save()
            # contact.show = False
            # contact.save()
            return redirect('contact:contact', contact_id=contact.pk)
    
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
    
def delete(req, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id, show=True)
    # confirmation = req.POST.get('confirmation', 'no')
    
    # context = {
    #     'contact':contact,
    #     'confirmation':confirmation,
    # }
    
    # if confirmation == 'yes':
    contact.delete()
    return redirect('contact:index')
    

