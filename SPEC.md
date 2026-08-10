# truckee-trains: site specification (draft for review)

Status: proposal. Nothing below is built. The source inventory behind every claim was
verified August 9-10, 2026; access mechanics are noted because they decide what the site
can actually deliver.

## What the site is for

The railroad is the oldest piece of infrastructure in town and the least legible. A resident
hears a horn at 3 a.m. and has no way to learn what it was; a visitor waits for a train at
Bridge Street with no idea whether it runs twice a day or twenty times. The site makes the
line legible the way truckee-flights made the airport legible: a morning glance answers what
passed in the night, how the passenger train is doing, and what is happening at the crossing;
the reference pages answer how it got here, who built it, who governs it, and what it carries.

Voice and editorial rules are in CLAUDE.md and are identical to the sibling sites:
falsifiability is the admission criterion, every number links to its source, no em-dashes,
corrections by dated addenda.

## The reader's morning (the product, in one view)

The landing page leads with an at-a-glance panel, rendered daily by automation:

- **Last night's trains.** Until home-station hardware exists (Phase 2), this is partial by
  necessity and says so: the two Amtrak trains are logged precisely; freight has no public
  schedule (a verified negative the page states plainly, with the federal crossing inventory's
  15 trains/day as the official baseline).
- **How the Zephyr is doing.** Yesterday's California Zephyr arrivals at Truckee, scheduled
  versus actual, plus trailing 30-day and year-to-date punctuality from the site's own
  accumulating log.
- **The crossing.** Current status of the Bridge Street quiet zone project, updated as the
  Town's records move.

## Pages

### 1. The crossing (the hero page)

Bridge Street, federal crossing ID 753183A, milepost 206.05 of the Roseville Subdivision.
The corrected headline claim, verified against a full milepost census of the subdivision's
109 crossings: **the only main-line at-grade crossing in Truckee proper, the only one for
about eight miles in either direction, and by far the busiest on the mountain** (10,679
vehicles a day versus 1,193 at Stampede Meadows Road and 30 at Old Donner Summit Road).
The original "only one for dozens of miles" phrasing fails checking and will not be used.

Content, all from the federal record:
- The inventory facts: two main tracks, gates, 8 day + 7 night trains, no whistle ban.
- The horn rule: 49 CFR 222 requires the horn 15-20 seconds before every public crossing,
  96-110 decibels, the long-long-short-long pattern. Every horn downtown is federal law
  executing, which is the fact that reframes every complaint about it.
- The accident record: four incidents at Bridge Street, 1979-1991, all vehicles, no injuries,
  all in the Southern Pacific era. **Zero reported incidents in the 35 years since.** Nearby
  crossings' records included for comparison.
- The quiet zone: the Town's Reimagine Bridge Street project explicitly aims to designate one
  ($6.325M project, design contract awarded January 2025). What a quiet zone legally requires,
  what it changes (the horn stops being routine; the gates carry the safety burden), and a
  status ledger the site keeps current from council records.

### 2. How the railroad got here (history)

The sourced timeline, wagon-road era to the present: construction 1863-68, the Summit Tunnel
opened November 30, 1867, the snowshed system, cab-forward steam from 1910, the 1925 second
track and Tunnel 41, the last steam over the pass in 1958, the 1993 abandonment of the
original 1868 summit track, the 1996 Union Pacific merger, and the 2009 tunnel-notching
project that cleared double-stack containers over Donner. Era-by-era traffic figures filled
from book sources in Phase 3 (Signor's *Donner Pass*, the historical society archives),
clearly marked where the record is book-derived.

### 3. Who built it, and who keeps it open (labor)

The page the history books wrote in the margins, from primary-anchored sources (Stanford's
Chinese Railroad Workers Project, the National Park Service, the local historical societies):

- Chinese workers were about ninety percent of the Central Pacific's workforce by 1867,
  roughly eleven thousand men, paid less than white workers and charged for their own board.
  They hand-drilled the Summit Tunnel through granite, worked through the 44-storm winter of
  1866-67, died in avalanches and blasting accidents in numbers no one recorded carefully
  (published estimates run from dozens to over a thousand; the page states the range and why
  it exists), and struck for equal wages in June 1867.
- Truckee then had one of the largest Chinatowns in the Sierra: 407 of the town's 1,467
  residents in 1870. The page records what the town did: the Trout Creek killings of 1876 and
  the acquittals that followed, the 1878 burning of Chinatown, and the 1886 boycott that
  expelled the community in about five weeks, celebrated statewide as "the Truckee Method."
  Context: the same years produced Rock Springs, Tacoma, Seattle, and the Chinese Exclusion
  Act. This happened across the West; Truckee's version has a name because it worked.
- The recent record too: Nevada County's 2023 landmark designation, the 2024 memorial plaque,
  and the December 2024 designation of Summit Camp as a National Historic Landmark.
- Who keeps it open now: Union Pacific's Roseville-based maintenance and snow-fighting
  operation, the flanger runs and rotary plows (the operational detail is enthusiast-sourced
  and labeled as such; no official workforce figures exist).

All of it in the site's flat, sourced register. The facts do not need help.

### 4. What the line carries (multimodal reference)

The comparison page, kept strictly factual:
- Roughly 15 freight trains a day over the pass (federal inventory figure) beside roughly
  6,500 trucks a day on I-80 at Truckee (Caltrans census), with the corridor cleared for
  double-stack containers since 2009.
- Amtrak ridership at Truckee, the full published series (FY2018-2024: 15,251 down to 5,759
  in the pandemic, back to 14,755; FY2025 pending verification).
- The planning record, including its silences, each a verified negative stated as fact: the
  State Rail Plan reaches Reno by bus; the Capitol Corridor's Reno extension has not advanced;
  no truck-to-rail diversion study exists for this corridor; no modern electrification
  proposal exists for Donner. What has been studied and what has never been studied are both
  facts about the corridor.
- Any train-equals-N-trucks equivalence is published only with a citable source; none has
  been verified yet, so none appears until one is.

### 5. Watching the trains (links)

Verified live resources only: the Truckee Donner Railroad Society and its caboose train-cam,
the downtown webcam that covers the crossing, the historical societies and their newsletter
archives, the Pacific Southwest Railway Historical Society's Donner timeline, the historic
timetable archive, the railroad-radio feed (linked, not embedded, per its terms), and the
California State Railroad Museum's library. Dead or paywalled resources stay off the page.

## Data collection and automation

Same architecture as truckee-i80: stdlib Python, GitHub Actions, everything accumulates in
the open, provenance in DATA-SOURCES.md.

- **amtrak_poll.py** (Phase 1): polls a public Amtrak status API for the Zephyr at Truckee
  around the two daily arrival windows, logs scheduled versus actual to `data/amtrak/`, and
  renders the punctuality panel. Primary source: the community Amtraker API (open JSON, with
  attribution); fallback: the government-hosted ArcGIS mirror (15-minute updates). No
  official Amtrak API exists; the page says so.
- **crossing_pull.py** (Phase 1): monthly pull of the Bridge Street record from the federal
  crossing-inventory GIS API into `data/fra/`, so changes to the official trains/day count or
  crossing configuration become a logged diff.
- **Historical punctuality backfill**: a community archive holds Truckee records back to
  January 2008. It has no export interface and is one person's labor of love; the site will
  ask its maintainer before using it, and the ask is a step in Phase 1, not an assumption.
- **Quiet zone ledger**: council records checked monthly by hand (the meeting portal is
  searchable; scraping it is not worth the brittleness), changes logged with dates.
- **Phase 2, the per-train log**: the home station's calibrated microphone (see
  truckee-station) turns the site into the train equivalent of the flight log: timestamp,
  direction, duration, peak decibels, and horn signature for every passage, published as
  numbers only under the station's metadata-only guarantee. This is what makes "what just
  honked" answerable at a glance, including for freight, and it measures the crossing's
  soundscape before and after any quiet zone takes effect, which no one else will have.
- **Phase 3, the deep record**: era tonnage and train counts from book and archive sources,
  worked into the history page with page-level citations.

## Phases and acceptance

- **Phase 1 (buildable now):** the five pages above, Amtrak poller live, FRA data pulled,
  landing panel rendering daily. Acceptance: a reader can wake up, see yesterday's Zephyr
  performance and the official picture of the crossing, and every claim on every page
  survives the hostile-vet pass that the airport site got.
- **Phase 2 (hardware-gated):** per-train event log from the station microphone.
- **Phase 3 (research-gated):** historical traffic series; multimodal page enriched if any
  citable study or equivalence surfaces.

## Held claims (known, not yet publishable)

- Construction death tolls: publish as a contested range with the reasons, never a number.
- "15 to 18 trains a day" (2009 press quote): the 15/day federal figure is the citable one.
- Quiet zone component cost: not yet public; ledger tracks it.
- The 2009 double-stack project cost (~$25-30M circulates): not in the primary source; held.
- One 1876 date discrepancy in the Trout Creek record: verify before the labor page ships.

## Open questions for review

1. Scope check: five pages plus the daily panel; anything missing, anything that should wait?
2. The labor page as its own page (recommended) versus folded into history?
3. Comfort level with the archive-permission email in Phase 1?
4. The radio feed: link only (recommended) versus any embedded audio?
