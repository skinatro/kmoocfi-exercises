"""
Count the number of the GET requests to the app and store it a file
"""
import os
from flask import Flask, request, make_response
import psycopg2

app = Flask(__name__)

class Counter:
    """
    Class to increment the number of visits to the site and save to file
    """
    def __init__(self):
        self.value = 0
        self.conn = psycopg2.connect(
            host=os.environ.get("DB_HOST", "localhost"),
            port=5432,
            dbname=os.environ.get("POSTGRES_DB"),
            user=os.environ.get("POSTGRES_USER"),
            password=os.environ.get("POSTGRES_PASSWORD")
        )
        self.conn.autocommit = True

        with self.conn.cursor() as cur:
            # Ensure table exists
            cur.execute("""
                CREATE TABLE IF NOT EXISTS pingpong (
                    id SERIAL PRIMARY KEY,
                    counter INTEGER NOT NULL
                );
            """)
            # Ensure one row exists
            cur.execute("SELECT COUNT(*) FROM pingpong;")
            if cur.fetchone()[0] == 0:
                cur.execute("INSERT INTO pingpong (counter) VALUES (0);")

            # Load existing counter value
            cur.execute("SELECT counter FROM pingpong WHERE id = 1;")
            result = cur.fetchone()
            self.value = result[0] if result else 0

    def increment(self):
        """
        Method to increment the number of visits to the site and save to file
        """
        # file_path = "/tmp/kube/pongs.txt"
        self.value += 1
        with self.conn.cursor() as cur:
            cur.execute("UPDATE pingpong SET counter = %s WHERE id = 1;", (self.value,))
        # with open(file_path, 'w') as file:
        #     file.write("ping pongs "+str(self.value) + '\n')
        return self.value

counter = Counter()

@app.route("/pings")
def ping():
    """
    Shows the number of pings
    """
    return str(counter.increment())

@app.route('/')
def pong():
    """
    Call the increment function to increment and log to file upon GET request
    """
    if request.method == 'GET':
        return f"Ping / Pong: {counter.increment()}"

@app.route('/healthz')
def healthz():
    """
    Health check endpoint.
    Returns 200 OK if the app and DB connection are healthy.
    """
    try:
        with counter.conn.cursor() as cur:
            cur.execute("SELECT 1;")    
            _ = cur.fetchone()
        return "OK", 200
    except Exception as e:
        app.logger.error(f"Health check failed: {e}")
        return "Database connection error", 500


if __name__ == '__main__':
    PORT = os.environ.get("PORT")
    app.run(host="0.0.0.0", port=int(PORT), debug=True)