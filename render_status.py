#!/usr/bin/env python3
"""Render docs/status.html from the accumulated Zephyr observations.

For each (train, scheduled date) the latest poll wins. Delay is measured on
departure when present, else arrival. Stops are grouped by day, newest first;
today's group (Pacific time at render) is labeled and tinted. Stdlib only; run
after each poll.
"""
import json
import os
import datetime
from zoneinfo import ZoneInfo

LOG = "data/amtrak/observations.jsonl"
OUT = "docs/status.html"
PACIFIC = ZoneInfo("America/Los_Angeles")
LATE_CAP, EARLY_CAP = 90, 34   # bar lengths in px (1 px per minute); the number stays exact


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
    return d.strftime("%H:%M") if d else ""


def signed(d):
    return "0" if d == 0 else (f"+{d}" if d > 0 else str(d))


def day_heading(ds, today):
    d = datetime.date.fromisoformat(ds)
    label = d.strftime("%A, %B ") + str(d.day)
    return f"Today ({label})" if d == today else label


def delay_cell(d):
    """Bars grow from a shared zero line: late to the right, early to the left."""
    left, right = "", ""
    if d > 0:
        right = f'<span class="bar late" style="width:{min(LATE_CAP, d)}px"></span><span>{signed(d)}</span>'
    elif d < 0:
        left = f'<span>{signed(d)}</span><span class="bar early" style="width:{min(EARLY_CAP, -d)}px"></span>'
    else:
        right = "<span>0</span>"
    return f'<span class="dz"><span class="dl">{left}</span><span class="zero"></span><span class="dr">{right}</span></span>'


def render():
    rows = load()
    today = datetime.datetime.now(PACIFIC).date()
    recent = [o for o in rows if o["sch_date"]][-14:]
    done = [(o, delay_min(o)) for o in rows if o.get("status") == "Departed"]
    done = [(o, d) for o, d in done if d is not None]
    stats = ""
    if done:
        within15 = sum(1 for _, d in done if abs(d) <= 15)
        median = sorted(d for _, d in done)[len(done) // 2]
        first = datetime.date.fromisoformat(done[0][0]["sch_date"])
        stats = (f'<div class="figs">'
                 f'<span><strong>{len(done)}</strong>stops logged since {first.strftime("%b")} {first.day}</span>'
                 f'<span><strong>{within15}</strong>left within 15 minutes of schedule</span>'
                 f'<span><strong>{signed(median)}</strong>median minutes off scheduled departure</span>'
                 f'</div>')

    body = []
    last_date = None
    for o in reversed(recent):
        is_today = datetime.date.fromisoformat(o["sch_date"]) == today
        tcls = " today" if is_today else ""
        if o["sch_date"] != last_date:
            last_date = o["sch_date"]
            body.append(f'<tr class="day{tcls}"><td colspan=5>{day_heading(o["sch_date"], today)}</td></tr>')
        train = "westbound (5)" if o["train"] == "5" else "eastbound (6)"
        sched = fmt_t(o.get("schDep") or o.get("schArr"))
        actual = fmt_t(o.get("dep") or o.get("arr"))
        d = delay_min(o)
        if o.get("status") == "Departed" and d is not None:
            cells = f'<td class=num>{actual}</td><td class=num>{delay_cell(d)}</td><td class=st>departed</td>'
        else:
            cells = f'<td class="num exp">expected {actual}</td><td class="num exp">not yet</td><td class=st>en route</td>'
        body.append(f'<tr class="stop{tcls}"><td class=tr>{train}</td><td class=num>{sched}</td>{cells}</tr>')
    body = "".join(body)

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
    --early: #eb6834; --today: rgba(42,120,214,0.07);
  }}
  @media (prefers-color-scheme: dark) {{
    :root:where(:not([data-theme="light"])) {{
      color-scheme: dark;
      --page: #0c0e11; --surface: #1a1a19; --ink: #ffffff; --ink-2: #c3c2b7;
      --muted: #898781; --grid: #2c2c2a; --axis: #383835; --border: rgba(255,255,255,0.10); --accent: #3987e5;
      --early: #d95926; --today: rgba(57,135,229,0.12);
    }}
  }}
  :root[data-theme="dark"] {{
    color-scheme: dark;
    --page: #0c0e11; --surface: #1a1a19; --ink: #ffffff; --ink-2: #c3c2b7;
    --muted: #898781; --grid: #2c2c2a; --axis: #383835; --border: rgba(255,255,255,0.10); --accent: #3987e5;
    --early: #d95926; --today: rgba(57,135,229,0.12);
  }}
  :root[data-theme="light"] {{
    color-scheme: light;
    --page: #f6f7f9; --surface: #fcfcfb; --ink: #0b0b0b; --ink-2: #52514e;
    --muted: #898781; --grid: #e1e0d9; --axis: #c3c2b7; --border: rgba(11,11,11,0.10); --accent: #2a78d6;
    --early: #eb6834; --today: rgba(42,120,214,0.07);
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
  .figs {{ display: flex; gap: 28px; flex-wrap: wrap; padding: 12px 0 14px; margin: 24px 0 6px; font-size: 13.5px; color: var(--ink-2);
    border-top: 1px solid var(--axis); border-bottom: 1px solid var(--grid); }}
  .figs strong {{ color: var(--ink); font-size: 20px; font-weight: 650; margin-right: 6px; }}
  table {{ border-collapse: collapse; width: 100%; font-size: 13.5px; margin: 10px 0 6px; }}
  th {{ text-align: left; font-size: 11px; letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted);
    font-weight: 600; padding: 6px 12px 6px 0; border-bottom: 1px solid var(--axis); }}
  td {{ padding: 6px 12px 6px 0; border-bottom: 1px solid var(--grid); font-variant-numeric: tabular-nums; }}
  td.num {{ font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace; white-space: nowrap; }}
  td.exp {{ color: var(--muted); font-style: italic; }}
  td.st {{ color: var(--ink-2); }}
  td.tr {{ padding-left: 12px; width: 120px; }}
  tr.day td {{ padding-top: 14px; border-bottom: 0; font-weight: 650; font-size: 13px; color: var(--ink); }}
  tr.today td {{ background: var(--today); }}
  tr.day.today td {{ padding-top: 10px; }}
  .dz {{ display: inline-flex; align-items: center; white-space: nowrap; }}
  .dl {{ display: inline-flex; justify-content: flex-end; align-items: center; gap: 6px; width: 64px; }}
  .dr {{ display: inline-flex; align-items: center; gap: 6px; width: 130px; }}
  .zero {{ display: inline-block; width: 1px; height: 14px; background: var(--axis); }}
  .bar {{ display: inline-block; height: 8px; }}
  .bar.late {{ background: var(--accent); border-radius: 0 4px 4px 0; }}
  .bar.early {{ background: var(--early); border-radius: 4px 0 0 4px; }}
  .key {{ font-size: 12px; color: var(--muted); margin: 8px 0 0; display: flex; gap: 16px; flex-wrap: wrap; align-items: center; max-width: none; }}
  .key .sw {{ display: inline-block; width: 18px; height: 8px; border-radius: 4px; vertical-align: middle; margin-right: 6px; }}
  .src {{ font-size: 12px; color: var(--muted); margin: 12px 0 0; max-width: 70ch; }}
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
  <p><strong>Where is it right now:</strong> live position of
  <a href="https://railrat.net/trains/5/">train 5 westbound</a> and
  <a href="https://railrat.net/trains/6/">train 6 eastbound</a>, or the
  <a href="https://asm.transitdocs.com/">national live map</a>.</p>
  <p><strong>Tickets:</strong> book at
  <a href="https://www.amtrak.com/home">amtrak.com</a> and enter Truckee, CA (TRU) as your
  station; Amtrak's booking page does not accept a prefilled link.</p>
  {stats}
  <div class="table-scroll"><table>
    <thead><tr><th>Train</th><th>Scheduled departure</th><th>Left Truckee</th><th>Minutes off scheduled departure</th><th>Status</th></tr></thead>
    <tbody>{body if body else '<tr><td colspan=5>Collection just began; the first stops will appear within a day.</td></tr>'}</tbody>
  </table></div>
  <p class="key"><span>Bars grow from the zero line:</span>
    <span><span class="sw" style="background:var(--early)"></span>early, to the left</span>
    <span><span class="sw" style="background:var(--accent)"></span>late, to the right</span>
    <span>Both count against the schedule. Bars cap at {EARLY_CAP} early and {LATE_CAP} late; the number is exact.
    Times are departures from Truckee; Amtrak schedules the arrival and the departure here at the same minute.
    If Amtrak reports no departure time for a stop, the arrival is compared with the scheduled arrival instead.
    Rows marked en route show Amtrak's current estimate, not a departure.</span></p>
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
