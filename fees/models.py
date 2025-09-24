from django.db import models
from admissions.models import Student

class FeePayment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending Confirmation'),
        ('Confirmed', 'Confirmed'),
        ('Rejected', 'Rejected'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    receipt_no = models.CharField(max_length=20)
    paid_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    confirmed_by = models.CharField(max_length=100, blank=True)
    confirmed_on = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Payment {self.receipt_no} for {self.student.name}"
