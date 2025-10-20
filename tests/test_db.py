from pcbuilder.db import load_sample_parts, list_parts
from pathlib import Path


def test_list_parts(tmp_path):
    # load sample into a temp DB path
    data = Path(__file__).resolve().parents[1] / "data" / "sample_parts.json"
    # use default DB file but clear it by re-initializing
    load_sample_parts(data)
    parts = list_parts()
    assert len(parts) >= 6
