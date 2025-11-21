# Testing Guide

## Setup

Install test dependencies:
```powershell
pip install -r requirements.txt
```

## Running Tests

### Run all tests
```powershell
pytest tests/
```

### Run with verbose output
```powershell
pytest tests/ -v
```

### Run specific test file
```powershell
pytest tests/test_screenshot_service.py
pytest tests/test_email_service.py
```

### Run with coverage report
```powershell
pytest tests/ --cov=services --cov-report=html
```
Then open `htmlcov/index.html` to view detailed coverage.

### Run specific test class or method
```powershell
pytest tests/test_screenshot_service.py::TestTakeScreenshot::test_single_monitor_success
```

## Test Structure

```
tests/
├── __init__.py                    # Makes tests a package
├── test_screenshot_service.py     # 8 test cases for screenshot service
├── test_email_service.py          # 12 test cases for email service
└── README.md                      # This file
```

## What's Tested

### Screenshot Service (`test_screenshot_service.py`)
- ✓ Single monitor capture
- ✓ Multiple monitor capture  
- ✓ No monitors detected handling
- ✓ Exception handling
- ✓ Directory creation
- ✓ Hostname in path
- ✓ Timestamp formatting
- ✓ File naming conventions

### Email Service (`test_email_service.py`)
- ✓ Simple plain text emails
- ✓ HTML emails
- ✓ Multiple recipients (To, CC, BCC)
- ✓ Email attachments (single/multiple)
- ✓ Missing attachment handling
- ✓ SMTP exception handling
- ✓ Authentication failures
- ✓ Connection timeouts
- ✓ Error propagation (raise_on_error flag)
- ✓ SMTP connection parameters

## Best Practices

1. **Run tests before committing**: `pytest tests/`
2. **Check coverage**: `pytest tests/ --cov=services`
3. **Keep tests isolated**: Each test uses mocks, no real files/emails sent
4. **Add tests for new features**: When adding new functions, add corresponding tests

## Continuous Integration

To run tests in CI/CD pipelines:
```yaml
# Example GitHub Actions
- name: Run tests
  run: |
    pip install -r requirements.txt
    pytest tests/ --cov=services --cov-report=xml
```

## Troubleshooting

**Import errors**: Make sure you're in the project root directory when running pytest.

**Module not found**: Install dependencies: `pip install -r requirements.txt`

**Tests fail**: Check that config/settings.py exists and has required variables.
