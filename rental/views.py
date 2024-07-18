from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .models import Drone, Rental
from django.contrib import messages
from .forms import NewDroneForm, EditDroneForm, RentalForm
from django.http import JsonResponse



from django.shortcuts import render

def index(request):
    drones = [
        {
            'name': 'Mini IHA',
            'category': 'Unarmed',
            'image_url': '../media/drone_images/mini_iha1.png'
        },
        {
            'name': 'BAYRAKTAR TB2',
            'category': 'Armed',
            'image_url': '../media/drone_images/tb2_1.png'
        },
        {
            'name': 'BAYRAKTAR TB3',
            'category': 'Armed',
            'image_url': '../media/drone_images/tb3.png'
        },
        
    ]
    
    categories = [
        {
            'name': 'Unarmed',
            'count': 1
        },
        {
            'name': 'Armed',
            'count': 2
        }
    ]
    
    return render(request, "index.html", {
        'drones': drones,
        'categories': categories
    })

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
    
    if request.method == 'POST':
        drone.delete()
        messages.success(request, 'Drone successfully deleted!')
        return redirect('rental:drone_list')
    return render(request, 'drone/drone_confirm_delete.html', {'drone': drone})

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
    if request.user.is_staff:
        rental = get_object_or_404(Rental, pk=pk)
    else:
        rental = get_object_or_404(Rental, pk=pk, user=request.user)
    if request.method == 'POST':
        form = RentalForm(request.POST, instance=rental)
        if form.is_valid():
            form.save()
            messages.success(request, 'Rental successfully updated!')
            if request.user.is_staff:
                return redirect('rental:all_rentals')
            else:
                return redirect('rental:user_rentals')
    else:
        form = RentalForm(instance=rental)
    return render(request, 'rental/rental_form.html', {'form': form, 'title': 'Edit Rental'})

@login_required
def rental_delete(request, pk):
    if request.user.is_staff:
        rental = get_object_or_404(Rental, pk=pk)
    else:
        rental = get_object_or_404(Rental, pk=pk, user=request.user)
       
    if request.method == 'POST':
        rental.delete()
        messages.success(request, 'Rental successfully deleted!')
        if request.user.is_staff:
            return redirect('rental:all_rentals')
        else:
            return redirect('rental:user_rentals')
    return render(request, 'rental/rental_confirm_delete.html', {'rental': rental})


@login_required
def all_rentals(request):
    if request.user.is_staff:
        return render(request, 'rental/all_rentals.html')
    else:
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('index')

@login_required
def all_rentals_data(request):
    if request.user.is_staff:
        draw = int(request.GET.get('draw', 0))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '')

        rentals = Rental.objects.all()
        total_records = rentals.count()

        if search_value:
            rentals = rentals.filter(
                drone__brand__icontains=search_value
            ) | rentals.filter(
                drone__model__icontains=search_value
            ) | rentals.filter(
                drone__category__icontains=search_value
            ) | rentals.filter(
                user__username__icontains=search_value
            )

        filtered_records = rentals.count()
        rentals = rentals[start:start+length]

        data = [{
            'id': rental.id,
            'drone': f"{rental.drone.brand} {rental.drone.model}",
            'user': rental.user.username,
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
    else:
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('index')
