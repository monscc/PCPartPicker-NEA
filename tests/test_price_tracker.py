"""Tests for price tracker functionality"""
from pcbuilder.price_tracker import record_price, get_price_history
from datetime import datetime, timedelta


def test_record_and_get_price_history():
    part_id = "test-part-1"
    # Record some prices
    now = datetime.now()
    for i in range(5):
        timestamp = (now - timedelta(days=4-i)).isoformat()
        record_price(part_id, 100.0 + i * 10, timestamp)
    
    history = get_price_history(part_id, limit=10)
    assert len(history) >= 5
    # Should be ordered by timestamp descending
    assert history[0]["price"] >= history[-1]["price"]


def test_get_empty_price_history():
    history = get_price_history("nonexistent-part", limit=10)
    assert history == []
