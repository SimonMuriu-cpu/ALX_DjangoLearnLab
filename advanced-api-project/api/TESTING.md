# Testing Documentation

## Overview
This document describes the unit testing strategy for the Book API endpoints.

## Test Structure
Tests are organized in `api/tests.py` and cover:
1. CRUD operations for Book model
2. Filtering, searching, and ordering functionality
3. Authentication and permission controls

## Running Tests
To run all tests:
```bash
python manage.py test api