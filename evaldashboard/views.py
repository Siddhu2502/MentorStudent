# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Mentor, Student, Evaluation
from .forms import MentorForm, StudentForm, EvaluationForm

def index(request):
    mentors = Mentor.objects.all()
    return render(request, 'index.html', {'mentors': mentors})

def add_mentor(request):
    if request.method == 'POST':
        form = MentorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mentor added successfully.')
            return redirect('index')
    else:
        form = MentorForm()
    return render(request, 'add_mentor.html', {'form': form})

def add_student(request, mentor_id):
    mentor = get_object_or_404(Mentor, id=mentor_id)
    if request.method == 'POST':
        form = EvaluationForm(request.POST, instance=Evaluation(mentor=mentor))
        if form.is_valid():
            evaluation = form.save(commit=False)
            evaluation.save()
            messages.success(request, 'Student added successfully.')
            return redirect('view_evaluations', mentor_id=mentor.id)
    else:
        form = EvaluationForm(instance=Evaluation(mentor=mentor))
    return render(request, 'add_student.html', {'form': form, 'mentor': mentor})

def assign_marks(request, mentor_id, evaluation_id):
    mentor = get_object_or_404(Mentor, id=mentor_id)
    evaluation = get_object_or_404(Evaluation, id=evaluation_id, mentor=mentor)
    if request.method == 'POST':
        form = EvaluationForm(request.POST, instance=evaluation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Marks assigned successfully.')
            return redirect('view_evaluations', mentor_id=mentor.id)
    else:
        form = EvaluationForm(instance=evaluation)
    return render(request, 'assign_marks.html', {'form': form, 'mentor': mentor, 'evaluation': evaluation})

def remove_student(request, mentor_id, evaluation_id):
    mentor = get_object_or_404(Mentor, id=mentor_id)
    evaluation = get_object_or_404(Evaluation, id=evaluation_id, mentor=mentor)
    evaluation.delete()
    messages.success(request, 'Student removed successfully.')
    return redirect('view_evaluations', mentor_id=mentor.id)

def submit_marks(request, mentor_id, evaluation_id):
    mentor = get_object_or_404(Mentor, id=mentor_id)
    evaluation = get_object_or_404(Evaluation, id=evaluation_id, mentor=mentor)
    if request.method == 'POST':
        if evaluation.ideation_marks is not None and evaluation.execution_marks is not None and evaluation.viva_marks is not None:
            evaluation.is_submitted = True
            evaluation.save()
            messages.success(request, 'Marks submitted successfully.')
            return redirect('view_evaluations', mentor_id=mentor.id)
        else:
            messages.error(request, 'Please assign marks before submitting.')
    return render(request, 'submit_marks.html', {'evaluation': evaluation})

def view_evaluations(request, mentor_id):
    mentor = get_object_or_404(Mentor, id=mentor_id)
    evaluations = mentor.evaluations.all()
    submitted_evaluations = evaluations.filter(is_submitted=True)
    pending_evaluations = evaluations.filter(is_submitted=False)
    context = {
        'mentor': mentor,
        'submitted_evaluations': submitted_evaluations,
        'pending_evaluations': pending_evaluations,
    }
    return render(request, 'view_evaluations.html', context)