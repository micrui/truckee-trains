# CLAUDE.md — truckee-trains

Public record of the railroad through Truckee: the Union Pacific line over Donner Pass, its
history, governance (including train-horn rules and the federal Quiet Zone process), traffic,
and accident record. Site will publish via GitHub Pages from `/docs`.

## Voice and editorial rules (non-negotiable)

Same rules as truckee-flights and truckee-i80:

- Community member writing for neighbors; no side-taking, no outreach voice.
- No railroad jargon in prose (plain-English glosses or a link to the defining source).
- **Falsifiability is the admission criterion.** Unfalsifiable claims appear only as attributed
  statements. Political questions stay open; the site supplies the record.
- No self-referential neutrality statements, no apologetic framing, no editorializing labels.
- Every number traces to a linked source. Corrections are dated addenda, never silent.

## Planned structure (reference-first)

- **Governance page** — who controls the railroad: federal preemption (FRA/STB), the train-horn
  rule (49 CFR Part 222) and what a Quiet Zone actually requires, Union Pacific's ownership,
  what the Town of Truckee can and cannot decide. This is the centerpiece.
- **History page** — sourced timeline: Central Pacific construction and the summit tunnels,
  snowsheds, the 1925/1993 track changes, Amtrak's California Zephyr, the 2000s tunnel
  abandonment over the historic pass.
- **Safety page** — FRA crossing inventory and accident record for Truckee-area crossings.
- **Traveler links** — Amtrak schedules/status, UP public resources; links only, no dashboards.
- **Per-train log** — dark until home station hardware exists (see truckee-station);
  no public per-train data source matches the fidelity the other sites' logs have.

## Data sources to use

- FRA Office of Safety public databases: grade-crossing inventory, crossing accident/incident
  files, trespasser casualties (all public downloads; document provenance in DATA-SOURCES.md).
- FRA Quiet Zone rules and the horn-rule docket (49 CFR 222), plus Truckee's own municipal
  record on any Quiet Zone exploration.
- Amtrak public schedules; Union Pacific public network maps.

## Working discipline

- Stdlib-only Python; hand-written HTML in `/docs` on the shared CSS token set.
- Hold pushes until coherent; verify locally; single push.
- No credentials of any kind are needed for the sources above; keep it that way.
