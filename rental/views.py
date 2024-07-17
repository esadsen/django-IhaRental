from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .models import Drone, Rental
from django.contrib import messages
from .forms import NewDroneForm, EditDroneForm, RentalForm
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

@login_required
def drone_rent(request, pk):
    drone = get_object_or_404(Drone, pk=pk)

    if request.method == 'POST':
        form = RentalForm(request.POST)
        if form.is_valid():
            rental = form.save(commit=False)
            rental.drone = drone
            rental.user = request.user
            rental.save()
            messages.success(request, 'Drone successfully rented!')
            return redirect('rental:drone_list')
    else:
        form = RentalForm()

    return render(request, 'rental/rental_form.html', {
        'form': form,
        'drone': drone,
        'title': 'Rent Drone'
    })

@login_required
def user_rentals(request):
    return render(request, 'rental/user_rentals.html')

@login_required
def user_rentals_data(request):
    draw = int(request.GET.get('draw', 0))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '')

    rentals = Rental.objects.filter(user=request.user)
    total_records = rentals.count()

    if search_value:
        rentals = rentals.filter(
            drone__brand__icontains=search_value
        ) | rentals.filter(
            drone__model__icontains=search_value
        ) | rentals.filter(
            drone__category__icontains=search_value
        )

    filtered_records = rentals.count()
    rentals = rentals[start:start+length]

    data = [{
        'id': rental.id,
        'drone': f"{rental.drone.brand} {rental.drone.model}",
        'start_datetime': rental.start_datetime.strftime('%Y-%m-%d %H:%M'),
        'end_datetime': rental.end_datetime.strftime('%Y-%m-%d %H:%M'),
    } for rental in rentals]

    response = {
        'draw': draw,
        'recordsTotal': total_records,
        'recordsFiltered': filtered_records,
        'data': data
    }

    return JsonResponse(response)

@login_required
def rental_update(request, pk):
    rental = get_object_or_404(Rental, pk=pk, user=request.user)
    if request.method == 'POST':
        form = RentalForm(request.POST, instance=rental)
        if form.is_valid():
            form.save()
            messages.success(request, 'Rental successfully updated!')
            return redirect('rental:user_rentals')
    else:
        form = RentalForm(instance=rental)
    return render(request, 'rental/rental_form.html', {'form': form, 'title': 'Edit Rental'})

@login_required
def rental_delete(request, pk):
    rental = get_object_or_404(Rental, pk=pk, user=request.user)
    if request.method == 'POST':
        rental.delete()
        messages.success(request, 'Rental successfully deleted!')
        return redirect('rental:user_rentals')
    return render(request, 'rental/rental_confirm_delete.html', {'rental': rental})
