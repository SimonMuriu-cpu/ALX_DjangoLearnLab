from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

def is_admin(user):
    return user.userprofile.role == 'Admin'

def is_librarian(user):
    return user.userprofile.role == 'Librarian'

def is_member(user):
    return user.userprofile.role == 'Member'


@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'accounts/admin_view.html')


@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'accounts/librarian_view.html')


@user_passes_test(is_member)
def member_view(request):
    return render(request, 'accounts/member_view.html')
