
use std::collections::HashMap;
use std::env;

use std::fs::File;
use std::io::{self, prelude::*, BufReader};
use std::time::SystemTime;

struct Record {
    min: f32,
    max: f32,

    sum: f32,
    qtd: f32,
}


fn main() -> io::Result<()> {
    let args: Vec<String> = env::args().collect();

    let start = SystemTime::now();

    let file = File::open(&args[1])?;
    let reader = BufReader::new(file);

    let mut records: HashMap<String, Record> = HashMap::new();

    for line in reader.lines() {
        let line = line?;
        let (station, measurement) = line.split_once(";").unwrap();

        let measurement = measurement.parse::<f32>().unwrap();

        records.entry(station.to_string())
            .and_modify(|record| {
                record.min = record.min.min(measurement);
                record.max = record.max.max(measurement);
                record.sum = record.sum + measurement;
                record.qtd = record.qtd + 1.0;
            })
            .or_insert_with(|| {
                Record {
                    min: measurement,
                    max: measurement,
                    sum: measurement,
                    qtd: 1.0
                }
            });
    }

    print!("{{");

    for (station, record) in records {
        print!("{}={}/{:.1}/{},", station, record.min, record.sum / record.qtd, record.max);
    }

    println!("}}");

    eprintln!("Timing {}", SystemTime::now().duration_since(start).unwrap().as_millis());


    Ok(())
}
