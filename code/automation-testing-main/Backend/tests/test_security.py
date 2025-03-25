import pytest
import requests

BASE_URL = "http://localhost:5000"

def test_sql_injection_login():
    """Test login for SQL injection vulnerability via email field."""
    data = {"scu_email": "' OR '1'='1'; --", "scu_id": "0000000000"}
    response = requests.post(f"{BASE_URL}/", data=data)
    # Expecting the system to safely reject the injected input
    assert response.status_code == 401

def test_xss_login():
    """Test login for Cross-Site Scripting (XSS) injection via email field."""
    data = {"scu_email": "<script>alert('XSS');</script>", "scu_id": "1234567890"}
    response = requests.post(f"{BASE_URL}/", data=data)
    # Expecting the system to safely reject the script input
    assert response.status_code == 401

def test_sql_injection_in_scu_id():
    """Test login for SQL injection vulnerability via SCU ID field."""
    data = {"scu_email": "test@scu.edu", "scu_id": "1234567890' OR '1'='1"}
    response = requests.post(f"{BASE_URL}/", data=data)
    # The input should be rejected as it tries to alter the query logic.
    assert response.status_code == 401

def test_xss_in_scu_id():
    """Test login for XSS injection in the SCU ID field."""
    data = {"scu_email": "test@scu.edu", "scu_id": "<script>alert('XSS');</script>"}
    response = requests.post(f"{BASE_URL}/", data=data)
    # The system should not execute or accept script input in the ID field.
    assert response.status_code == 401

def test_long_input_login():
    """Test login with excessively long input values to check for potential DoS issues."""
    long_email = "a" * 10000 + "@scu.edu"
    long_id = "1" * 10000
    data = {"scu_email": long_email, "scu_id": long_id}
    response = requests.post(f"{BASE_URL}/", data=data)
    # The server should gracefully handle or reject overly long inputs.
    assert response.status_code in (400, 401)

def test_special_characters_login():
    """Test login with a variety of special characters in the email field."""
    data = {"scu_email": "test!#$%&'*+/=?^_`{|}~-@scu.edu", "scu_id": "1234567890"}
    response = requests.post(f"{BASE_URL}/", data=data)
    # Depending on your input validation, these characters might be rejected.
    # For security purposes, assume they are not allowed.
    assert response.status_code == 401

def test_invalid_email_format():
    """Test login with an invalid email format."""
    data = {"scu_email": "invalid_email_format", "scu_id": "1234567890"}
    response = requests.post(f"{BASE_URL}/", data=data)
    # The system should reject improperly formatted email addresses.
    assert response.status_code == 401
