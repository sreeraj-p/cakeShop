from django.shortcuts import render,redirect
from django import forms
from cakes.models import Cake
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from cakes.forms import LoginForm,RegisterationForm,CakeForm
from django.contrib import messages
from django.utils.decorators import method_decorator

# Create your views here.

def signin_required(fn):

    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"You must login to perform this action")
            return redirect('signin')
        return fn(request,*args,**kwargs)
    return wrapper



class SignUpView(View):
    model=User
    form_class=RegisterationForm
    template_name='register.html'

    def get(self,request,*args,**kwargs):
        form=self.form_class
        return render(request,self.template_name,{'form':form})
    
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Account has been created")
            return redirect('signin')
        messages.error(request,"Faild to create Your Account")
        return render(request,self.template_name,{'form':form})
    
class SignInView(View):
    model=User
    template_name='login.html'
    form_class=LoginForm

    def get(self,request,*args,**kwargs):
        form=self.form_class
        return render(request,self.template_name,{'form':form})
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get('username')
            pwd=form.cleaned_data.get('password')
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                messages.success(request,"Login Success")
                return redirect('cake-list')
            messages.error(request,"Invalid credential")
            return render(request,self.template_name,{'form':form})
        
    
@method_decorator(signin_required,name='dispatch')
class CakeCreateView(View):
    def get(self,request,*args,**kwargs):
        form=CakeForm()
        return render(request, 'cake-add.html',{'form':form})
    
    def post(self,request,*args,**kwargs):
        form=CakeForm(data=request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"Cake Added Successfully")
            return redirect('cake-list')
        messages.error(request,"Faild To Add Cake")
        return render(request,'cake-add.html',{'form':form})
    
    
@method_decorator(signin_required,name='dispatch')
class CakeListView(View):
    def get(self,request,*args,**kwargs):
        qs=Cake.objects.all()
        return render(request,"cake-list.html",{'cakes':qs})
    
    
@method_decorator(signin_required,name='dispatch')
class CakeDetailsView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('j')
        qs=Cake.objects.get(id=id)
        return render(request,'cake-detail.html',{'cakes':qs})


@method_decorator(signin_required,name='dispatch')
class CakeEditView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('j')
        ck=Cake.objects.get(id=id)
        form=CakeForm(instance=ck)
        return render(request,'cake-edit.html',{'form':form})
    
    def post(self,request,*args,**kwargs):
        id=kwargs.get('j')
        ck=Cake.objects.get(id=id)
        form=CakeForm(instance=ck,data=request.POST,files=request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request,"Cake Details Updated")
            return redirect('cake-list')
        messages.error(request,'Failed To Update Cake Details')
        return render(request,'cake-detail.html',{'form':form})
    

@method_decorator(signin_required,name='dispatch')
class CakeDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('j')
        Cake.objects.filter(id=id).delete()
        messages.error(request,"Cake Deleted")
        return redirect('cake-list')

@signin_required
def sign_out_view(request,*args,**kwargs):
    logout(request)
    messages.success(request,"Logout Successfull")
    return redirect('signin')

    