# 1brc - 1 Billion Rows Challenge

These are my attempts at the [1 billion rows challenge](https://github.com/gunnarmorling/1brc)

The implementation does not follow the specified output format

## Setup


1. Download `weather_stations.csv` file

```
wget https://raw.githubusercontent.com/gunnarmorling/1brc/ba20cd8439fdcdcd8c33fb6d3f9532afc07ade52/data/weather_stations.csv
sha256sum --check checksums
```

2. Generate test sets

OBS. This is a different version from the script provided by the initial proponents of the challenge. 
This version has been modified primarily to allow the creation of files with an arbitrary number of rows

```
python create.py -m 1_000 -o m1k
python create.py -m 1_000_000 -o m1m
python create.py -m 10_000_000 -o m10m
python create.py -m 1_000_000_000 -o m1b
```

3. Run the elixir sequential version 

```
cd elx
mix compile
time mix run -e "Elx.version1(\"m10m\")"
```
