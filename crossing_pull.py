#!/usr/bin/env python3
"""Pull the Bridge Street crossing record from the FRA crossing inventory.

Queries the FRA's public GIS service for crossing 753183A, stores the
attributes as data/fra/crossing-753183A.json, and appends a dated diff to
data/fra/changes.jsonl when anything moved (train counts, devices, status).

If the FRA server is down (it serves runtime errors from time to time), the
run falls back to the NTAD mirror of the same inventory on ArcGIS Online and
stores that snapshot beside the primary; the change log stays tied to the
FRA schema only. Both failing is a hard failure so the cron shows red.

Stdlib only. Run monthly by GitHub Actions.
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request
import datetime

UA = {"User-Agent": "truckee-trains public record (github.com/micrui/truckee-trains)"}
URL = ("https://fragis.fra.dot.gov/arcgis/rest/services/FRA/FRAGradeXing/MapServer/0/query?"
       + urllib.parse.urlencode({
           "where": "CROSSING='753183A'",
           "outFields": "*",
           "f": "json",
       }))
NTAD_URL = ("https://services.arcgis.com/xOi1kZaI0eWDREZv/arcgis/rest/services/"
            "NTAD_Railroad_Grade_Crossings/FeatureServer/0/query?"
            + urllib.parse.urlencode({
                "where": "CrossingID='753183A'",
                "outFields": "*",
                "f": "json",
            }))
CUR = "data/fra/crossing-753183A.json"
NTAD = "data/fra/crossing-753183A-ntad.json"
CHANGES = "data/fra/changes.jsonl"


def query(url, tries=3):
    last = None
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=90) as r:
                data = json.load(r)
            if "error" in data:
                raise RuntimeError(data["error"])
            return data.get("features", [])
        except Exception as e:
            last = e
            print(f"attempt {attempt + 1}/{tries} failed: {e}", file=sys.stderr)
            if attempt < tries - 1:
                time.sleep(30)
    raise last


def main():
    os.makedirs(os.path.dirname(CUR), exist_ok=True)
    try:
        feats = query(URL)
    except Exception as e:
        print(f"FRA server unavailable ({e}); falling back to the NTAD mirror",
              file=sys.stderr)
        feats = query(NTAD_URL)
        if not feats:
            sys.exit("NTAD mirror returned no record either")
        attrs = feats[0]["attributes"]
        attrs["_pulled"] = datetime.date.today().isoformat()
        with open(NTAD, "w") as f:
            json.dump(attrs, f, indent=1, sort_keys=True)
        print("stored NTAD snapshot; FRA record and change log untouched")
        return
    if not feats:
        print("no record returned; leaving stored copy untouched")
        return
    attrs = feats[0]["attributes"]
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
