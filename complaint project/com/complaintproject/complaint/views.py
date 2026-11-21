from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import ComplaintForm
from .models import Complaint


# ================= STUDENT =================

def student_register(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        
        # Validation
        if not username or not email or not password:
            error = 'All fields are required.'
        elif User.objects.filter(username=username).exists():
            error = f'Username "{username}" already exists. Please choose a different username.'
        elif User.objects.filter(email=email).exists():
            error = 'Email already registered. Please use a different email.'
        else:
            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            return redirect('student_login')
    
    return render(request, 'student_register.html', {'error': error})


def student_login(request):
    error = None
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user and not user.is_superuser:
            login(request, user)
            return redirect('student_dashboard')
        else:
            error = 'Invalid username or password.'
    
    return render(request, 'student_login.html', {'error': error})


@login_required
def student_dashboard(request):
    complaints = Complaint.objects.filter(student=request.user)
    return render(request, 'student_dashboard.html', {'complaints': complaints})


@login_required
def add_complaint(request):
    form = ComplaintForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        complaint = form.save(commit=False)
        complaint.student = request.user
        complaint.save()
        return redirect('student_dashboard')

    return render(request, 'add_complaint.html', {'form': form})


@login_required
def student_view(request, id):
    complaint = get_object_or_404(Complaint, id=id, student=request.user)
    return render(request, 'student_view.html', {'complaint': complaint})


@login_required
def edit_complaint(request, id):
    complaint = get_object_or_404(Complaint, id=id, student=request.user)

    if complaint.status != "Pending":
        return redirect('student_dashboard')

    if request.method == 'POST':
        complaint.title = request.POST['title']
        complaint.category = request.POST['category']
        complaint.description = request.POST['description']
        complaint.save()
        return redirect('student_dashboard')

    return render(request, 'edit_complaint.html', {'complaint': complaint})


@login_required
def delete_complaint(request, id):
    complaint = get_object_or_404(Complaint, id=id, student=request.user)

    if request.method == 'POST' and complaint.status == "Pending":
        complaint.delete()

    return redirect('student_dashboard')


def student_logout(request):
    logout(request)
    return redirect('student_login')


# ================= ADMIN =================

def admin_login(request):
    error = None
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user and user.is_superuser:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            error = 'Invalid admin credentials.'
    
    return render(request, 'admin_login.html', {'error': error})


@login_required
def admin_dashboard(request):
    complaints = Complaint.objects.all()
    return render(request, 'admin_dashboard.html', {'complaints': complaints})


@login_required
def admin_view(request, id):
    complaint = get_object_or_404(Complaint, id=id)
    return render(request, 'admin_view.html', {'complaint': complaint})


@login_required
def approve_complaint(request, id):
    complaint = get_object_or_404(Complaint, id=id)
    complaint.status = "Approved"
    complaint.save()
    return redirect('admin_dashboard')


@login_required
def reject_complaint(request, id):
    complaint = get_object_or_404(Complaint, id=id)
    complaint.status = "Rejected"
    complaint.save()
    return redirect('admin_dashboard')


def admin_logout(request):
    logout(request)
    return redirect('admin_login')
