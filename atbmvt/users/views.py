from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from .forms import CustomUserCreationForm, CustomUserLoginForm
from django.contrib import messages

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save(commit=False)

                if 'image' in request.FILES:
                    image = request.FILES['image']
                    user.image_small = image
                    user.image_medium = image
                    user.image_large = image

                user.save()  # завжди зберігаємо користувача
                messages.success(request, "Реєстрація пройшла успішно!")
                return redirect('homepage')

            except Exception as e:
                messages.error(request, f"Щось пішло не так: {e}")
        else:
            messages.error(request, 'Виправте помилки у формі')
    else:
        form = CustomUserCreationForm()

    return render(request, "register.html", {"form": form})


def user_login(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('homepage')
    else:
        form = CustomUserLoginForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('homepage')


