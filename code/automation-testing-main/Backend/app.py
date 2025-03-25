from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import mysql.connector
import secrets
import os
import uuid

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# MySQL Configuration
app.config['MYSQL_HOST'] = os.getenv("MYSQL_HOST", "localhost")
app.config['MYSQL_USER'] = os.getenv("MYSQL_USER", "scu_food")
app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASSWORD", "")
app.config['MYSQL_DB'] = os.getenv("MYSQL_DB", "scu_food_delivery")

# Location Delivery Times (in minutes)
LOCATION_TIMES = {
    "Lucas Hall": 7,
    "scdi": 3,
    "Alameda Hall": 6,
    "Kenna Hall": 3,
    "Finn Residence Hall": 6
}

# Location Image Mapping
LOCATION_IMAGES = {
    "Lucas Hall": "lucas_hall.jpeg",
    "scdi": "scdi.jpeg",
    "Alameda Hall": "alameda_hall.jpeg",
    "Kenna Hall": "kenna_hall.jpeg",
    "Finn Residence Hall": "finn_hall.jpeg"
}

def get_db_connection():
    """Establish and return a database connection."""
    try:
        return mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB']
        )
    except mysql.connector.Error as err:
        print(f"Database Connection Error: {err}")
        return None

@app.route('/', methods=['GET', 'POST'])
def login():
    """Handles user login."""
    error = None
    if request.method == 'POST':
        scu_email = request.form['scu_email']
        scu_id = request.form['scu_id']

        conn = get_db_connection()
        if conn is None:
            return "Database connection failed", 500

        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE scu_email = %s AND scu_id = %s', (scu_email, scu_id))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['name'] = user['name']
            return redirect(url_for('index'))
        else:
            error = 'Invalid SCU Email or SCU ID'

    return render_template('login.html', error=error)

@app.route('/index')
def index():
    """Displays the main menu."""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    if conn is None:
        return "Database connection failed", 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM menu_items")
    menu_items = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('index.html', username=session['name'], menu_items=menu_items)

@app.route('/logout')
def logout():
    """Logs out the user and clears session."""
    session.clear()
    return redirect(url_for('login'))

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    """Adds an item to the user's session-based cart."""
    if 'cart' not in session:
        session['cart'] = []

    data = request.get_json()
    session['cart'].append({
        'id': data['item_id'],
        'name': data['name'],
        'price': float(data['price'])  # Ensure price is float
    })
    session.modified = True  # Ensure session updates
    return jsonify({"message": "Item added to cart"}), 200

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    """Removes an item from the cart."""
    if 'cart' in session:
        session['cart'] = [item for item in session['cart'] if item['id'] != request.json['item_id']]
        session.modified = True  # Ensure session updates
    return jsonify({"message": "Item removed from cart"}), 200

@app.route('/cart_total', methods=['GET'])
def cart_total():
    """Calculates the total cart price."""
    total = sum(item['price'] for item in session.get('cart', []))
    return jsonify({"total": total}), 200

@app.route('/place_order', methods=['POST'])
def place_order():
    """Handles order placement."""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized access'}), 401

    user_id = session['user_id']
    data = request.get_json()
    location = data['location']
    cart_items = data['cart_items']

    if location not in LOCATION_TIMES:
        return jsonify({'error': 'Invalid location'}), 400

    conn = get_db_connection()
    if conn is None:
        return "Database connection failed", 500

    cursor = conn.cursor(dictionary=True)

    try:
        # Calculate total price
        total_price = 0
        for item_id in cart_items:
            cursor.execute("SELECT price FROM menu_items WHERE id = %s", (item_id,))
            item = cursor.fetchone()
            if item:
                total_price += float(item['price'])

        # Generate unique order ID
        order_id = f"ORD-{uuid.uuid4().hex[:8]}-{user_id}"

        # Insert into orders table
        cursor.execute(
            "INSERT INTO orders (user_id, location, total_price, order_id) VALUES (%s, %s, %s, %s)",
            (user_id, location, total_price, order_id)
        )
        conn.commit()
        order_id_db = cursor.lastrowid

        # Insert into order_items table
        for item_id in cart_items:
            cursor.execute("INSERT INTO order_items (order_id, menu_item_id) VALUES (%s, %s)", (order_id_db, item_id))

        conn.commit()

        # Calculate and update estimated delivery time
        delivery_time = calculate_delivery_time(location, len(cart_items))
        cursor.execute("UPDATE orders SET estimated_delivery_time = %s WHERE id = %s", (delivery_time, order_id_db))
        conn.commit()

        return jsonify({'order_id': order_id, 'delivery_time': delivery_time})

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn.rollback()
        return jsonify({'error': 'Order placement failed.'}), 500

    finally:
        cursor.close()
        conn.close()

def calculate_delivery_time(location, num_items):
    """Calculates estimated delivery time based on location and number of items."""
    base_time = LOCATION_TIMES.get(location, 5) + 10  # Base 10 mins prep time
    if 3 <= num_items < 5:
        base_time += 5
    elif 5 <= num_items < 10:
        base_time += 10
    return base_time

@app.route('/get_location_image/<location>')
def get_location_image(location):
    """Returns the image URL for a given location."""
    filename = LOCATION_IMAGES.get(location, "default.jpeg")
    return jsonify({'image_url': url_for('static', filename=filename)})

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0', port=5000, debug=True)  # ✅ Fixed binding for Docker
