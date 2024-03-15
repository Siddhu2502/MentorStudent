from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.mail import send_mail

class Mentor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Evaluation(models.Model):
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='evaluations')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='evaluations')
    ideation_marks = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    execution_marks = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    viva_marks = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    total_marks = models.PositiveIntegerField(editable=False, default=0)
    is_submitted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('mentor', 'student')

    def __str__(self):
        return f"{self.mentor.name} - {self.student.name}"

    def clean(self):
        if Evaluation.objects.filter(mentor=self.mentor).exclude(pk=self.pk).count() >= 4:
            raise ValidationError("A mentor can have a maximum of 4 students.")

        if Evaluation.objects.filter(student=self.student).exclude(pk=self.pk).exists():
            raise ValidationError("A student cannot be assigned to multiple mentors.")

    def send_mail_if_submitted(self):
        if self.is_submitted:
            subject = f"Evaluation Marks Submitted for {self.student.name}"
            message = f"Dear {self.student.name},\n\nYour marks have been submitted.\n\n your marks are \n\nIdeation: {self.ideation_marks}\nExecution: {self.execution_marks}\nViva: {self.viva_marks}\n Total: {self.total_marks} \n\n Thanks"
            from_email = self.mentor.email
            recipient_list = [self.student.email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

    def save(self, *args, **kwargs):
        self.total_marks = self.ideation_marks + self.execution_marks + self.viva_marks
        super().save(*args, **kwargs)
        self.send_mail_if_submitted()