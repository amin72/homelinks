from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .models import ContactUs
from .forms import ContactUsForm
from dashboard.models import Action


# contact us
def contact_us(request):
    message = _('Your message was successfully submitted.')

    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            obj = form.save()

            # create action
            model_name = ContactUs.__name__.lower()
            content_type = ContentType.objects.get(model=model_name,
                app_label='contact')
            Action.objects.get_or_create(type='contact_us',
                content_type=content_type, object_id=obj.id)

            messages.success(request, message)
            return redirect(reverse('links:index'))
    else:
        form = ContactUsForm()

    context = {
        'form': form,
        'active_contactus': True,
    }
    return render(request, 'contact/contact_us.html', context)
