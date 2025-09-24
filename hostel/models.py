from django.db import models
from django.contrib.auth.models import User
from admissions.models import Student

class Room(models.Model):
    room_number = models.CharField(max_length=10, unique=True)
    capacity = models.IntegerField()
    occupied = models.IntegerField(default=0)

    def __str__(self):
        return self.room_number

class HostelAllocation(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    allocated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} in {self.room.room_number}"

class StaffAllocation(models.Model):
    staff = models.OneToOneField(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    allocated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.staff.username} in {self.room.room_number}"
