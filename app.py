import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from flask import Flask, request
from werkzeug.middleware.proxy_fix import ProxyFix

load_dotenv()  # loads variables from .env file into environment

app = Flask(__name__)
app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)
url = os.environ.get("DATABASE_URL")  # gets variables from environment
connection = psycopg2.connect(url)

@app.get("/api/statistiques/<string:table>")
def getStatistiques(table):
    STATS = (f"select * from pastell.{table};")
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(STATS)
            results = cursor.fetchall();
    return results, 200

if __name__ == "__main__":
    app.run(host='127.0.0.1')
