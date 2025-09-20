# 🧪 Testing Guide for QuickPick Multi-Agent System

This document provides comprehensive information about testing the QuickPick Multi-Agent System.

## 📁 Test Structure

```
tests/
├── __init__.py                 # Test package initialization
├── conftest.py                 # Pytest configuration and shared fixtures
├── unit/                       # Unit tests
│   ├── __init__.py
│   ├── test_base_agent.py      # BaseAgent tests
│   ├── test_food_agent.py      # FoodAgent tests
│   ├── test_quick_commerce_agent.py  # QuickCommerceAgent tests
│   └── test_master_agent.py    # MasterAgent tests
├── integration/                # Integration tests
│   ├── __init__.py
│   └── test_api_integration.py # API endpoint tests
├── e2e/                        # End-to-end tests
│   ├── __init__.py
│   └── test_complete_workflows.py  # Complete workflow tests
├── fixtures/                   # Test data and fixtures
│   ├── __init__.py
│   └── sample_data.json        # Sample test data
└── mocks/                      # Mock objects
    ├── __init__.py
    └── mock_clients.py         # Mock API clients
```

## 🚀 Quick Start

### 1. Install Test Dependencies

```bash
# Using the test runner
python run_tests.py --install-deps

# Or manually
pip install pytest pytest-asyncio pytest-cov pytest-mock
pip install httpx fastapi[all]
```

### 2. Run Tests

```bash
# Run all tests
python run_tests.py --all

# Run specific test types
python run_tests.py --unit
python run_tests.py --integration
python run_tests.py --e2e

# Run with coverage
python run_tests.py --all --coverage

# Run specific test file
python run_tests.py --test tests/unit/test_food_agent.py

# Run tests with specific markers
python run_tests.py --markers "unit and not slow"
```

## 🧪 Test Types

### Unit Tests

Test individual components in isolation:

```bash
# Run all unit tests
pytest tests/unit/

# Run specific unit test
pytest tests/unit/test_food_agent.py::TestFoodAgent::test_process_request_meal_planning

# Run with verbose output
pytest tests/unit/ -v
```

**Coverage:**
- BaseAgent functionality
- Individual agent methods
- Utility functions
- Data validation
- Error handling

### Integration Tests

Test component interactions:

```bash
# Run all integration tests
pytest tests/integration/

# Run specific integration test
pytest tests/integration/test_api_integration.py::TestAPIIntegration::test_assistant_endpoint_food_request
```

**Coverage:**
- API endpoint functionality
- Agent coordination
- External service integration
- Database interactions
- Authentication flows

### End-to-End Tests

Test complete user workflows:

```bash
# Run all E2E tests
pytest tests/e2e/

# Run specific workflow test
pytest tests/e2e/test_complete_workflows.py::TestCompleteWorkflows::test_complete_meal_planning_workflow
```

**Coverage:**
- Complete user journeys
- Multi-agent workflows
- Error recovery
- Performance under load
- Concurrent user scenarios

## 🔧 Test Configuration

### Pytest Configuration

The `pytest.ini` file configures:

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --tb=short
    --strict-markers
    --disable-warnings
    --color=yes
    --durations=10
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    slow: Slow running tests
    api: API tests
    agent: Agent tests
asyncio_mode = auto
```

### Test Fixtures

The `conftest.py` file provides shared fixtures:

- **Mock Clients**: Mocked external API clients
- **Agent Instances**: Pre-configured agent instances
- **Sample Data**: Test data for various scenarios
- **Async Support**: Async test helpers

### Environment Setup

Tests use environment variables for configuration:

```bash
# Set test environment variables
export SPOONACULAR_API_KEY="test_key"
export GROQ_API_KEY="test_key"
export RAZORPAY_API_KEY="test_key"
export RAZORPAY_API_SECRET="test_secret"
export LOG_LEVEL="DEBUG"
```

## 📊 Coverage Reports

### Generate Coverage Report

```bash
# Generate HTML and terminal coverage reports
python run_tests.py --all --coverage

# Or manually
pytest tests/ --cov=agents --cov=master --cov=mcp --cov-report=html --cov-report=term
```

### View Coverage Report

```bash
# Open HTML coverage report
open htmlcov/index.html

# Or on Linux
xdg-open htmlcov/index.html
```

### Coverage Targets

- **Overall Coverage**: > 80%
- **Critical Paths**: > 90%
- **New Code**: > 95%

## 🎯 Test Markers

Use markers to categorize and filter tests:

```python
@pytest.mark.unit
def test_agent_initialization():
    pass

@pytest.mark.integration
def test_api_endpoint():
    pass

@pytest.mark.e2e
def test_complete_workflow():
    pass

@pytest.mark.slow
def test_performance():
    pass
```

### Run Tests by Marker

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run only E2E tests
pytest -m e2e

# Run tests excluding slow ones
pytest -m "not slow"

# Run unit and integration tests
pytest -m "unit or integration"
```

## 🔍 Debugging Tests

### Verbose Output

```bash
# Run with verbose output
pytest tests/ -v

# Run with extra verbose output
pytest tests/ -vv

# Show local variables on failure
pytest tests/ -l
```

### Debug Specific Test

```bash
# Run specific test with debugging
pytest tests/unit/test_food_agent.py::TestFoodAgent::test_process_request_meal_planning -v -s

# Drop into debugger on failure
pytest tests/ --pdb

# Drop into debugger on first failure
pytest tests/ --pdb -x
```

### Test Discovery

```bash
# List all tests
pytest --collect-only

# List tests in specific file
pytest tests/unit/test_food_agent.py --collect-only

# Show test collection warnings
pytest --collect-only -W default
```

## 🚀 CI/CD Integration

### GitHub Actions

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.10
      - name: Install dependencies
        run: |
          pip install -e .
          pip install pytest pytest-asyncio pytest-cov
      - name: Run tests
        run: python run_tests.py --ci
```

### Local CI Pipeline

```bash
# Run full CI pipeline locally
python run_tests.py --ci
```

This runs:
- All tests with coverage
- Code linting (flake8)
- Code formatting check (black)
- Import sorting check (isort)
- Type checking (mypy)

## 📝 Writing Tests

### Unit Test Example

```python
import pytest
from unittest.mock import Mock, AsyncMock
from agents.food_agent import FoodAgent

class TestFoodAgent:
    def test_initialization(self):
        agent = FoodAgent()
        assert agent.agent_id == "food_agent"
        assert "meal_planning" in agent.capabilities

    @pytest.mark.asyncio
    async def test_process_request_meal_planning(self, food_agent):
        request_data = {
            "task_type": "meal_planning",
            "calories": 500,
            "diet": "vegetarian"
        }
        
        result = await food_agent.process_request(request_data, {})
        
        assert result["status"] == "success"
        assert "meal_plan" in result["data"]
```

### Integration Test Example

```python
import pytest
from fastapi.testclient import TestClient
from main import app

class TestAPIIntegration:
    @pytest.fixture
    def client(self):
        return TestClient(app)

    def test_assistant_endpoint_food_request(self, client):
        request_data = {
            "message": "Plan a healthy dinner",
            "user_id": "test_user",
            "context": {}
        }
        
        response = client.post("/assistant", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["agent_used"] == "food"
```

### E2E Test Example

```python
import pytest
from fastapi.testclient import TestClient
from main import app

class TestCompleteWorkflows:
    @pytest.fixture
    def client(self):
        return TestClient(app)

    def test_complete_meal_planning_workflow(self, client):
        # Step 1: Plan a meal
        meal_request = {
            "message": "Plan a healthy dinner for tonight",
            "user_id": "test_user",
            "context": {}
        }
        
        response = client.post("/assistant", json=meal_request)
        assert response.status_code == 200
        meal_data = response.json()
        assert meal_data["agent_used"] == "food"
        
        # Step 2: Generate grocery list
        grocery_request = {
            "message": "Create a grocery list from the meal plan",
            "user_id": "test_user",
            "context": meal_data["data"]
        }
        
        response = client.post("/assistant", json=grocery_request)
        assert response.status_code == 200
        grocery_data = response.json()
        assert grocery_data["status"] == "success"
```

## 🐛 Common Issues

### Import Errors

```bash
# Add project root to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Or use pytest with Python path
pytest --pythonpath=. tests/
```

### Async Test Issues

```python
# Use pytest-asyncio
@pytest.mark.asyncio
async def test_async_function():
    result = await async_function()
    assert result is not None
```

### Mock Issues

```python
# Use AsyncMock for async functions
mock_client = Mock()
mock_client.async_method = AsyncMock(return_value="test_result")

# Use side_effect for exceptions
mock_client.method.side_effect = Exception("Test error")
```

### Environment Variables

```python
# Use monkeypatch in tests
def test_with_env_vars(monkeypatch):
    monkeypatch.setenv("API_KEY", "test_key")
    # Test code here
```

## 📈 Performance Testing

### Load Testing

```python
import pytest
import asyncio
from concurrent.futures import ThreadPoolExecutor

class TestPerformance:
    def test_concurrent_requests(self, client):
        def make_request():
            response = client.post("/assistant", json={
                "message": "Test message",
                "user_id": "test_user"
            })
            return response.status_code
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(100)]
            results = [future.result() for future in futures]
        
        assert all(status == 200 for status in results)
```

### Memory Testing

```python
import pytest
import psutil
import os

class TestMemory:
    def test_memory_usage(self):
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Run memory-intensive operations
        # ...
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Assert memory increase is reasonable
        assert memory_increase < 100 * 1024 * 1024  # 100MB
```

## 🔧 Test Utilities

### Custom Fixtures

```python
@pytest.fixture
def sample_user_data():
    return {
        "user_id": "test_user_123",
        "preferences": {
            "dietary_restrictions": ["vegetarian"],
            "allergies": ["nuts"]
        }
    }

@pytest.fixture
def mock_api_response():
    return {
        "status": "success",
        "data": {"result": "test_data"},
        "timestamp": "2024-01-01T00:00:00Z"
    }
```

### Test Helpers

```python
def assert_valid_response(response_data):
    """Helper to validate API response format."""
    assert "status" in response_data
    assert "data" in response_data
    assert response_data["status"] in ["success", "error"]

def create_test_order():
    """Helper to create test order data."""
    return {
        "order_id": "test_order_123",
        "items": [{"name": "test_item", "quantity": 1}],
        "total_amount": 100.0
    }
```

## 📚 Best Practices

### Test Organization

1. **One test class per component**
2. **Descriptive test names**
3. **Arrange-Act-Assert pattern**
4. **Independent tests**
5. **Clear assertions**

### Test Data

1. **Use fixtures for shared data**
2. **Create realistic test data**
3. **Use factories for complex objects**
4. **Clean up test data**

### Mocking

1. **Mock external dependencies**
2. **Use AsyncMock for async functions**
3. **Verify mock calls**
4. **Don't mock the system under test**

### Error Testing

1. **Test error conditions**
2. **Test edge cases**
3. **Test validation failures**
4. **Test timeout scenarios**

## 🎯 Test Goals

### Coverage Targets

- **Unit Tests**: > 90% coverage
- **Integration Tests**: > 80% coverage
- **E2E Tests**: > 70% coverage
- **Overall**: > 85% coverage

### Performance Targets

- **Unit Tests**: < 1 second per test
- **Integration Tests**: < 5 seconds per test
- **E2E Tests**: < 30 seconds per test
- **Total Test Suite**: < 10 minutes

### Quality Targets

- **Zero flaky tests**
- **Clear error messages**
- **Fast feedback loop**
- **Easy to maintain**

---

**Happy Testing! 🎉**

For more information, see the main [README.md](README.md) or contact the development team.
