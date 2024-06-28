from flask import Flask, request, jsonify
import pymysql
import etcd
import redis
import logging

app = Flask(__name__)

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
db_host = 'mysql'
db_user = 'user'
db_password = 'password'
db_name = 'reservationdb'
etcd_host = 'etcd'
redis_host = 'redis'
redis_port = 6379

# etcd Client
etcd_client = etcd.Client(host=etcd_host, port=2379)

# Redis Client
redis_client = redis.Redis(host=redis_host, port=redis_port, db=0)

# Database Connection
def get_db_connection():
    try:
        connection = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        logger.info("Successfully connected to the database")
        return connection
    except pymysql.MySQLError as e:
        logger.error(f"Error connecting to the database: {e}")
        return None

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/users', methods=['GET'])
def users():
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Failed to connect to the database"}), 500

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users")
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(result)
    except pymysql.MySQLError as e:
        logger.error(f"Error executing query: {e}")
        return jsonify({"error": f"Failed to execute query: {str(e)}"}), 500

@app.route('/etcd-test', methods=['GET'])
def etcd_test():
    try:
        etcd_client.write('/test_key', 'test_value')
        value = etcd_client.read('/test_key').value
        return value
    except Exception as e:
        logger.error(f"Error interacting with etcd: {e}")
        return jsonify({"error": "Failed to interact with etcd"}), 500

@app.route('/events', methods=['GET'])
def get_events():
    cached_events = redis_client.get('events')
    if cached_events:
        return jsonify(eval(cached_events)), 200
    
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Failed to connect to the database"}), 500

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM events")
        events = cursor.fetchall()
        redis_client.set('events', str(events), ex=300)  # Cache for 5 minutes
        return jsonify(events), 200
    except pymysql.MySQLError as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/reserve', methods=['POST'])
def reserve_tickets():
    event_id = request.json['event_id']
    user_id = request.json['user_id']
    num_tickets = request.json['num_tickets']

    lock_key = f"/events/{event_id}/lock"
    
    # Acquire Lock
    try:
        etcd_client.write(lock_key, "locked", ttl=60)
    except etcd.EtcdAlreadyExist:
        return jsonify({"error": "Another reservation is in progress"}), 409

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Failed to connect to the database"}), 500

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT available_tickets FROM events WHERE id=%s", (event_id,))
        result = cursor.fetchone()
        
        if result and result[0] >= num_tickets:
            cursor.execute("UPDATE events SET available_tickets=available_tickets-%s WHERE id=%s", (num_tickets, event_id))
            cursor.execute("INSERT INTO reservations (user_id, event_id, num_tickets) VALUES (%s, %s, %s)", (user_id, event_id, num_tickets))
            connection.commit()
            return jsonify({"message": "Reservation successful"}), 200
        else:
            return jsonify({"error": "Not enough tickets available"}), 400
    except pymysql.MySQLError as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()
        etcd_client.delete(lock_key)

@app.route('/reservations', methods=['GET'])
def get_reservations():
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Failed to connect to the database"}), 500

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM reservations")
        reservations = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(reservations), 200
    except pymysql.MySQLError as e:
        logger.error(f"Error executing query: {e}")
        return jsonify({"error": f"Failed to execute query: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
