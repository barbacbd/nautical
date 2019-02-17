#!/usr/bin/env python

import io
import analysis


def main():

    vb_id = 44099
    init_url = "https://www.ndbc.noaa.gov/station_page.php?station="
    search_url = "{}{}".format(init_url, vb_id)

    data = io.get_wave_table(search_url)

    print(analysis.analyze_dominant_wave_period(data, 10))


if __name__ == "__main__":
    main()
