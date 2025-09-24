from django import forms
from .models import FeePayment

class FeePaymentForm(forms.ModelForm):
    class Meta:
        model = FeePayment
        fields = ['student', 'amount', 'receipt_no']