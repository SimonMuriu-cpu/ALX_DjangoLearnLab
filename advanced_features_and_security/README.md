## Documentation for custom permissions


# Permissions and Groups Setup

## Overview
This Django application implements a custom permission system with user groups to control access to book and library resources.

## Groups Created
1. **Viewers**: Can view books and libraries
2. **Editors**: Can view, create, and edit books and libraries
3. **Admins**: Can perform all actions (view, create, edit, delete)

## Permissions Defined
For both Book and Library models:
- `can_view`: Permission to view resources
- `can_create`: Permission to create new resources
- `can_edit`: Permission to edit existing resources
- `can_delete`: Permission to delete resources

## How to Set Up
1. Run migrations to create permission models:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
