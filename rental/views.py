from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .models import Drone,Rental
from django.contrib import messages
from .forms import NewDroneForm,EditDroneForm
from PIL import Image
from django.http import JsonResponse



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

@login_required
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

@login_required
def delete(request, pk):
    try:
        if request.user.is_staff:
            drone = Drone.objects.get(pk=pk)
        else:
            messages.error(request, 'You do not have permission to delete this drone.')
            return redirect('index')
        
    except Drone.DoesNotExist:
        messages.error(request, 'The drone does not exist or you do not have permission to delete it.')
        return redirect('index')  
    
    drone.delete()
    return redirect('index')

def drone_list(request):
    return render(request, 'drone/drone_list.html')

def drone_data(request):
    draw = int(request.GET.get('draw', 0))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '')

    drones = Drone.objects.all()
    total_records = drones.count()

    if search_value:
        drones = drones.filter(brand__icontains=search_value) | drones.filter(model__icontains=search_value) | drones.filter(category__icontains=search_value)

    filtered_records = drones.count()
    drones = drones[start:start+length]

    data = [{
        'brand': drone.brand,
        'model': drone.model,
        'category': drone.category,
        'weight': drone.weight,
        'id': drone.id
    } for drone in drones]

    response = {
        'draw': draw,
        'recordsTotal': total_records,
        'recordsFiltered': filtered_records,
        'data': data
    }

    return JsonResponse(response)

def resize_image(image_path, size=(2000, 2000)):
    img = Image.open(image_path)
    img = img.resize(size, Image.Resampling.LANCZOS)
    img.save(image_path)