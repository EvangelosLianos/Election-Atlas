# NY Metro Election Atlas — portable 2024 research website

This is a complete static website with real 2024 ED boundaries and statewide 2024 election results for Queens, Nassau, and Suffolk. **No paid services, login, API keys, or backend required.** The site is designed for transfer to other people and devices.

## Fastest way to share it publicly (GitHub Pages)

1. Unzip the supplied archive.
2. Create a public GitHub repository, e.g. `ny-metro-election-atlas`.
3. Upload the **contents** of the `election_atlas` folder (`index.html`, `app.js`, and the `data/` folder) to the repository root.
4. In GitHub **Settings → Pages**, choose **Deploy from a branch**, branch **main**, folder **/(root)**, and Save.
5. GitHub will provide a public `https://USERNAME.github.io/ny-metro-election-atlas/` address. Share that link with anyone; it works on desktop and mobile browsers.

Alternatively, upload the folder to Netlify Drop or any static web host. The site requires an internet connection to load the Leaflet JavaScript library and the CARTO/OpenStreetMap basemap; all ED and election results are hosted with the website itself.

## Run locally

On a Mac or PC with Python 3, open a terminal in this folder and run:

```bash
python3 -m http.server 8000
```

Open http://localhost:8000. Do **not** double-click `index.html` directly: browsers block the local GeoJSON fetch when opened using `file://`.

## Features

- 3,349 matched 2024 ED boundary/result records across Queens, Nassau and Suffolk
- Choropleths for President, U.S. House, U.S. Senate, NY State Senate, NY State Assembly, and Proposition 1
- County, congressional district, and Assembly District filters
- ED outlines, derived AD and CD outlines, labeled reference towns/neighborhoods, interactive ED inspector
- Congressional ballot-line counts, two-ED comparison, search, and CSV export
- Responsive desktop/mobile layout

## Sources and limitations

- ED boundaries: `NYStatewide_Nov24_ED_Consolidated_011125.geojson` (Rosenblatt, November 2024).
- Results: `NY_2024StatewideResults-75a75e51.xlsx` (Rosenblatt statewide 2024 results workbook).
- Joined by `GEOID24`: 3,349/3,349 three-county records matched. Three invalid source polygons were repaired during map processing; geometries were simplified for performance.
- ED outlines reflect November 2024 geography, not current 2026 boundaries. AD and CD outlines are **derived by dissolving the supplied ED polygons** based on workbook labels; they are not authoritative legislative boundary files. Validate before legal/operational use.
- Basemap labels from OpenStreetMap/CARTO; additional neighborhood and village names are approximate reference points, **not jurisdictional boundaries**.
- Election totals are from an independent compilation, **not yet fully reconciled** with official county certified ED-level reports.
- Election data are candidate totals. State Assembly and State Senate races feature different candidates in different districts; the map compares the workbook's party totals, not one named statewide candidate. Blank workbook cells are treated as zero for rendering; do not interpret gray districts as definitive zero turnout.
- The website does **not yet** include 2020 ED population allocations, ACS estimates, enrollment, polling sites, 2016–2023 elections, 2025/2026 elections, or individual voter records. Do not interpret it as having those datasets.
- The site does not provide real-time results or automatic updates.

## Extend the website

`data/districts.geojson` is a standard GeoJSON FeatureCollection. Each feature has `properties.id` (2024 GEOID), county, municipality, ED name, AD/SD/CD identifiers, and result columns. New datasets can be joined by the correct historical ED identifier and geography vintage. To add a new election year, use year-specific polygons and results and expose a year selector; do not assume 2024 ED IDs or boundaries remain stable.

## Rebuild

The data preparation script used in this build is included in the separate source archive root as `build_atlas.py` (optional). To rebuild, place the original two Rosenblatt source files at the paths specified in that script and run it with Python, shapely, and openpyxl installed.
