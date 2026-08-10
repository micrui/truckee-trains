# truckee-trains

A public record of the railroad through Truckee, California: the Union Pacific main line over
Donner Pass. History, governance (including the federal rules that decide where train horns
sound), traffic, and the official accident record, every claim traceable to its source.

Sibling projects: [truckee-flights](https://github.com/micrui/truckee-flights) (the airport),
[truckee-i80](https://github.com/micrui/truckee-i80) (the freeway).

**Site: https://micrui.github.io/truckee-trains**

- The Zephyr at Truckee: scheduled versus actual times, logged half-hourly, accumulating.
- The Bridge Street crossing: the federal record, the horn rule, and the Town's quiet
  zone project.
- History, the labor record (who built it and what the town did afterward), what the
  line carries, and verified links for watching the trains.

Automation: `amtrak_poll.py` (half-hourly), `crossing_pull.py` (monthly),
`render_status.py`. Stdlib-only Python; provenance in `DATA-SOURCES.md`.

Maintained by a Truckee resident. Not affiliated with Union Pacific, Amtrak, the FRA, or the
Town of Truckee. Corrections welcome via issues.
