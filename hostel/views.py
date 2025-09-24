from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Room, HostelAllocation, StaffAllocation
from .forms import StudentAllocationForm, StaffAllocationForm

@login_required
def hostel(request):
    rooms = Room.objects.all()
    student_allocations = HostelAllocation.objects.all()
    staff_allocations = StaffAllocation.objects.all()

    is_staff = not request.user.groups.filter(name='Student').exists()

    student_form = StudentAllocationForm()
    staff_form = StaffAllocationForm()

    if request.method == 'POST':
        if 'allocate_student' in request.POST and is_staff:
            student_form = StudentAllocationForm(request.POST)
            if student_form.is_valid():
                allocation = student_form.save()
                # Update room occupied count
                allocation.room.occupied += 1
                allocation.room.save()
                messages.success(request, f"Allocated {allocation.student.name} to {allocation.room.room_number}")
                return redirect('hostel:hostel')
        elif 'allocate_staff' in request.POST and is_staff:
            staff_form = StaffAllocationForm(request.POST)
            if staff_form.is_valid():
                allocation = staff_form.save()
                # Update room occupied count
                allocation.room.occupied += 1
                allocation.room.save()
                messages.success(request, f"Allocated {allocation.staff.username} to {allocation.room.room_number}")
                return redirect('hostel:hostel')
        else:
            messages.error(request, "You do not have permission to allocate rooms.")

    # Calculate occupancy percentage for each room
    for room in rooms:
        if room.capacity > 0:
            room.occupancy_percentage = int((room.occupied / room.capacity) * 100)
        else:
            room.occupancy_percentage = 0

    context = {
        'rooms': rooms,
        'student_allocations': student_allocations,
        'staff_allocations': staff_allocations,
        'is_staff': is_staff,
        'student_form': student_form,
        'staff_form': staff_form,
    }
    return render(request, 'hostel/hostel.html', context)
