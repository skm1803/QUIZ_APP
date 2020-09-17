#From Django Core
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from django.views.generic import CreateView,FormView
from django.contrib import messages
from django.utils.http import is_safe_url
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_out


# This folder imports
from .forms import LoginForm,RegisterForm

def login_page(request):
    next_     = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post
    print(redirect_path)
    if request.method =="POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            print(email,password)
            user = authenticate(request,email=email,password=password)
            print(user)
            if user is not None:
                login(request,user)
                try:
                    del request.session['guest_email_id']
                except:
                    pass
                messages.success(request,"You are logged in")
                if is_safe_url(redirect_path,request.get_host()):
                    return redirect(redirect_path)
                else:
                    return redirect('/')
            else:
                messages.warning(request,"The email or password is incorrect or Email not Confirmed")
                context = {'form':form,'page_name':'Login Page'}
                return render(request,'my_auth/login.html',context)
        print(form.errors)
        messages.warning(request,"the following error occured")
        messages.error(request,form.errors)
        context = {'form':form,'page_name':'Login Page'}
        return render(request,'my_auth/login.html',context)
    else:
        form = LoginForm()
        context = {'form':form,'page_name':'Login Page'}
        return render(request,'my_auth/login.html',context)

######----------------Signup----------------------------------------------

def signup(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Registered')
            return redirect('login')
        messages.warning(request,"The following errors occured")
        messages.error(request,form.errors)
        context = {'form':form,'page_name':'Signup Form'}
        return render(request,'my_auth/signup.html',context)
    else:
        form = RegisterForm()
        context = {'form':form,'page_name':'Signup Form'}
        return  render(request,'my_auth/signup.html',context)


class RegisterView(CreateView):
    '''This is the reason why people love class based views and
    this is the reason why I hate CBVs!! Too much abstraction is based for maintainace of software'''

    form_class   = RegisterForm
    template_name= 'my_auth/signup.html'
    success_url  = '/login/'



###----------------Logout ----------------###############
@receiver(user_logged_out)
def on_user_logged_out(sender, request, **kwargs):
    """So that the user knows that he/she is logged out"""
    messages.add_message(request, messages.INFO, 'Successfully Logged out.')