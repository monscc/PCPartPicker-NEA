from pcbuilder.compat import run_full_check


def make_parts():
    from pathlib import Path
    import json
    p = Path(__file__).resolve().parents[1] / "data" / "sample_parts.json"
    with open(p, "r", encoding="utf-8") as f:
        arr = json.load(f)
    d = {x["category"]: x for x in arr}
    return d


def test_full_check_ok():
    parts = make_parts()
    results = run_full_check(parts)
    # all checks should pass in sample data
    assert all(r[1] for r in results)


def test_psu_insufficient():
    parts = make_parts()
    # make GPU and CPU draw huge
    parts["GPU"]["attributes"]["power_draw"] = "600"
    parts["CPU"]["attributes"]["power_draw"] = "300"
    results = run_full_check(parts)
    # find psu result
    psu = [r for r in results if r[0] == "psu_wattage"][0]
    assert psu[1] is False
