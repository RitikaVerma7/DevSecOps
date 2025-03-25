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

def test_add_to_cart(client):
    """Test adding items to the cart."""
    with client.session_transaction() as sess:
        sess['user_id'] = 1
        sess['name'] = 'Ritika Verma'
    
    response = client.post('/add_to_cart', json={
        'item_id': 1,
        'name': 'Test Item',
        'price': 10.0
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Item added to cart'

def test_remove_from_cart(client):
    """Test removing items from the cart."""
    with client.session_transaction() as sess:
        sess['user_id'] = 1
        sess['name'] = 'Ritika Verma'
        sess['cart'] = [{'id': 1, 'name': 'Test Item', 'price': 10.0}]
    
    response = client.post('/remove_from_cart', json={'item_id': 1})
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Item removed from cart'

def test_cart_total_calculation(client):
    """Test cart total calculation."""
    with client.session_transaction() as sess:
        sess['user_id'] = 1
        sess['name'] = 'Ritika Verma'
        sess['cart'] = [
            {'id': 1, 'name': 'Item 1', 'price': 10.0},
            {'id': 2, 'name': 'Item 2', 'price': 15.0}
        ]
    
    response = client.get('/cart_total')
    assert response.status_code == 200
    data = response.get_json()
    assert data['total'] == 25.0

def test_place_order_success(client):
    """Test successful order placement using a valid location."""
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

def test_place_order_empty_cart(client):
    """Test order placement with an empty cart."""
    with client.session_transaction() as sess:
        sess['user_id'] = 1
        sess['name'] = 'Ritika Verma'
    
    response = client.post('/place_order', json={
        'cart_items': [],
        'location': 'Lucas Hall'
    })
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Cart is empty'

def test_place_order_invalid_location(client):
    """Test order placement with an invalid location."""
    with client.session_transaction() as sess:
        sess['user_id'] = 1
        sess['name'] = 'Ritika Verma'
    
    response = client.post('/place_order', json={
        'cart_items': [1, 2],
        'location': 'Invalid Location'
    })
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_estimated_delivery_time(client):
    """Test estimated delivery time calculation for an order with 5 items at 'Lucas Hall'."""
    with client.session_transaction() as sess:
        sess['user_id'] = 1
        sess['name'] = 'Ritika Verma'
    
    response = client.post('/place_order', json={
        'cart_items': [1, 2, 3, 4, 5],
        'location': 'Lucas Hall'
    })
    assert response.status_code == 200
    data = response.get_json()
    # Expected delivery time: base 10 + Lucas Hall time (7) + extra for 5 items (10) = 27 minutes.
    assert data['delivery_time'] == 27

if __name__ == '__main__':
    pytest.main()
