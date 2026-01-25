# bookshelf/forms.py
from django import forms
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
import re
from .models import Book, Library, CustomUser

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'library', 'published_date']
        widgets = {
            'published_date': forms.DateInput(attrs={'type': 'date'}),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter book title',
                'maxlength': '200'
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter author name',
                'maxlength': '100'
            }),
            'isbn': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter 10-13 digit ISBN',
                'pattern': '\d{10,13}',
                'title': 'ISBN must be 10-13 digits'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize form if needed
        self.fields['library'].queryset = Library.objects.all()
        self.fields['library'].widget.attrs.update({'class': 'form-control'})
    
    def clean_title(self):
        """Sanitize and validate book title."""
        title = self.cleaned_data.get('title', '')
        
        # Strip HTML tags
        title = strip_tags(title)
        
        # Remove excessive whitespace
        title = ' '.join(title.split())
        
        # Validate length
        if len(title) < 2:
            raise ValidationError(_('Title must be at least 2 characters long.'))
        if len(title) > 200:
            raise ValidationError(_('Title cannot exceed 200 characters.'))
        
        return title
    
    def clean_author(self):
        """Sanitize and validate author name."""
        author = self.cleaned_data.get('author', '')
        
        # Strip HTML tags
        author = strip_tags(author)
        
        # Remove excessive whitespace
        author = ' '.join(author.split())
        
        # Validate format (allow letters, spaces, hyphens, apostrophes)
        if not re.match(r'^[A-Za-z\s\-\'\.]+$', author):
            raise ValidationError(_('Author name contains invalid characters.'))
        
        if len(author) < 2:
            raise ValidationError(_('Author name must be at least 2 characters long.'))
        if len(author) > 100:
            raise ValidationError(_('Author name cannot exceed 100 characters.'))
        
        return author
    
    def clean_isbn(self):
        """Validate ISBN format."""
        isbn = self.cleaned_data.get('isbn', '')
        
        # Remove any hyphens or spaces
        isbn = re.sub(r'[-\s]', '', isbn)
        
        # Validate length and format
        if not re.match(r'^\d{10,13}$', isbn):
            raise ValidationError(_('ISBN must be 10-13 digits.'))
        
        # Check for duplicate ISBN (excluding current instance)
        if self.instance and self.instance.pk:
            if Book.objects.filter(isbn=isbn).exclude(pk=self.instance.pk).exists():
                raise ValidationError(_('A book with this ISBN already exists.'))
        else:
            if Book.objects.filter(isbn=isbn).exists():
                raise ValidationError(_('A book with this ISBN already exists.'))
        
        return isbn

# ============ EXAMPLE FORM FOR SECURITY DEMONSTRATION ============

class ExampleForm(forms.Form):
    """
    ExampleForm demonstrating security best practices.
    This form showcases input validation, sanitization, and security measures.
    """
    
    # Field with validation and sanitization
    user_input = forms.CharField(
        label='User Input',
        max_length=500,
        widget=forms.Textarea(attrs={
            'rows': 4,
            'cols': 50,
            'class': 'form-control',
            'placeholder': 'Enter text here (HTML will be stripped)',
            'maxlength': '500'
        }),
        help_text='Enter up to 500 characters. HTML tags will be removed.'
    )
    
    # Email field with validation
    email = forms.EmailField(
        label='Email Address',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your@email.com'
        }),
        help_text='Enter a valid email address.'
    )
    
    # Number field with range validation
    rating = forms.IntegerField(
        label='Rating (1-5)',
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '1',
            'max': '5'
        }),
        help_text='Rate from 1 to 5.'
    )
    
    # Choice field
    category = forms.ChoiceField(
        label='Category',
        choices=[
            ('', 'Select a category'),
            ('fiction', 'Fiction'),
            ('non-fiction', 'Non-Fiction'),
            ('academic', 'Academic'),
            ('other', 'Other')
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    
    # Checkbox for terms agreement
    agree_terms = forms.BooleanField(
        label='I agree to the terms and conditions',
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    def clean_user_input(self):
        """Sanitize user input to prevent XSS attacks."""
        user_input = self.cleaned_data.get('user_input', '')
        
        # 1. Strip HTML/JavaScript tags
        user_input = strip_tags(user_input)
        
        # 2. Remove potentially dangerous characters
        # Allow alphanumeric, spaces, and basic punctuation
        user_input = re.sub(r'[<>{}[\]]', '', user_input)
        
        # 3. Limit length (already done by max_length, but double-check)
        if len(user_input) > 500:
            raise ValidationError(_('Input cannot exceed 500 characters.'))
        
        # 4. Check for minimum length
        if len(user_input.strip()) < 10:
            raise ValidationError(_('Input must be at least 10 characters.'))
        
        # 5. Check for common attack patterns
        attack_patterns = [
            r'javascript:', 
            r'onclick=', 
            r'onload=', 
            r'alert\(', 
            r'<script',
            r'</script>',
            r'SELECT.*FROM',
            r'INSERT.*INTO',
            r'DELETE.*FROM',
            r'DROP.*TABLE',
            r'UNION.*SELECT'
        ]
        
        input_lower = user_input.lower()
        for pattern in attack_patterns:
            if re.search(pattern, input_lower):
                # Log suspicious input (in real app, you'd log this)
                raise ValidationError(_('Input contains suspicious content.'))
        
        return user_input
    
    def clean_email(self):
        """Validate and normalize email address."""
        email = self.cleaned_data.get('email', '').strip().lower()
        
        # Basic email validation (Django does this, but we add extra)
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValidationError(_('Please enter a valid email address.'))
        
        # Check for disposable email domains (example)
        disposable_domains = ['tempmail.com', 'throwawaymail.com']
        domain = email.split('@')[1] if '@' in email else ''
        if domain in disposable_domains:
            raise ValidationError(_('Disposable email addresses are not allowed.'))
        
        return email
    
    def clean(self):
        """Cross-field validation."""
        cleaned_data = super().clean()
        
        # Example: If rating is 5 and category is 'fiction', require longer input
        rating = cleaned_data.get('rating')
        category = cleaned_data.get('category')
        user_input = cleaned_data.get('user_input', '')
        
        if rating == 5 and category == 'fiction' and len(user_input) < 50:
            self.add_error(
                'user_input',
                _('For 5-star fiction ratings, please provide at least 50 characters of feedback.')
            )
        
        return cleaned_data

# ============ ADDITIONAL SECURITY-FOCUSED FORMS ============

class SecureSearchForm(forms.Form):
    """
    Secure search form with input validation to prevent injection attacks.
    """
    
    search_query = forms.CharField(
        label='Search',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search books...',
            'aria-label': 'Search',
            'maxlength': '100'
        })
    )
    
    def clean_search_query(self):
        """Sanitize search input."""
        query = self.cleaned_data.get('search_query', '')
        
        # Remove HTML tags
        query = strip_tags(query)
        
        # Remove potentially dangerous characters but keep useful ones
        # Allow alphanumeric, spaces, hyphens, apostrophes, commas, periods
        query = re.sub(r'[<>{}[\]\\|;]', '', query)
        
        # Trim whitespace
        query = query.strip()
        
        # Check for minimum search length (if provided)
        if query and len(query) < 2:
            raise ValidationError(_('Search query must be at least 2 characters.'))
        
        return query

class UserRegistrationForm(forms.ModelForm):
    """
    Secure user registration form with password validation.
    """
    
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password',
            'minlength': '8'
        }),
        help_text='Password must be at least 8 characters long.'
    )
    
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })
    )
    
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'date_of_birth']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
    
    def clean_password1(self):
        """Validate password strength."""
        password1 = self.cleaned_data.get('password1', '')
        
        # Check minimum length
        if len(password1) < 8:
            raise ValidationError(_('Password must be at least 8 characters long.'))
        
        # Check for common patterns
        if password1.lower() in ['password', '12345678', 'qwerty123']:
            raise ValidationError(_('This password is too common. Please choose a stronger one.'))
        
        # Check for at least one digit
        if not re.search(r'\d', password1):
            raise ValidationError(_('Password must contain at least one number.'))
        
        # Check for at least one uppercase letter
        if not re.search(r'[A-Z]', password1):
            raise ValidationError(_('Password must contain at least one uppercase letter.'))
        
        # Check for at least one lowercase letter
        if not re.search(r'[a-z]', password1):
            raise ValidationError(_('Password must contain at least one lowercase letter.'))
        
        return password1
    
    def clean(self):
        """Check that passwords match."""
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            self.add_error('password2', _('Passwords do not match.'))
        
        return cleaned_data
    
    def save(self, commit=True):
        """Save the user with hashed password."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        
        if commit:
            user.save()
        
        return user

# ============ FORM FOR SECURITY SETTINGS DEMONSTRATION ============

class SecuritySettingsForm(forms.Form):
    """
    Form demonstrating security-related settings and configurations.
    """
    
    enable_two_factor = forms.BooleanField(
        label='Enable Two-Factor Authentication',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        help_text='Add an extra layer of security to your account.'
    )
    
    session_timeout = forms.IntegerField(
        label='Session Timeout (minutes)',
        min_value=5,
        max_value=1440,  # 24 hours
        initial=30,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '5',
            'max': '1440'
        }),
        help_text='Automatically log out after inactivity.'
    )
    
    login_notifications = forms.BooleanField(
        label='Login Notifications',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        help_text='Receive email notifications for new logins.'
    )
    
    allowed_ip_ranges = forms.CharField(
        label='Allowed IP Ranges (comma-separated)',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '192.168.1.0/24, 10.0.0.0/8'
        }),
        help_text='Restrict access to specific IP ranges. Leave empty for no restrictions.'
    )
    
    def clean_allowed_ip_ranges(self):
        """Validate IP ranges format."""
        ip_ranges = self.cleaned_data.get('allowed_ip_ranges', '')
        
        if not ip_ranges:
            return ip_ranges
        
        ranges = [r.strip() for r in ip_ranges.split(',')]
        
        # Simple IP range validation (in production, use proper IP validation)
        for ip_range in ranges:
            if ip_range and not re.match(r'^\d{1,3}(\.\d{1,3}){0,3}(/\d{1,2})?$', ip_range):
                raise ValidationError(
                    _('Invalid IP range format: %(range)s. Use format like 192.168.1.0/24'),
                    params={'range': ip_range}
                )
        
        return ip_ranges