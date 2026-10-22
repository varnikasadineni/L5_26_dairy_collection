"""Milk collection ledger for a dairy cooperative.

Records each farmer's milk deliveries, totals a day's collection, finds the
top supplier, flags low-fat milk and prints collection slips.
"""

import hashlib
import sqlite3

LOW_FAT_THRESHOLD = 3.5


def create_db():
    """Create an in-memory database with the milk table and return it."""
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "CREATE TABLE milk (id INTEGER PRIMARY KEY, farmer TEXT, "
        "litres REAL, fat REAL, day TEXT)"
    )
    return conn


def record_milk(conn, farmer, litres, fat, day):
    """Store one milk delivery using a parameterised query."""
    conn.execute(
        "INSERT INTO milk (farmer, litres, fat, day) VALUES (?, ?, ?, ?)",
        (farmer, litres, fat, day),
    )
    conn.commit()


def farmer_token(farmer):
    """Return a SHA-256 token identifying the farmer."""
    return hashlib.sha256(farmer.encode()).hexdigest()


def daily_total(conn, day):
    """Return a formatted string with the total litres collected on a day."""
    rows = conn.execute(
        "SELECT litres FROM milk WHERE day = ?", (day,)
    ).fetchall()
    total = sum(r[0] for r in rows)
    return f"Total: {total:.1f} litres"


def top_farmer(conn):
    """Return the farmer who supplied the most litres, or None if no data."""
    rows = conn.execute(
        "SELECT farmer, SUM(litres) FROM milk GROUP BY farmer"
    ).fetchall()
    if not rows:
        return None
    top = max(rows, key=lambda r: r[1])
    return top[0]


def print_slip(farmer):
    """Print a collection slip for the farmer (no shell involved)."""
    print(f"printing slip for {farmer}")


def low_fat(conn):
    """Return farmers whose milk has missing or below-threshold fat."""
    rows = conn.execute("SELECT farmer, fat FROM milk").fetchall()
    return [f for f, fat in rows if fat is None or fat < LOW_FAT_THRESHOLD]


def main():
    """Run a short demonstration of the ledger."""
    conn = create_db()
    record_milk(conn, "Gopal", 12.5, 4.1, "Mon")
    record_milk(conn, "Lata", 20.0, 3.2, "Mon")
    print(daily_total(conn, "Mon"), top_farmer(conn), low_fat(conn))
    print_slip("Gopal")
    print(farmer_token("Lata"))
    conn.close()


if __name__ == "__main__":
    main()
