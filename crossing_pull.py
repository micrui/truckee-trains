#!/usr/bin/env python3
"""Pull the Bridge Street crossing record from the FRA crossing inventory.

Queries the FRA's public GIS service for crossing 753183A, stores the
attributes as data/fra/crossing-753183A.json, and appends a dated diff to
data/fra/changes.jsonl when anything moved (train counts, devices, status).

Stdlib only. Run monthly by GitHub Actions.
"""
import json
import os
import urllib.parse
import urllib.request
import datetime

URL = ("https://fragis.fra.dot.gov/arcgis/rest/services/FRA/FRAGradeXing/MapServer/0/query?"
       + urllib.parse.urlencode({
           "where": "CROSSING='753183A'",
           "outFields": "*",
           "f": "json",
       }))
CUR = "data/fra/crossing-753183A.json"
CHANGES = "data/fra/changes.jsonl"


def main():
    req = urllib.request.Request(
        URL, headers={"User-Agent": "truckee-trains public record (github.com/micrui/truckee-trains)"})
    with urllib.request.urlopen(req, timeout=90) as r:
        data = json.load(r)
    feats = data.get("features", [])
    if not feats:
        print("no record returned; leaving stored copy untouched")
        return
    attrs = feats[0]["attributes"]
    os.makedirs(os.path.dirname(CUR), exist_ok=True)
    old = json.load(open(CUR)) if os.path.exists(CUR) else None
    if old is not None:
        diff = {k: [old.get(k), v] for k, v in attrs.items() if old.get(k) != v}
        if diff:
            with open(CHANGES, "a") as f:
                f.write(json.dumps({
                    "date": datetime.date.today().isoformat(),
                    "changed": diff}) + "\n")
            print(f"changes: {sorted(diff)}")
        else:
            print("no changes")
    with open(CUR, "w") as f:
        json.dump(attrs, f, indent=1, sort_keys=True)
    print("stored current record")


if __name__ == "__main__":
    main()
