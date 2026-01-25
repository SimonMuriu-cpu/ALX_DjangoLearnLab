# Add this import at the top
from .forms import ExampleForm, SecureSearchForm, UserRegistrationForm, SecuritySettingsForm

# Add this view function
def example_form_view(request):
    """
    View demonstrating secure form handling with ExampleForm.
    """
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Process cleaned data
            user_input = form.cleaned_data['user_input']
            email = form.cleaned_data['email']
            rating = form.cleaned_data['rating']
            category = form.cleaned_data['category']
            
            # In a real application, you would save to database
            # For demonstration, just show success
            
            # Log the submission (in production)
            import logging
            logger = logging.getLogger('django.security')
            logger.info(f'Secure form submission from {email}')
            
            # Show success message
            from django.contrib import messages
            messages.success(request, 'Form submitted securely!')
            
            return redirect('example_form_success')
    else:
        form = ExampleForm()
    
    return render(request, 'bookshelf/example_form.html', {'form': form})

def example_form_success(request):
    """Success page for example form submission."""
    return render(request, 'bookshelf/example_form_success.html')

# Add view for secure search form demonstration
def secure_search_demo(request):
    """Demonstrate secure search form."""
    form = SecureSearchForm(request.GET or None)
    results = []
    
    if form.is_valid():
        query = form.cleaned_data.get('search_query')
        if query:
            # Safe search using Django ORM
            results = Book.objects.filter(
                Q(title__icontains=query) | Q(author__icontains=query)
            )[:10]
    
    return render(request, 'bookshelf/secure_search.html', {
        'form': form,
        'results': results,
        'query': form.cleaned_data.get('search_query', '') if form.is_valid() else ''
    })