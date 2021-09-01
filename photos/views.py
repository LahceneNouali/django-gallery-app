from django.shortcuts import render, redirect
from .models import Category, Photo
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm

# Create your views here.

def loginUser(request):
    page = 'login'

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('add')

    return render(request, 'photos/login_register.html', {'page': page})

def registerUser(request):
    page = 'register'
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            if user is not None:
                login(request, user)
                return redirect('gallery')
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()

    context = {'form': form, 'page': page}
    return render(request, 'photos/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('gallery')

def gallery(request):
    category = request.GET.get('category')

    if category == None:
        photos = Photo.objects.all()
    else:
        photos = Photo.objects.filter(category__name=category)
    
    categories = Category.objects.all()
    context = {'categories': categories, 'photos': photos}
    return render(request, 'photos/gallery.html', context)

def viewPhoto(request, id):
    photo = Photo.objects.get(pk=id)
    return render(request, 'photos/photo.html', {'photo': photo})

@login_required(login_url='login')
def addPhoto(request):
    user = request.user

    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')

        if data['category'] != 'none':
            category = Category.objects.get(pk=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(name=data['category_new'])
        else:
            category = None

        for image in images:
            photo = Photo.objects.create(
                user=user,
                # description = data['description'],
                category = category,
                image = image,
            )

        return redirect('gallery')

    categories = Category.objects.all()
    return render(request, 'photos/add.html', {'categories': categories})
