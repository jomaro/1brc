# 1brc - 1 Billion Rows Challenge

These are my attempts at the [1 billion rows challenge](https://github.com/gunnarmorling/1brc)

Note: The implementation does not follow the specified output format


### Timings

| Version         | Size | Time (average) | Time (std) |
|-----------------|------|---------------:|-----------:|
| Elx.serial_v1   | 1k   |              7 |          1 |
| Elx.serial_v1   | 1m   |           1606 |         29 |
| Elx.serial_v1   | 10m  |          15520 |        280 |
| Elx.serial_v1   | 1b   |        1842119 |      24642 |
| Elx.parallel_v1 | 1k   |             22 |          2 |
| Elx.parallel_v1 | 1m   |            439 |          8 |
| Elx.parallel_v1 | 10m  |           4289 |        114 |
| Elx.parallel_v1 | 1b   |         477376 |       3304 |


Test data generated with seed `1707066384638`


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

3. Run the elixir versions 

```
cd elx
mix compile
```

Run sequential version

```
mix run -e "Elx.serial_v1(\"m10m\")"
```


Run parallel version

```
mix run -e "Elx.parallel_v1(\"m10m\")"
```

