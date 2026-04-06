# Constituency GeoJSON Sources for Upcoming State Elections in India

Date verified: 2026-03-05

## Scope
You asked where to find constituency GeoJSONs for upcoming state elections in India.

## High-confidence sources (usable now)

### 1) DataMeet (Pan-India assembly constituencies; shapefile)
- Repository: https://github.com/datameet/maps/tree/master/assembly-constituencies
- Direct downloads:
  - https://raw.githubusercontent.com/datameet/maps/master/assembly-constituencies/India_AC.shp
  - https://raw.githubusercontent.com/datameet/maps/master/assembly-constituencies/India_AC.dbf
  - https://raw.githubusercontent.com/datameet/maps/master/assembly-constituencies/India_AC.shx
  - https://raw.githubusercontent.com/datameet/maps/master/assembly-constituencies/India_AC.prj
- Source caveats (important): https://raw.githubusercontent.com/datameet/maps/master/assembly-constituencies/README.md

Notes from source caveats:
- Some states may be pre-delimitation in that dataset.
- Some constituency names/geometry alignment may need validation before production use.

### 2) INDIAN-SHAPEFILES (state-level GeoJSON files; quick to use)
- Repository: https://github.com/datta07/INDIAN-SHAPEFILES
- Data vintage/currency note: https://raw.githubusercontent.com/datta07/INDIAN-SHAPEFILES/master/README.md

Direct assembly GeoJSON links verified as reachable (HTTP 200):
- Assam: https://raw.githubusercontent.com/datta07/INDIAN-SHAPEFILES/master/STATES/ASSAM/ASSAM_ASSEMBLY.geojson
- Kerala: https://raw.githubusercontent.com/datta07/INDIAN-SHAPEFILES/master/STATES/KERALA/KERALA_ASSEMBLY.geojson
- Tamil Nadu: https://raw.githubusercontent.com/datta07/INDIAN-SHAPEFILES/master/STATES/TAMIL%20NADU/TAMIL%20NADU_ASSEMBLY.geojson
- West Bengal: https://raw.githubusercontent.com/datta07/INDIAN-SHAPEFILES/master/STATES/WEST%20BENGAL/WEST%20BENGAL_ASSEMBLY.geojson
- Puducherry: https://raw.githubusercontent.com/datta07/INDIAN-SHAPEFILES/master/STATES/PUDUCHERRY/PUDUCHERRY_ASSEMBLY.geojson

## Official references for legal/latest boundary validation

### Election Commission of India (ECI) delimitation documents
- Assam final papers: https://www.eci.gov.in/Documents/Delimitation/FINAL-PAPERS1-7.pdf
- Assam delimitation update/order document: https://www.eci.gov.in/Documents/Delimitation/DELIMITATIONASSAM_UPDATED.pdf
- Delimitation Order 2008 (base legal doc): https://www.eci.gov.in/Documents/Delimitation/DelimitationofParliamentaryAssemblyConstituenciesOrder-2008%28English%29.pdf

Use these to validate geometry and constituency names/codes before election analytics or publication.

## Government GIS portals checked

### State GIS Portal (official)
- Portal: https://stategisportal.nic.in/stategisportal
- State map pages checked live (HTTP 200):
  - Assam: https://stategisportal.nic.in/stategisportal/Home/Map/18
  - West Bengal: https://stategisportal.nic.in/stategisportal/Home/Map/19
  - Kerala: https://stategisportal.nic.in/stategisportal/Home/Map/32
  - Tamil Nadu: https://stategisportal.nic.in/stategisportal/Home/Map/33
  - Puducherry: https://stategisportal.nic.in/stategisportal/Home/Map/34

### Bharat Map Service/NIC ArcGIS endpoints observed
- Service index:
  - https://mapservice.gov.in/mapserviceserv176/rest/services?f=pjson
- AC/PC map service URL found in State GIS config:
  - https://mapservice.gov.in/gismapservice/rest/services/BharatMapService/AC_PC/MapServer

## Technical finding on official AC/PC API access
- The AC/PC ArcGIS endpoint currently requires a valid token.
- Public requests without a fresh valid token returned token errors in tests.
- The State GIS front-end references the AC/PC service but direct extraction via static token in config was not valid at check time.

Practical implication:
- For immediate GeoJSON use, community GeoJSON/shapefile sources above are faster.
- For official-grade publication, cross-check against ECI delimitation documents.

## Additional checks attempted
- State GIS portal root and state pages were reachable.
- Some older/alternate GIS links are inconsistent or not directly exposing downloadable constituency data.

## Recommended workflow
1. Start with state GeoJSON from INDIAN-SHAPEFILES for speed.
2. Cross-check names/codes/boundaries with ECI delimitation PDFs.
3. If needed, normalize to a common schema (state, AC_NO, AC_NAME, PC_NAME, etc.).
4. Keep a note of source/date in downstream outputs.
