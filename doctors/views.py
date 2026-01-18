
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Availability, DoctorCategory
from datetime import date

@login_required
def doctor_dashboard(request):
	if not request.user.is_authenticated or request.user.role != 'DOCTOR':
		return redirect('home')
	slots = Availability.objects.filter(doctor=request.user).order_by('date', 'start_time')
	return render(request, 'doctor_dashboard.html', {'slots': slots})

@login_required
def add_slot(request):
	if not request.user.is_authenticated or request.user.role != 'DOCTOR':
		return redirect('home')
	categories = DoctorCategory.objects.all()
	if request.method == 'POST':
		slot_date = request.POST.get('date')
		start_time = request.POST.get('start_time')
		end_time = request.POST.get('end_time')
		category_id = request.POST.get('category')
		category = DoctorCategory.objects.filter(id=category_id).first() if category_id else None
		if not (slot_date and start_time and end_time):
			messages.error(request, 'All fields are required.')
		else:
			exists = Availability.objects.filter(
				doctor=request.user,
				date=slot_date,
				start_time=start_time,
				end_time=end_time
			).exists()
			if exists:
				messages.warning(request, 'This slot already exists.')
			else:
				Availability.objects.create(
					doctor=request.user,
					date=slot_date,
					start_time=start_time,
					end_time=end_time,
					category=category
				)
				messages.success(request, 'Slot added successfully!')
				return redirect('doctor_dashboard')
	return render(request, 'add_slot.html', {'categories': categories})

@login_required
def edit_slot(request, slot_id):
	if not request.user.is_authenticated or request.user.role != 'DOCTOR':
		return redirect('home')
	slot = get_object_or_404(Availability, id=slot_id, doctor=request.user)
	categories = DoctorCategory.objects.all()
	if request.method == 'POST':
		slot.date = request.POST.get('date')
		slot.start_time = request.POST.get('start_time')
		slot.end_time = request.POST.get('end_time')
		category_id = request.POST.get('category')
		slot.category = DoctorCategory.objects.filter(id=category_id).first() if category_id else None
		slot.save()
		messages.success(request, 'Slot updated!')
		return redirect('doctor_dashboard')
	return render(request, 'edit_slot.html', {'slot': slot, 'categories': categories})

@login_required
def delete_slot(request, slot_id):
	if not request.user.is_authenticated or request.user.role != 'DOCTOR':
		return redirect('home')
	slot = get_object_or_404(Availability, id=slot_id, doctor=request.user)
	if request.method == 'POST':
		slot.delete()
		messages.success(request, 'Slot deleted!')
		return redirect('doctor_dashboard')
	return render(request, 'delete_slot.html', {'slot': slot})
