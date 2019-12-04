# Query-a-Cat(alog)

CLI application to query a CSW catalog written in Python, outputs results in JSON format.

## Installation dependencies

See `requirements.txt` file. Install depedencies with:

```
pip3 install -r requirements.txt
```

Requires Python version >= 3.6.8.

## Installation application

Install query-a-cat with (executed from root of repository):

```
pip3 install .
```
## Usage

```
qac csw --help
Usage: qac csw [OPTIONS] CSW_ENDPOINT QUERY

  Query CSW

Options:
  --result-type [hits|uids|summary|full]
  --limit INTEGER
  --help                          Show this message and exit.
```

## Usage examples

```
qac csw https://www.nationaalgeoregister.nl/geonetwork/srv/dut/csw "identifier='bf8b2e13-1af2-5cf5-a7c5-6c0d3d363ea6'" --result-type summary
qac csw https://www.nationaalgeoregister.nl/geonetwork/srv/dut/csw "organisationName='Provincie Drenthe'" --result-type hits
qac csw https://www.nationaalgeoregister.nl/geonetwork/srv/dut/csw "keyword='defensie'" --result-type hits
qac csw https://www.nationaalgeoregister.nl/geonetwork/srv/dut/csw "type='service'" --result-type hits  
qac csw https://www.nationaalgeoregister.nl/geonetwork/srv/dut/csw "type='dataset'" --result-type hits  
qac csw https://www.nationaalgeoregister.nl/geonetwork/srv/dut/csw "type='dataset' AND keyword='defensie'" --result-type hits
qac csw https://www.nationaalgeoregister.nl/geonetwork/srv/dut/csw "anytext LIKE '%Kadaster%'" --result-type hits
qac csw https://www.nationaalgeoregister.nl/geonetwork/srv/dut/csw "" --result-type hits
qac csw https://www.nationaalgeoregister.nl/geonetwork/srv/dut/csw "type='service' AND organisationName='Beheer PDOK'" --result-type uids
qac csw-download https://www.nationaalgeoregister.nl/geonetwork/srv/dut/csw "type='service' AND organisationName='Beheer PDOK'"
```

## Result-types

- `hits`: prints outs number of matched records

```
{"numberOfRecordsMatched": 386}
```

- `uids`: prints out list of (metadata)identifiers of matched records

```
[
    "c3593105-cd26-48a4-bd06-ad931cc262da",
    "86cb5bcc-a199-43e2-9e03-2d0fe8bdfa3f",
    "a84f9836-9111-4e45-a311-3dab39019e15",
    "d467c2cc-4026-b80a-d4e1a9d2bf79"
]
```

- `summary`: prints out list of matched records (summary)


```
[{
        "modified": "2017-11-03",
        "identifier": "dd2c0d91-43b1-41ec-bdda-c822d8940475",
        "titel": "BRT achtergrondkaart Pastel WMTS",
        "abstract": "De achtergrondkaart PDOK is de kaartlaag waarop locatiegebonden content wordt afgebeeld. De achtergrondkaart moet ervoor zorgen dat de eindgebruiker zich kan orienteren tijdens het gebruik van geografische applicaties. Data automatisch gegeneraliseerd op basis van TOP10NL. Buiten de standaard projectie EPSG:28992 (Amersfoort / RD New) wordt deze service ook geleverd in de projectie EPSG:25831 (ETRS89 / UTM zone 31N).",
        "md_type": "service",
        "keywords": [
            "Achtergrond",
            "Ondergrond",
            "Referentie",
            "PDOK",
            "infoMapAccessService"
        ]
}]
```

- `full`: prints out list of matched records with xml in base64 encoded field

```
[{
    "uid": "c0a8e0ee-8639-44d4-be07-d7edf9c276c7",
    "encoding": "base64"
    "md_record": "PGdtZDpNRF9NZXRhZGF0YSB4bWxuczpnbWQ9Imh0dHA6Ly93d3cuaXNvdGMyMTEub3JnLzIwMDUvZ21kIiB4bWxuczpnY289Imh0dHA6Ly93d3cuaXNvdGMyMTEub3JnLzIwMDUvZ2NvIiB4bWxuczpnbWw9Imh0dHA6Ly93d3cub3Blbmdpcy5uZXQvZ21sLzMuMiIgeG1sbnM6Z214PSJodHRwOi8vd3d3Lmlzb3RjMjExLm9yZy8yMDA1L2dteCIgeG1sbnM6Z3NyPSJodHRwOi8vd3d3Lmlzb3RjMjExLm9yZy8yMDA1L2dzciIgeG1sbnM6Z3RzPSJodHRwOi8vd3d3Lmlzb3RjMjExLm9yZy8yMDA1L2d0cyIgeG1sbnM6c3J2PSJodHRwOi8vd3d3Lmlzb3RjMjExLm9yZy8yMDA1L3NydiIgeG1sbnM6eGxpbms9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGxpbmsiIHhtbG5zOnhzPSJodHRwOi8vd3d3LnczLm9yZy8yMDAxL1hNTFNjaGVtYSIgeG1sbnM6eHNpPSJodHRwOi8vd3d3LnczLm9yZy8yMDAxL1hNTFNjaGVtYS1pbnN0YW5jZSIgeG1sbnM6Z2VvbmV0PSJodHRwOi8vd3d3LmZhby5vcmcvZ2VvbmV0d29yayIgeG1sbnM6Y3N3PSJodHRwOi8vd3d3Lm9wZW5naXMubmV0L2NhdC9jc3cvMi4wLjIiIHhzaTpzY2hlbWFMb2NhdGlvbj0iaHR0cDovL3d3...
    ...
}]
```