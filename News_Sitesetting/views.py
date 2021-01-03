from django.contrib import messages
from django.shortcuts import render, redirect
from .models import SiteSetiing
from .forms import ContactForm
from Extentions.utils import get_ext_file

def aboutus_page(request):
    return render(request, 'about_us.html', {'SiteSetiing':SiteSetiing.objects.filter(active=True).first()})


def contactus_page(request):
    contact = ContactForm(request.POST or None, request.FILES or None)
    context = {
        'contact': contact
    }

    contact = ContactForm(request.POST or request.FILES)
    if contact.is_valid():
        imagee = request.FILES.get('image')
        if imagee:
            yes_no = get_ext_file(imagee)

            if yes_no == 'yes':
                contact_item = contact.save(commit=False)
                contact_item.image = imagee
                contact_item.save()

                messages.info(request, 'پیام شما با موفقیت ارسال شد. ممنون از تبادلات شما')
                return redirect('/')

            else:
                messages.info(request, 'پسوند فایل مجاز نمیباشد.')
                return redirect('sitesetting:contactus')
        else:
            contact_item = contact.save(commit=False)
            contact_item.save()
            messages.info(request, 'پیام شما با موفقیت ارسال شد. ممنون از تبادلات شما')
            return redirect('/')

    return render(request, 'contact_us.html', context)