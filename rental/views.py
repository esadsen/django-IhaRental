from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .models import Drone,Rental
from django.contrib import messages
from .forms import NewDroneForm,EditDroneForm
from PIL import Image


def index(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact.html')

@login_required
def new(request):
    if request.method=='POST':
        form=NewDroneForm(request.POST,request.FILES)
        
        if form.is_valid():
            item=form.save(commit=False)
            item.save()
            
            resize_image(item.image.path)
            
            return redirect('index')
    
    else:
        form=NewDroneForm()
    
    return render(request, 'drone/form.html',{
        'form':form,
        'title':'New Drone'
    })

@login_required(login_url='../../../user/login')
def edit(request, pk):
    drone = get_object_or_404(Drone, pk=pk)
    
    # Kullanıcının admin olup olmadığını kontrol et
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to edit this item.')
        return redirect('index')

    if request.method == 'POST':
        form = EditDroneForm(request.POST, request.FILES, instance=drone)
        
        if form.is_valid():
            form.save()
            resize_image(drone.image.path)  # resize_image fonksiyonunu tanımladığınızdan emin olun
            
            return redirect('index')
    else:
        form = EditDroneForm(instance=drone)
    
    return render(request, 'drone/form.html', {
        'form': form,
        'title': 'Edit Drone'
    })

def resize_image(image_path, size=(2000, 2000)):
    img = Image.open(image_path)
    img = img.resize(size, Image.Resampling.LANCZOS)
    img.save(image_path)