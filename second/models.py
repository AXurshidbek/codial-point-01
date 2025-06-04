from main.models import *
from django.core.exceptions import ValidationError


TASK_STATUS = [
    ('new', 'Yangi'),
    ('in_progress', 'Jarayonda'),
    ('completed', 'Tugallangan'),
]

RESPONSE_STATUS=(('given','Berildi'),
             ('assigned','Topshirdi'),
             ('failed','Bajarilmadi'),
             ('graded','Baholandi'))

class Assignment(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    file=models.FileField(upload_to='tasks/', null=True, blank=True)
    mentor=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    max_point=models.PositiveIntegerField(default=0)
    status=models.CharField(max_length=20, choices=TASK_STATUS, default='new')
    deadline=models.DateTimeField()

    def __str__(self):
        return self.title




class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    student = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    response = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='responses/', null=True, blank=True)
    point = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=10, choices=RESPONSE_STATUS, default='given')

    def clean(self):
        if not (self.response or self.description or self.file):
            raise ValidationError("Hech bo'lmaganda response, description yoki file dan biri kiritilishi kerak.")

    def save(self, *args, **kwargs):
        self.full_clean()  # clean() metodini chaqiramiz

        from django.utils.timezone import now
        if self.assignment.deadline and now() > self.assignment.deadline:
            raise ValidationError("Topshiriq muddati tugagan.")

        # Statusni aniqlash
        if self.response or self.description or self.file:
            self.status = 'assigned'
        else:
            self.status = 'given'

        if self.point > self.assignment.max_point:
            self.point = self.assignment.max_point

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.assignment.title} - {self.student.username} ({self.get_status_display()})"

    class Meta:
        ordering = ['-created_at']
