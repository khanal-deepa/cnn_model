from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, ProfileForm
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import subprocess

# Create your views here.


def index(request):
    return render(request, 'users/index.html')

# def camera(request):
#     return render(request, 'users/camera.html')

def start_test(request):
    try:
        # Replace 'python test.py' with the appropriate command to start your backend server
<<<<<<< HEAD
        subprocess.run(['python', 'users/test.py'])
=======
        subprocess.run(['python3', 'users/test.py'])
>>>>>>> e95a7396 (first commit)
        return HttpResponse('Backend server started successfully!')
    except Exception as e:
        return HttpResponse(f'Error starting backend server: {e}')

<<<<<<< HEAD

# def start_test(request):
#     try:
#         # Adjust the path and command as needed
#         result = subprocess.run(['python', 'users/test.py'], capture_output=True, text=True, check=True)
        
#         # Include the output in the response
#         response_content = f'Backend server started successfully!\n\nOutput:\n{result.stdout}'
        
#         return HttpResponse(response_content)
#     except subprocess.CalledProcessError as e:
#         # Include the error message in the response
#         response_content = f'Error starting backend server: {e}\n\nOutput:\n{e.stderr}'
#         return HttpResponse(response_content)
#     except Exception as e:
#         # Handle other exceptions and include the error message in the response
#         return HttpResponse(f'Error: {e}')


=======
>>>>>>> e95a7396 (first commit)
def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Invalid username')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'users/login.html')


def logoutUser(request):
    logout(request)
    messages.success(request, 'User logged Out')
    return redirect('index')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User Registred')

            # login(request, user)
            return redirect('index')

        else:
            messages.error(request, 'User not registered')

    context = {'page': page, 'form': form}
    return render(request, 'users/register.html', context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    context = {'profile': profile}
    return render(request, 'users/user-profile.html', context)


@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    context = {'profile': profile}
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')
    context = {'form': form}
    return render(request, 'users/profile_form.html', context)


@login_required(login_url='login')
def deleteProfile(request, pk):
    profile = Profile.objects.get(id=pk)

    if request.method == 'POST':
        profile.delete()
        messages.success(request, 'Profile deleted successfully')
        return redirect('index')

    context = {'object': profile}
    return render(request, 'users/delete_profile.html', context)
