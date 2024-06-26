from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from contact.models import Contact
from django.db.models import Q
from django.http import Http404
from django.db.models.functions import Lower

# Create your views here.
def index(req, mine=False):
    if mine:
        contacts = Contact.objects.filter(show=True, owner=req.user).annotate(first_name_lower=Lower('first_name')).order_by('first_name_lower', 'last_name')
    else:
        contacts = Contact.objects.filter(show=True).annotate(first_name_lower=Lower('first_name')).order_by('first_name_lower', 'last_name')
        
    paginator = Paginator(contacts, 20) 

    page_number = req.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'site_title': 'Contacts - '
    }
    
    return render(
        req,
        'contact/index.html',
        context,
    )
    
def startwa(req):
    contacts = Contact.objects.filter(show=True, first_name__istartswith='a')
    paginator = Paginator(contacts, 20) 

    page_number = req.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    contacts_count = contacts.count()
    show_contact_count = True
    
    context = {
        'page_obj': page_obj,
        'contacts_count': contacts_count,
        'show_contact': show_contact_count
    }
    return render(
        req,
        'contact/index.html',
        context
    )
    
def withemail(req):
    # Todos os contatos com email
    # contacts = Contact.objects.filter(show=True, email__isnull=True).exclude(email='')
    
    # Todos os contatos sem email
    contacts = Contact.objects.filter(show=True).filter(
        Q(email__isnull=True) |
        Q(email='')
    )
    paginator = Paginator(contacts, 20)
    
    page_number = req.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    contacts_count = contacts.count()
    show_contact_count = True
    
    context = {
        'page_obj': page_obj,
        'contacts_count': contacts_count,
        'show_contact': show_contact_count
    }
    
    return render(
        req,
        'contact/index.html',
        context
    )
    
def search(req):
    search_value = req.GET.get('q', '').strip()
    
    if search_value == '':
        return redirect('contact:index')
    
    contacts = Contact.objects.filter(show=True).annotate(first_name_lower=Lower('first_name')).filter(
        Q(first_name__icontains=search_value) |
        Q(last_name__icontains=search_value) |
        Q(phone__icontains=search_value) |
        Q(email__icontains=search_value)
    ).order_by('first_name_lower', 'last_name')
    
    paginator = Paginator(contacts, 20) 

    page_number = req.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    contacts_count = contacts.count()
    
    context = {
        'page_obj': page_obj,
        'site_title': f'Search - {search_value} ',
        'contacts_count': contacts_count,
        'search_value': search_value
    }
    
    return render(
        req,
        'contact/index.html',
        context,
    )
    
def contact(req, contact_id):
    # single_contact = Contact.objects.filter(pk=contact_id).first()
    # if single_contact is None:
    #     raise Http404
    
    # single_contact = get_object_or_404(Contact.objects.filter(pk=contact_id))
    
    single_contact = get_object_or_404(Contact, pk=contact_id, show=True)
    contact_name = f'{single_contact.first_name} {single_contact.last_name}'
    
    
    context = {
        'contact': single_contact,
        'site_title': f'{contact_name } - '
    }
    
    return render(
        req,
        'contact/contact.html',
        context,
    )
