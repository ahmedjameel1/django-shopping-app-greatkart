from django.shortcuts import render , redirect
from .forms import *
from .models import Account 
from django.contrib import messages, auth
from django.contrib.auth import authenticate
# Create your views here.




def register(request):
    if request.method == "POST":
        updated_request = request.POST.copy()
        updated_request.update({'username': request.POST['email']})
        form = RegistrationForm(updated_request)
        print(form.is_valid())
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = form.cleaned_data['username'].split('@')[0]
            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name, 
                email=email, 
                username=username, 
                password=password
            )
            
            user.phone_number = phone_number
            user.save()
            messages.success(request, 'User account was created!')
            return redirect('store')
    else:
        form = RegistrationForm()
    
    ctx = {'form':form}
    return render(request, 'accounts/register.html',ctx)



def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth.login(request,user)
            # Redirect to a success page.
            return redirect('store')
            
        else:
            # Return an 'invalid login' error message.
            messages.success(request, 'username or Password is incorrect')
            return redirect('login')
    return render(request, 'accounts/login.html',{'form':form})




def logout(request):
    auth.logout(request)
    return redirect('login')



















