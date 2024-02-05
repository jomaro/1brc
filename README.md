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
| Rst.serial_v1   | 1k   |              0 |          0 |
| Rst.serial_v1   | 1m   |            122 |          0 |
| Rst.serial_v1   | 10m  |           1205 |         14 |
| Rst.serial_v1   | 1b   |         167712 |        680 |


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
python create.py -m 1_000 -o m1k.txt
python create.py -m 1_000_000 -o m1m.txt
python create.py -m 10_000_000 -o m10m.txt
python create.py -m 1_000_000_000 -o m1b.txt
```

3. Run the elixir versions

```
cd elx
mix compile
```

Run sequential version

```
mix run -e "Elx.serial_v1(\"m1b\")"
```


Run parallel version

```
mix run -e "Elx.parallel_v1(\"m1b\")"
```

4. Run the rust version

```
cd rst
cargo build --release
```

Run sequential version

```
./target/release/rst ../m1b.txt
```
