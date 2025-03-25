import pytest
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_order_sql_injection():
    """Test order placement for SQL injection vulnerability via location field."""
    with client.session_transaction() as sess:
        sess['user_id'] = 1
        sess['name'] = 'Ritika Verma'
    
    # Attempt SQL injection in the 'location' field for order placement
    response = client.post('/place_order', json={
        'cart_items': [1, 2],
        'location': "' OR '1'='1'; --"
    })
    # Expect the system to reject the injection attempt (e.g., HTTP 400 or 401)
    assert response.status_code in (400, 401)

def test_order_xss():
    """Test order placement for XSS vulnerability in the location field."""
    with client.session_transaction() as sess:
        sess['user_id'] = 1
        sess['name'] = 'Ritika Verma'
    
    response = client.post('/place_order', json={
        'cart_items': [1, 2],
        'location': "<script>alert('XSS');</script>"
    })
    # Expect the system to sanitize input and reject the script input
    assert response.status_code in (400, 401)

def test_order_with_excessively_long_input():
    """Test order placement with excessively long input to check for potential DoS issues."""
    with client.session_transaction() as sess:
        sess['user_id'] = 1
        sess['name'] = 'Ritika Verma'
    
    long_location = "L" * 10000  # Excessively long location string
    response = client.post('/place_order', json={
        'cart_items': [1, 2],
        'location': long_location
    })
    # Expect the server to handle or reject the input gracefully
    assert response.status_code in (400, 401)

def test_order_special_characters():
    """Test order placement with special characters in the location field."""
    with client.session_transaction() as sess:
        sess['user_id'] = 1
        sess['name'] = 'Ritika Verma'
    
    response = client.post('/place_order', json={
        'cart_items': [1, 2],
        'location': "Lucas!@#$%^&*()Hall"
    })
    # Depending on the validation rules, expect the input to be rejected or sanitized
    assert response.status_code in (400, 401)

if __name__ == '__main__':
    pytest.main()
