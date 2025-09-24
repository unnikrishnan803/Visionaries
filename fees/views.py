from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
from django.utils import timezone
from .models import FeePayment
from .forms import FeePaymentForm

@login_required
def fees(request):
    # Check if user is a student
    if not request.user.groups.filter(name='Student').exists():
        messages.error(request, 'Access denied. This page is only for students.')
        return redirect('dashboard:dashboard')

    try:
        student = request.user.student
    except:
        messages.error(request, 'Student profile not found.')
        return redirect('dashboard:dashboard')

    payments = FeePayment.objects.filter(student=student).order_by('-paid_on')

    if request.method == 'POST':
        form = FeePaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.student = student
            payment.save()
            messages.success(request, 'Payment recorded successfully.')
            return redirect('fees:fees')
    else:
        form = FeePaymentForm()

    return render(request, 'fees/fees.html', {
        'form': form,
        'payments': payments,
        'student': student
    })

@login_required
def download_receipt(request, payment_id):
    # Check if user is a student
    if not request.user.groups.filter(name='Student').exists():
        messages.error(request, 'Access denied.')
        return redirect('dashboard:dashboard')

    payment = get_object_or_404(FeePayment, id=payment_id, student=request.user.student)

    # Return HTML receipt that can be printed/saved
    template = get_template('fees/receipt.html')
    context = {'payment': payment}
    html = template.render(context)

    response = HttpResponse(content_type='text/html')
    response['Content-Disposition'] = f'attachment; filename="receipt_{payment.receipt_no}.html"'

    response.write(html)
    return response

@login_required
def confirm_payment(request, payment_id):
    # Check if user is staff/admin (not student)
    if request.user.groups.filter(name='Student').exists():
        messages.error(request, 'Access denied. Only staff can confirm payments.')
        return redirect('dashboard:dashboard')

    payment = get_object_or_404(FeePayment, id=payment_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'confirm':
            payment.status = 'Confirmed'
            payment.confirmed_by = request.user.username
            payment.confirmed_on = timezone.now()
            payment.save()
            messages.success(request, f'Payment {payment.receipt_no} confirmed successfully.')
        elif action == 'reject':
            payment.status = 'Rejected'
            payment.confirmed_by = request.user.username
            payment.confirmed_on = timezone.now()
            payment.save()
            messages.success(request, f'Payment {payment.receipt_no} rejected.')

        return redirect('dashboard:dashboard')

    return render(request, 'fees/confirm_payment.html', {'payment': payment})

@login_required
def download_certificate(request, payment_id):
    # Check if user is a student
    if not request.user.groups.filter(name='Student').exists():
        messages.error(request, 'Access denied.')
        return redirect('dashboard:dashboard')

    payment = get_object_or_404(FeePayment, id=payment_id, student=request.user.student)

    # Only allow download if payment is confirmed
    if payment.status != 'Confirmed':
        messages.error(request, 'Certificate not available. Payment must be confirmed first.')
        return redirect('fees:fees')

    # Return HTML certificate
    template = get_template('fees/certificate.html')
    context = {'payment': payment}
    html = template.render(context)

    response = HttpResponse(content_type='text/html')
    response['Content-Disposition'] = f'attachment; filename="certificate_{payment.student.student_id}.html"'

    response.write(html)
    return response
