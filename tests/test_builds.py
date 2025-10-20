"""Tests for build save/load persistence"""
from pcbuilder.db import save_build, load_user_builds, load_build_by_id, DB_FILE, init_db
from pcbuilder.accounts import register
import sqlite3


def clear_test_builds():
    """Helper to clear test builds"""
    init_db()  # Ensure tables exist
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("DELETE FROM builds WHERE name LIKE 'test_build%'")
    conn.commit()
    conn.close()


def test_save_and_load_build():
    clear_test_builds()
    # Create a test user
    success, msg = register("testbuilduser1", "password123")
    # Extract user_id from message or login
    from pcbuilder.accounts import authenticate
    _, user_id, _ = authenticate("testbuilduser1", "password123")
    
    parts = {
        "CPU": {"id": "cpu-1", "name": "Test CPU", "category": "CPU", "price": 199.99, "attributes": {}},
        "GPU": None,
    }
    build_id = save_build(user_id, "test_build_1", parts)
    assert build_id > 0
    
    # Load builds for user
    builds = load_user_builds(user_id)
    assert len(builds) >= 1
    found = [b for b in builds if b["name"] == "test_build_1"]
    assert len(found) == 1
    assert found[0]["parts"]["CPU"]["name"] == "Test CPU"


def test_load_build_by_id():
    clear_test_builds()
    from pcbuilder.accounts import authenticate
    success, msg = register("testbuilduser2", "password123")
    _, user_id, _ = authenticate("testbuilduser2", "password123")
    
    parts = {"CPU": {"id": "cpu-2", "name": "CPU 2", "category": "CPU", "price": 150.0, "attributes": {}}}
    build_id = save_build(user_id, "test_build_2", parts)
    
    loaded = load_build_by_id(build_id)
    assert loaded is not None
    assert loaded["name"] == "test_build_2"
    assert loaded["parts"]["CPU"]["name"] == "CPU 2"


def test_load_nonexistent_build():
    loaded = load_build_by_id(999999)
    assert loaded is None
