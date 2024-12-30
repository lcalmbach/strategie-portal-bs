from django.shortcuts import render

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from login_account.forms import LoginForm
from django.contrib.auth import login

from objective_manager_app.models import Person, Strategie
from objective_manager_app.forms import PersonForm

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse
from .forms import LoginForm

def user_login(request):
    strategie = get_object_or_404(Strategie, id=request.session['strategie_id']) 

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])
            person = Person.objects.get(user=user)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.info(request, f"Willkommen {person.vorname}.")
                    return redirect('home', pk=strategie.pk)  # Pass `pk` to the redirect
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()

    context = { 
        'form': form,
        'strategie': strategie
    }
    return render(request, 'login_account/login.html', context)


@login_required
def user_logout(request):
    user = request.user
    strategie = get_object_or_404(Strategie, id=request.session['strategie_id']) 
    try:
        person = Person.objects.get(user=user)
        logout(request)
        messages.info(request, f"Auf Wiedersehen {person.vorname}.")
    except Person.DoesNotExist:
        logout(request)
        messages.info(request, f"Auf Wiedersehen.")
    return redirect('home', pk=strategie.pk)  # Pass `pk` to the redirect

@login_required
def user_profile(request):
    user = request.user
    try:
        person = Person.objects.get(user=user)
    except Person.DoesNotExist:
        messages.error(request, "Profile not found.")
        return redirect('some_error_page')  # Handle the error appropriately

    if request.method == 'POST':
        profile_form_valid = False
        password_change_form_valid = False

        password_change_form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            form.save()
            profile_form_valid = True
            messages.success(request, "Profile updated successfully.")
        
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in
            password_change_form_valid = True
            messages.success(request, "Password changed successfully.")

        if profile_form_valid or password_change_form_valid:
            return redirect('profile')  # Redirect to a profile success page
    else:
        form = PersonForm(instance=person)

        password_change_form = PasswordChangeForm(request.user)

    return render(request, 'login_account/profile.html', {
        'form': form,
        'password_change_form': password_change_form
    })