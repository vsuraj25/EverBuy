from django.shortcuts import render
from .forms import RegistrationForm
from .models import Account

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            first_name =  cleaned_data['first_name']
            last_name =  cleaned_data['last_name']
            phone =  cleaned_data['phone']
            email =  cleaned_data['email']
            password =  cleaned_data['password']
            username = email.split('@')[0]

            user = Account.objects.create_user(first_name= first_name, last_name=last_name,
                     email =email, username =username, password = password)
            user.phone = phone
            user.save()
    else:
        form = RegistrationForm()

    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)

def login(request):
    return render(request, 'accounts/login.html')

def logout(request):
    return render(request, 'accounts/logout.html')
