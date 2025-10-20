"""Price tracker module for tracking part price history"""
from typing import List, Dict
import sqlite3
from datetime import datetime
from .db import DB_FILE, init_db


def init_price_tracker():
    """Initialize price history table"""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS price_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        part_id TEXT NOT NULL,
        price REAL NOT NULL,
        timestamp TEXT NOT NULL,
        FOREIGN KEY (part_id) REFERENCES parts(id)
    )
    """
    )
    conn.commit()
    conn.close()


def record_price(part_id: str, price: float, timestamp: str = None) -> int:
    """Record a price point for a part. Returns record ID."""
    init_price_tracker()
    if timestamp is None:
        timestamp = datetime.now().isoformat()
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO price_history (part_id, price, timestamp) VALUES (?, ?, ?)",
        (part_id, price, timestamp),
    )
    conn.commit()
    record_id = cur.lastrowid
    conn.close()
    return record_id


def get_price_history(part_id: str, limit: int = 100) -> List[Dict]:
    """Get price history for a part, ordered by timestamp descending."""
    init_price_tracker()
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(
        "SELECT id, price, timestamp FROM price_history WHERE part_id = ? ORDER BY timestamp DESC LIMIT ?",
        (part_id, limit),
    )
    rows = cur.fetchall()
    conn.close()
    return [{"id": r[0], "price": r[1], "timestamp": r[2]} for r in rows]


def plot_price_history(part_id: str, part_name: str = None):
    """Plot price history for a part using matplotlib (for embedding in Tkinter later)."""
    import matplotlib.pyplot as plt
    from datetime import datetime

    history = get_price_history(part_id, limit=100)
    if not history:
        print(f"No price history for part {part_id}")
        return None

    # Reverse to show oldest first
    history.reverse()
    dates = [datetime.fromisoformat(h["timestamp"]) for h in history]
    prices = [h["price"] for h in history]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(dates, prices, marker="o", linestyle="-", linewidth=2)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price ($)")
    ax.set_title(f"Price History: {part_name or part_id}")
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig
