#!/usr/bin/env python3
"""Render docs/status.html from the accumulated Zephyr observations.

For each (train, scheduled date) the latest poll wins. Delay is measured on
departure when present, else arrival. Stdlib only; run after each poll.
"""
import json
import os
import datetime

LOG = "data/amtrak/observations.jsonl"
OUT = "docs/status.html"


def parse(ts):
    if not ts:
        return None
    try:
        return datetime.datetime.fromisoformat(ts)
    except ValueError:
        return None


def load():
    best = {}
    if os.path.exists(LOG):
        with open(LOG) as f:
            for line in f:
                o = json.loads(line)
                if o.get("sch_date"):
                    best[(o["train"], o["sch_date"])] = o
    return sorted(best.values(), key=lambda o: (o["sch_date"], o["train"]))


def delay_min(o):
    sch, act = parse(o.get("schDep")), parse(o.get("dep"))
    if not act:
        sch, act = parse(o.get("schArr")), parse(o.get("arr"))
    if sch and act:
        return round((act - sch).total_seconds() / 60)
    return None


def fmt_t(ts):
    d = parse(ts)
    return d.strftime("%H:%M") if d else "–"


def render():
    rows = load()
    recent = [o for o in rows if o["sch_date"]][-14:]
    done = [(o, delay_min(o)) for o in rows if o.get("status") == "Departed"]
    done = [(o, d) for o, d in done if d is not None]
    stats = ""
    if done:
        within15 = sum(1 for _, d in done if d <= 15)
        stats = (f"<p>Across the {len(done)} stops logged since this record began, "
                 f"{within15} departed Truckee within 15 minutes of schedule. "
                 f"Median delay: {sorted(d for _, d in done)[len(done)//2]} minutes.</p>")

    body = "".join(
        f"<tr><td class=num>{o['sch_date']}</td>"
        f"<td>{'westbound (5)' if o['train']=='5' else 'eastbound (6)'}</td>"
        f"<td class=num>{fmt_t(o.get('schDep') or o.get('schArr'))}</td>"
        f"<td class=num>{fmt_t(o.get('dep') or o.get('arr'))}</td>"
        f"<td class=num>{('+' if (delay_min(o) or 0) > 0 else '')}{delay_min(o) if delay_min(o) is not None else '–'}</td>"
        f"<td>{o.get('status') or ''}</td></tr>"
        for o in reversed(recent))

    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    html = f"""<meta charset="utf-8">
<title>Truckee train schedule and status: the California Zephyr at Truckee</title>
<meta name="description" content="Is the train on time in Truckee? Scheduled versus actual California Zephyr times at the Truckee Amtrak station, logged half-hourly, with the accumulating punctuality record.">
<link rel="canonical" href="https://micrui.github.io/truckee-trains/status.html">
<meta property="og:title" content="Truckee train schedule and status: the California Zephyr at Truckee">
<meta property="og:description" content="Scheduled versus actual California Zephyr times at Truckee, logged half-hourly.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://micrui.github.io/truckee-trains/status.html">
<meta name="twitter:card" content="summary">
<style>
  :root {{
    color-scheme: light;
    --page: #f6f7f9; --surface: #fcfcfb; --ink: #0b0b0b; --ink-2: #52514e;
    --muted: #898781; --grid: #e1e0d9; --axis: #c3c2b7; --border: rgba(11,11,11,0.10); --accent: #2a78d6;
  }}
  @media (prefers-color-scheme: dark) {{
    :root:where(:not([data-theme="light"])) {{
      color-scheme: dark;
      --page: #0c0e11; --surface: #1a1a19; --ink: #ffffff; --ink-2: #c3c2b7;
      --muted: #898781; --grid: #2c2c2a; --axis: #383835; --border: rgba(255,255,255,0.10); --accent: #3987e5;
    }}
  }}
  :root[data-theme="dark"] {{
    color-scheme: dark;
    --page: #0c0e11; --surface: #1a1a19; --ink: #ffffff; --ink-2: #c3c2b7;
    --muted: #898781; --grid: #2c2c2a; --axis: #383835; --border: rgba(255,255,255,0.10); --accent: #3987e5;
  }}
  :root[data-theme="light"] {{
    color-scheme: light;
    --page: #f6f7f9; --surface: #fcfcfb; --ink: #0b0b0b; --ink-2: #52514e;
    --muted: #898781; --grid: #e1e0d9; --axis: #c3c2b7; --border: rgba(11,11,11,0.10); --accent: #2a78d6;
  }}
  body {{ background: var(--page); color: var(--ink); font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
    line-height: 1.6; margin: 0; padding: 48px 20px 72px; }}
  .wrap {{ max-width: 800px; margin: 0 auto; }}
  .nav {{ font-size: 12.5px; margin: 0 0 26px; color: var(--muted);
    font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace; }}
  .nav a {{ color: var(--ink-2); text-decoration: none; margin-right: 14px; white-space: nowrap; }}
  .nav a:hover {{ color: var(--accent); }}
  .nav a.here {{ color: var(--ink); font-weight: 650; }}
  .eyebrow {{ font-size: 12px; letter-spacing: 0.14em; text-transform: uppercase; color: var(--muted);
    margin: 0 0 10px; font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace; }}
  .eyebrow a {{ color: inherit; }}
  h1 {{ font-size: clamp(26px, 4vw, 38px); font-weight: 700; letter-spacing: -0.02em; margin: 0 0 14px; }}
  .standfirst {{ font-size: 15.5px; color: var(--ink-2); max-width: 66ch; margin: 0 0 30px; }}
  p {{ max-width: 70ch; font-size: 15px; margin: 0 0 12px; }}
  table {{ border-collapse: collapse; width: 100%; font-size: 13.5px; margin: 10px 0 6px; }}
  th {{ text-align: left; font-size: 11px; letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted);
    font-weight: 600; padding: 6px 12px 6px 0; border-bottom: 1px solid var(--axis); }}
  td {{ padding: 6px 12px 6px 0; border-bottom: 1px solid var(--grid); font-variant-numeric: tabular-nums; }}
  td.num {{ font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace; white-space: nowrap; }}
  .src {{ font-size: 12px; color: var(--muted); margin: 4px 0 0; max-width: 70ch; }}
  .src a {{ color: var(--muted); }}
  .table-scroll {{ overflow-x: auto; }}
  a {{ color: var(--accent); }}
  .foot {{ margin-top: 44px; padding-top: 16px; border-top: 1px solid var(--grid); color: var(--muted); font-size: 12.5px; max-width: 74ch; }}
</style>
<div class="wrap">
  <nav class="nav"><a href="index.html">home</a><a href="status.html" class="here">the Zephyr</a><a href="crossing.html">the crossing</a><a href="history.html">history</a><a href="built.html">labor</a><a href="carries.html">what it carries</a><a href="walk.html">train walk</a><a href="bigboy.html">Big Boy</a><a href="links.html">watching</a></nav>
  <p class="eyebrow"><a href="./">truckee-trains</a> · status</p>
  <h1>The Zephyr at Truckee</h1>
  <p class="standfirst">
    Amtrak's California Zephyr stops in Truckee twice a day: train 5 westbound toward the Bay,
    train 6 eastbound toward Chicago. This page logs scheduled against actual times at the
    Truckee station and accumulates the punctuality record. It updates through the day and
    settles by the following morning. Last rendered {now}.
  </p>
  <p><strong>Tickets:</strong> book from Truckee on
  <a href="https://www.amtrak.com/stations/tru">Amtrak's Truckee station page</a> (code TRU);
  the full route is the <a href="https://www.amtrak.com/california-zephyr-train">California
  Zephyr</a>.</p>
  {stats}
  <div class="table-scroll"><table>
    <thead><tr><th>Date</th><th>Train</th><th>Scheduled</th><th>Actual</th><th>Delay (min)</th><th>Status</th></tr></thead>
    <tbody>{body if body else '<tr><td colspan=6>Collection just began; the first stops will appear within a day.</td></tr>'}</tbody>
  </table></div>
  <p class="src">Times are local (Pacific). Data from the community
  <a href="https://github.com/piemadd/amtrak">Amtraker</a> mirror of Amtrak's live map, polled
  on a half-hour cadence; Amtrak publishes no official interface. The raw observation log is
  in <a href="https://github.com/micrui/truckee-trains/tree/main/data/amtrak">the repository</a>.
  Freight has no public schedule of any kind; the federal crossing inventory's figure for this
  line is 15 trains a day.</p>
  <div class="foot">
    <p>Corrections welcome via <a href="https://github.com/micrui/truckee-trains">GitHub</a>.</p>
  </div>
</div>
"""
    os.makedirs("docs", exist_ok=True)
    with open(OUT, "w") as f:
        f.write(html)
    print(f"wrote {OUT}: {len(recent)} recent stops")


if __name__ == "__main__":
    render()
