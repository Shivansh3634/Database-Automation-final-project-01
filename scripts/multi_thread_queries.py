"""Concurrent workload driver for ClimateData in MySQL."""

import os
import random
import string
import time
from datetime import date, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import mysql.connector  # type: ignore
except Exception as exc:  
    raise SystemExit(
        "mysql-connector-python is not installed in this interpreter. "
        "Activate your venv and run: pip install mysql-connector-python"
    ) from exc

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "project_db")


def get_conn():
    """Open and return a fresh MySQL connection."""
    return mysql.connector.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )


def rand_location():
    """Return a short random location label."""
    return "Loc-" + "".join(random.choices(string.ascii_uppercase, k=4))


def insert_row():
    """Insert one randomized climate row."""
    conn = get_conn()
    try:
        cur = conn.cursor()
        loc = rand_location()
        d = date.today() - timedelta(days=random.randint(0, 30))
        temp = round(random.uniform(-10, 40), 1)
        precip = round(random.uniform(0, 20), 1)
        humidity = round(random.uniform(20, 95), 1)
        cur.execute(
            (
                "INSERT INTO ClimateData "
                "(location, record_date, temperature, precipitation, humidity) "
                "VALUES (%s, %s, %s, %s, %s)"
            ),
            (loc, d, temp, precip, humidity),
        )
        conn.commit()
        return f"INSERT OK -> {loc}"
    finally:
        conn.close()


def select_hot():
    """Select a few hot days for smoke verification."""
    conn = get_conn()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(
            (
                "SELECT location, record_date, temperature, humidity "
                "FROM ClimateData "
                "WHERE temperature > 20 "
                "ORDER BY record_date DESC "
                "LIMIT 5"
            )
        )
        rows = cur.fetchall()
        return f"SELECT HOT -> {len(rows)} rows"
    finally:
        conn.close()


def update_humidity_for_location(target_loc="Chester"):
    """Bump humidity slightly for a target location (bounded 0..100)."""
    conn = get_conn()
    try:
        cur = conn.cursor()
        bump = round(random.uniform(-3, 3), 1)
        cur.execute(
            (
                "UPDATE ClimateData "
                "SET humidity = LEAST(GREATEST(humidity + %s, 0), 100) "
                "WHERE location = %s"
            ),
            (bump, target_loc),
        )
        conn.commit()
        return f"UPDATE HUMIDITY -> {cur.rowcount} rows ({target_loc}, Δ={bump})"
    finally:
        conn.close()


def main():
    """Run a mixed concurrent workload."""
    start = time.time()
    tasks = []
    with ThreadPoolExecutor(max_workers=8) as ex:
        for _ in range(12):
            tasks.append(ex.submit(insert_row))
        for _ in range(6):
            tasks.append(ex.submit(select_hot))
        for loc in ["Chester", "Vancouver", "Montreal"]:
            tasks.append(ex.submit(update_humidity_for_location, loc))
        done = 0
        for fut in as_completed(tasks):
            print(fut.result())
            done += 1
    elapsed = time.time() - start
    print(f"Concurrent ops completed: {done} in {elapsed:.2f}s")


if __name__ == "__main__":
    print(f"Connecting to {DB_HOST}/{DB_NAME} as {DB_USER}")
    main()
