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

def test_login_form_rendering(client):
    """Test if login form renders correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'SCU Email:' in response.data
    assert b'SCU Student ID:' in response.data

def test_login_success(client):
    """Test successful login using sample data (Ritika Verma)."""
    with patch('app.get_db_connection') as mock_db:
        mock_cursor = MagicMock()
        # Using sample data for Ritika Verma:
        mock_cursor.fetchone.return_value = {'id': 1, 'name': 'Ritika Verma'}
        mock_db.return_value.cursor.return_value = mock_cursor
        
        response = client.post('/', data={
            'scu_email': 'rverma@scu.edu',
            'scu_id': '1234567890'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Welcome, Ritika Verma' in response.data

def test_login_failure_invalid_credentials(client):
    """Test login failure due to invalid credentials."""
    with patch('app.get_db_connection') as mock_db:
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_db.return_value.cursor.return_value = mock_cursor
        
        response = client.post('/', data={
            'scu_email': 'wrong@scu.edu',
            'scu_id': '0987654321'
        })
        
        assert response.status_code == 200
        assert b'Invalid SCU Email or SCU ID' in response.data

def test_login_form_validation(client):
    """Test login form validation with improperly formatted data."""
    with patch('app.get_db_connection') as mock_db:
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_db.return_value.cursor.return_value = mock_cursor
    response = client.post('/', data={
        'scu_email': 'invalid_email',
        'scu_id': '123'  # Invalid ID format (should be 10 digits)
    })
    assert response.status_code == 200
    # Expected validation message from the form (adjust if your implementation varies)
    assert b'Enter a valid 10-digit SCU Student ID' in response.data

def test_session_creation(client):
    """Test session creation after successful login using sample data (Ritika Verma)."""
    with patch('app.get_db_connection') as mock_db:
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = {'id': 1, 'name': 'Ritika Verma'}
        mock_db.return_value.cursor.return_value = mock_cursor
        
        client.post('/', data={
            'scu_email': 'rverma@scu.edu',
            'scu_id': '1234567890'
        })
        
        with client.session_transaction() as sess:
            assert sess['user_id'] == 1
            assert sess['name'] == 'Ritika Verma'

def test_redirect_after_login(client):
    """Test redirection after successful login using sample data (Ritika Verma)."""
    with patch('app.get_db_connection') as mock_db:
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = {'id': 1, 'name': 'Ritika Verma'}
        mock_db.return_value.cursor.return_value = mock_cursor
        
        response = client.post('/', data={
            'scu_email': 'rverma@scu.edu',
            'scu_id': '1234567890'
        }, follow_redirects=True)
        
        # Verify that after successful login, the user is redirected to the index page.
        assert response.request.path == '/index'

if __name__ == '__main__':
    pytest.main()
