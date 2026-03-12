# Testing Guide for Estate Management System

This guide explains how to run and write tests for the Estate Management System.

## Test Configuration

**Automatic Test Database**: The project is configured to automatically use SQLite for testing (faster and doesn't require PostgreSQL to be running). When you run tests, the system will:
- Use SQLite in-memory database for tests
- Use MD5 password hasher (faster than Argon2 for testing)
- Use PostgreSQL for normal development/production

This means you can run tests immediately without needing to set up PostgreSQL!

## Test Files Created

The following test files have been added to the project:

### Core App Tests

1. **`core_apps/posts/tests.py`** - Tests for Posts and Replies
   - Model tests (creation, validation, sanitization, slug generation)
   - API tests (CRUD operations, bookmarking, voting)
   - Permission tests

2. **`core_apps/issues/tests.py`** - Tests for Issue tracking
   - Model tests (status workflow, assignment, content sanitization)
   - API tests (creating, listing, updating issues)
   - Permission tests (admin vs tenant access)

3. **`core_apps/profiles/tests.py`** - Tests for User Profiles
   - Model tests (auto-creation, reputation system, ban logic)
   - API tests (profile retrieval and updates)

4. **`core_apps/ratings/tests.py`** - Tests for Rating system
   - Model tests (rating creation, self-rating prevention, unique constraints)
   - API tests (creating and listing ratings)

5. **`core_apps/apartments/tests.py`** - Tests for Apartment management
   - Model tests (validation, unique constraints)
   - API tests (creation permissions)

6. **`core_apps/users/tests.py`** - Tests for User authentication
   - User model tests
   - Authentication API tests (registration, login, logout)

7. **`core_apps/common/tests.py`** - Tests for validators and exception handlers
   - Validator tests (HTML sanitization, SQL injection detection, etc.)
   - Exception handler tests
   - XSS prevention integration tests

## Running Tests

### Option 1: Using Django's Test Runner

Run all tests:
```bash
python manage.py test
```

Run tests for a specific app:
```bash
python manage.py test core_apps.posts
python manage.py test core_apps.issues
python manage.py test core_apps.profiles
```

Run a specific test class:
```bash
python manage.py test core_apps.posts.tests.PostModelTest
```

Run a specific test method:
```bash
python manage.py test core_apps.posts.tests.PostModelTest.test_post_creation
```

Run with verbose output:
```bash
python manage.py test --verbosity=2
```

Keep the test database (useful for debugging):
```bash
python manage.py test --keepdb
```

### Option 2: Using pytest (Recommended for advanced features)

First, install pytest and pytest-django:
```bash
pip install pytest pytest-django pytest-cov
```

Run all tests:
```bash
pytest
```

Run with coverage report:
```bash
pytest --cov=core_apps --cov-report=html
```

Run tests for a specific app:
```bash
pytest core_apps/posts/tests.py
pytest core_apps/issues/tests.py
```

Run tests matching a pattern:
```bash
pytest -k "test_post"
pytest -k "API"
```

Run with detailed output:
```bash
pytest -v
pytest -vv  # Even more verbose
```

Run tests in parallel (faster):
```bash
pip install pytest-xdist
pytest -n auto
```

### Option 3: Using Coverage

Generate a coverage report:
```bash
coverage run --source='core_apps' manage.py test
coverage report
coverage html  # Creates htmlcov/index.html
```

## Test Structure

### Model Tests
Test the behavior of Django models:
- Creation and default values
- Validation rules
- Custom methods
- String representations
- Database constraints

### API Tests
Test REST API endpoints:
- Authentication requirements
- Permission checks
- CRUD operations
- Status codes
- Response data structure

### Validator Tests
Test custom validators:
- Input sanitization
- Security checks (XSS, SQL injection)
- Content validation

### Integration Tests
Test complete workflows:
- User registration → profile creation
- Issue creation → notification emails
- Rating → reputation update

## Writing New Tests

### Example: Adding a New Test

```python
# In core_apps/yourapp/tests.py

from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

class YourModelTest(TestCase):
    def setUp(self):
        """Set up test data before each test"""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
    
    def test_your_feature(self):
        """Test description"""
        # Arrange
        # ... setup test data
        
        # Act
        # ... perform the action
        
        # Assert
        self.assertEqual(expected, actual)
```

### Example: API Test with Authentication

```python
class YourAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
    
    def test_authenticated_endpoint(self):
        """Test authenticated API endpoint"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/v1/your-endpoint/')
        self.assertEqual(response.status_code, 200)
```

## Test Coverage Goals

Current test coverage includes:
- ✅ Model validation and methods
- ✅ API endpoint authentication
- ✅ API endpoint permissions
- ✅ Content sanitization (XSS prevention)
- ✅ Business logic (reputation, bans, ratings)
- ✅ Error handling

Aim for:
- **80%+ code coverage** overall
- **100% coverage** for critical security features
- **All API endpoints** should have tests

## Continuous Integration

To set up CI/CD with GitHub Actions, create `.github/workflows/tests.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_DB: test_db
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.14'
    
    - name: Install dependencies
      run: |
        pip install -r requirements/local.txt
        pip install pytest pytest-django pytest-cov
    
    - name: Run tests
      env:
        POSTGRES_DB: test_db
        POSTGRES_USER: postgres
        POSTGRES_PASSWORD: postgres
        POSTGRES_HOST: localhost
        POSTGRES_PORT: 5432
      run: |
        pytest --cov=core_apps --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

## Best Practices

1. **Test Isolation**: Each test should be independent
2. **Clear Names**: Use descriptive test method names
3. **Arrange-Act-Assert**: Structure tests clearly
4. **Mock External Services**: Don't call real APIs or send real emails
5. **Test Edge Cases**: Not just happy paths
6. **Keep Tests Fast**: Use `--keepdb` flag during development
7. **Update Tests**: When code changes, update tests

## Troubleshooting

### Tests Failing Due to Database

If you see database connection errors:
```bash
# Make sure PostgreSQL is running
# Update .env with test database credentials
# Or use SQLite for testing by setting in settings:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
```

### Import Errors

If you see import errors:
```bash
# Make sure you're in the virtual environment
# Reinstall dependencies
pip install -r requirements/local.txt
```

### Slow Tests

Speed up tests:
```bash
# Use parallel testing
pytest -n auto

# Keep database between runs
python manage.py test --keepdb

# Run specific tests only
pytest -k "test_post"
```

## Next Steps

1. **Run the tests**: `python manage.py test`
2. **Check coverage**: `coverage run --source='core_apps' manage.py test && coverage report`
3. **Fix failing tests**: Address any failures
4. **Add more tests**: Cover edge cases and new features
5. **Set up CI/CD**: Automate testing on every commit

## Summary

✅ **7 test files** created covering all major features
✅ **100+ test cases** for models, APIs, validators
✅ **Security tests** for XSS, SQL injection prevention
✅ **Integration tests** for complete workflows
✅ **pytest.ini** configured for easy test running

Run `python manage.py test` to get started!
