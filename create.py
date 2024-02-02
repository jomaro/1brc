#!/usr/bin/env python
#
#  Copyright 2023 The original authors
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

# Based on https://github.com/gunnarmorling/1brc/blob/main/src/main/java/dev/morling/onebrc/CreateMeasurements.java

import argparse
import math
import os
import random
import statistics
import sys
import time


def parse_args():
    """
    Parse arguments providing help if necessary
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("-m", "--measurements", help = "Number of measurements to generate. Default: 1_000_000_000", type=int, default=1_000_000_000)
    parser.add_argument("-c", "--stations", help = "Number of stations to use. Default: sqrt(--measurements)", type=int)
    parser.add_argument("-o", "--output", help = "Output filename.")
    parser.add_argument("-s", "--seed", help = "Seed for deterministic generation of measurements.", type=int)

    args = parser.parse_args()
    args.stations = args.stations or math.floor(math.sqrt(args.measurements))
    args.output = args.output or 'measurements'
    args.seed = args.seed or int(time.time() * 1_000)

    return args


def build_weather_station_name_list(n_stations: int):
    """
    Grabs the weather station names from example data provided in repo and deduplicates
    """
    station_names = []
    with open('weather_stations.csv', 'r') as file:
        for station in file.readlines():
            if station.startswith('#'):
                continue
            
            station_names.append(station.split(';')[0])

    return random.sample(sorted(set(station_names)), n_stations)


def convert_bytes(num):
    """
    Convert bytes to a human-readable format (e.g., KiB, MiB, GiB)
    """
    for x in ['bytes', 'KiB', 'MiB', 'GiB']:
        if num < 1024.0:
            return f"{num:.1f} {x}"
        num /= 1024.0


def format_elapsed_time(seconds):
    """
    Format elapsed time in a human-readable format
    """
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    match (hours, minutes, seconds):
        case (0, 0, seconds):
            return f"{seconds:.3f} seconds"
        case (0, minutes, seconds):
            return f"{int(minutes)} minutes {int(seconds)} seconds"
        case (hours, 0, seconds):
            return f"{int(hours)} hours {int(seconds)} seconds"
        case (hours, minutes, seconds):
            return f"{int(hours)} hours {int(minutes)} minutes {int(seconds)} seconds"


def estimate_file_size(weather_station_names, num_rows_to_create):
    """
    Tries to estimate how large a file the test data will be
    """
    per_record_size = statistics.mean(len(station) for station in weather_station_names) + len(",-123.4")

    total_file_size = num_rows_to_create * per_record_size
    human_file_size = convert_bytes(total_file_size)

    print(f"Estimated max file size is:  {human_file_size}.")


def build_test_data(weather_station_names, args):
    """
    Generates and writes to file the requested length of test data
    """
    num_rows_to_create = args.measurements
    output_file_name = f"{args.output}.txt"
    start_time = time.time()
    coldest_temp = -99.9
    hottest_temp = 99.9
    batch_size = min(num_rows_to_create, 2_000) # instead of writing line by line to file, process a batch of stations and put it to disk
    progress_step = max(1, (num_rows_to_create // batch_size) // 100)

    print(f'Using seed {args.seed}')
    print(f'Effective number of stations {len(weather_station_names)}')
    print('Building test data...')

    try:
        with open(output_file_name, 'w') as file:
            for s in range(0, num_rows_to_create // batch_size):
                
                batch = random.choices(weather_station_names, k=batch_size)
                prepped_deviated_batch = ''.join(f"{station};{random.uniform(coldest_temp, hottest_temp):.1f}\n" for station in batch) # :.1f should quicker than round on a large scale, because round utilizes mathematical operation
                file.write(prepped_deviated_batch)
                
                # Update progress bar every 1%
                if s % progress_step == 0 or s == num_rows_to_create - 1:
                    sys.stdout.write("\r[%-50s] %d%%" % ('=' * int((s + 1) / num_rows_to_create * 50), (s + 1) / num_rows_to_create * 100))
                    sys.stdout.flush()
        sys.stdout.write('\n')
    except Exception as e:
        print("Something went wrong. Printing error info and exiting...")
        print(e)
        exit()
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    file_size = os.path.getsize(output_file_name)
    human_file_size = convert_bytes(file_size)
 
    print(f"Test data successfully written to {output_file_name}")
    print(f"Actual file size:  {human_file_size}")
    print(f"Elapsed time: {format_elapsed_time(elapsed_time)}")


def main():
    """
    main program function
    """
    args = parse_args()

    random.seed(args.seed)

    weather_station_names = build_weather_station_name_list(args.stations)

    estimate_file_size(weather_station_names, args.measurements)

    build_test_data(weather_station_names, args)

    print("Test data build complete.")


if __name__ == "__main__":
    main()
