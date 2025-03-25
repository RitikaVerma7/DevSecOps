import pytest
import sys
import os
from unittest.mock import patch, MagicMock

# Ensure Backend is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, get_db_connection, calculate_delivery_time

# Sample data from SQL inserts:
# INSERT INTO users (name, scu_email, scu_id) VALUES ('Mehak Agrawal', 'magrawal3@scu.edu', '1234567890');
# INSERT INTO users (name, scu_email, scu_id) VALUES ('Derleen Saini', 'dsaini@scu.edu', '1234567890');
# INSERT INTO users (name, scu_email, scu_id) VALUES ('Ritika Verma', 'rverma@scu.edu', '1234567890');
# INSERT INTO users (name, scu_email, scu_id) VALUES ('Tanya Jain', 'tjain2@scu.edu', '1234567890');

# Valid locations:
# "Lucas Hall", "scdi", "Alameda Hall", "Kenna Hall", "Finn Residence Hall"

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test if the home page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'SCU Food Delivery' in response.data

def test_login_page(client):
    """Test if the login page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Login' in response.data

def test_successful_login(client):
    """Test successful login using sample data (Ritika Verma)."""
    with patch('app.get_db_connection') as mock_db:
        # Using sample data: Ritika Verma, rverma@scu.edu, 1234567890
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = {'id': 1, 'name': 'Ritika Verma'}
        mock_db.return_value.cursor.return_value = mock_cursor
        
        response = client.post('/', data={
            'scu_email': 'rverma@scu.edu',
            'scu_id': '1234567890'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        # Expecting a welcome message that includes the user's name.
        assert b'Welcome, Ritika Verma' in response.data

def test_failed_login(client):
    """Test failed login with invalid credentials."""
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

def test_logout(client):
    """Test logout functionality."""
    with client.session_transaction() as sess:
        sess['user_id'] = 1
        sess['name'] = 'Ritika Verma'
    
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data

def test_index_page_authenticated(client):
    """Test index page when user is authenticated."""
    with client.session_transaction() as sess:
        sess['user_id'] = 1
        sess['name'] = 'Ritika Verma'
    
    with patch('app.get_db_connection') as mock_db:
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            {'id': 1, 'name': 'Item 1', 'price': 10.0, 'category': 'Breakfast'},
            {'id': 2, 'name': 'Item 2', 'price': 15.0, 'category': 'Lunch'}
        ]
        mock_db.return_value.cursor.return_value = mock_cursor
        
        response = client.get('/index')
        assert response.status_code == 200
        assert b'Item 1' in response.data
        assert b'Item 2' in response.data

def test_index_page_unauthenticated(client):
    """Test index page redirect when user is not authenticated."""
    response = client.get('/index', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data

def test_place_order(client):
    """Test place order functionality."""
    with client.session_transaction() as sess:
        sess['user_id'] = 1
        sess['name'] = 'Ritika Verma'
    
    with patch('app.get_db_connection') as mock_db:
        mock_cursor = MagicMock()
        mock_cursor.lastrowid = 1
        mock_db.return_value.cursor.return_value = mock_cursor
        
        response = client.post('/place_order', json={
            'cart_items': [1, 2],
            'location': 'Lucas Hall'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'order_id' in data
        assert 'delivery_time' in data

def test_calculate_delivery_time():
    """Test delivery time calculation for different scenarios."""
    # Using sample location "Lucas Hall"
    assert calculate_delivery_time('Lucas Hall', 2) == 17
    # Using sample location "scdi"
    assert calculate_delivery_time('scdi', 4) == 18
    # Using a location not in our predefined list defaults to 5 minutes added
    # Base preparation time = 10; default location time = 5; for 6 items: 10+5+10 = 25
    assert calculate_delivery_time('Unknown Location', 6) == 25

def test_get_location_image(client):
    """Test getting location image for 'Lucas Hall'."""
    response = client.get('/get_location_image/Lucas Hall')
    assert response.status_code == 200
    data = response.get_json()
    assert 'image_url' in data
    # Check that the returned image filename matches the mapping for Lucas Hall.
    assert 'lucas_hall.jpeg' in data['image_url']

if __name__ == '__main__':
    pytest.main()
