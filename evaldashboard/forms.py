from django import forms
from .models import Mentor, Student, Evaluation

class MentorForm(forms.ModelForm):
    class Meta:
        model = Mentor
        fields = ['name', 'email', 'phone']

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email', 'phone']

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['student', 'ideation_marks', 'execution_marks', 'viva_marks', 'is_submitted']

    def __init__(self, *args, **kwargs):
        mentor = kwargs.pop('mentor', None)
        super().__init__(*args, **kwargs)
        if mentor:
            self.instance.mentor = mentor
            self.fields['student'].queryset = Student.objects.exclude(evaluations__mentor=mentor)
        else:
            self.fields['student'].queryset = Student.objects.all()
        self.fields['ideation_marks'].initial = 0
        self.fields['execution_marks'].initial = 0
        self.fields['viva_marks'].initial = 0
        # self.fields['is_submitted'].initial = False