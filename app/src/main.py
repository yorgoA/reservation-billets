from flask import Flask, jsonify
import pymysql
import etcd
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db_host = 'mysql'
db_user = 'user'
db_password = 'password'
db_name = 'reservationdb'

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

@app.route('/users')
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

# etcd client
etcd_client = etcd.Client(host='etcd', port=2379)

@app.route('/etcd-test')
def etcd_test():
    try:
        etcd_client.write('/test_key', 'test_value')
        value = etcd_client.read('/test_key').value
        return value
    except Exception as e:
        logger.error(f"Error interacting with etcd: {e}")
        return jsonify({"error": "Failed to interact with etcd"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
