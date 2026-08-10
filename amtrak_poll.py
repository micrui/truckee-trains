#!/usr/bin/env python3
"""Log the California Zephyr's scheduled vs actual times at Truckee.

Polls the community Amtraker API (api.amtraker.com, open JSON, attribution
requested) for trains 5 and 6, extracts the Truckee (TRU) stop from each
active trainset, and appends observations to data/amtrak/observations.jsonl.
Each trainset is keyed by its scheduled TRU date, so repeated polls update
toward the final actual times. render_status.py turns the log into the page.

Stdlib only. Run by GitHub Actions on a half-hourly cron.
"""
import json
import os
import urllib.request
import datetime

API = "https://api.amtraker.com/v3/trains/{}"
LOG = "data/amtrak/observations.jsonl"


def fetch(train):
    req = urllib.request.Request(
        API.format(train),
        headers={"User-Agent": "truckee-trains public record (github.com/micrui/truckee-trains)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def main():
    now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    obs = []
    for train in ("5", "6"):
        try:
            data = fetch(train)
        except Exception as e:
            print(f"train {train}: fetch failed: {e}")
            continue
        for t in data.get(train, []):
            for s in t.get("stations", []):
                if s.get("code") != "TRU":
                    continue
                sch = s.get("schDep") or s.get("schArr") or ""
                obs.append({
                    "polled": now,
                    "train": train,
                    "sch_date": sch[:10],
                    "schArr": s.get("schArr"),
                    "schDep": s.get("schDep"),
                    "arr": s.get("arr"),
                    "dep": s.get("dep"),
                    "status": s.get("status"),
                })
    if not obs:
        print("no observations this poll")
        return
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    with open(LOG, "a") as f:
        for o in obs:
            f.write(json.dumps(o) + "\n")
    print(f"logged {len(obs)} observations")


if __name__ == "__main__":
    main()
