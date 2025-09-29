from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

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
            messages.success(request, 'Registration Successful.')
            return redirect('register')
    else:
        form = RegistrationForm()

    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)

def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        
        user = auth.authenticate(username = email, password = password)


        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid login credentials")
            return redirect('login')
        
    return render(request, 'accounts/login.html')

@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, "You are logged out!")
    return redirect('login')
