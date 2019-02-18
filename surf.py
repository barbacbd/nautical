#!/usr/bin/env python

import io
import analysis
from wave_data import WaveLocations


def main():
    wl = WaveLocations()

    id = wl.vb_id

    init_url = "https://www.ndbc.noaa.gov/station_page.php?station="
    search_url = "{}{}".format(init_url, id)

    current_data = io.get_current_data(search_url, id)
    detailed_data = io.get_detailed_wave_summary(search_url)
    past_swell = io.get_swell_data(search_url)
    past_wave = io.get_wave_table(search_url)

if __name__ == "__main__":
    main()
