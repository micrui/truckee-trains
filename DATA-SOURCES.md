# Data sources and provenance

## Amtrak status (data/amtrak/)

- Community Amtraker API (https://api.amtraker.com/v3, code at
  https://github.com/piemadd/amtrak, AGPL-3.0), which mirrors Amtrak's public live map.
  Polled every 30 minutes by `amtrak_poll.py` with an identifying user agent; attribution
  given on the status page. Amtrak publishes no official API; if Amtraker goes away, the
  government-hosted ArcGIS mirror
  (https://gis.fema.gov/arcgis/rest/services/Partner/Amtrak_Train_Status/MapServer) is the
  fallback.
- Historical punctuality back to 2008 exists in the Amtrak Status Maps Archive Database
  (https://juckins.net), a single maintainer's archive with no export interface. It is not
  used here; any future use follows a direct request to its maintainer.

## Federal crossing records (data/fra/)

- FRA National Highway-Rail Crossing Inventory via the public GIS service
  (https://fragis.fra.dot.gov/arcgis/rest/services/FRA/FRAGradeXing/MapServer), pulled
  monthly for crossing 753183A by `crossing_pull.py`; changes logged with dates.
- Crossing accident histories (FRA Form 6180.57) retrieved manually from
  https://safetydata.fra.dot.gov/OfficeofSafety/publicsite/crossing/crossing.aspx; the site
  cites the records rather than republishing the PDFs.

## Reference claims

Every page cites its sources inline. Union Pacific publishes no freight schedule and no
tonnage figures for the pass; where the record is silent, the pages say so instead of
estimating.

## Credentials

None. Every source used by automation is public and unauthenticated; keep it that way.
