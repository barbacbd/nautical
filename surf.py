#!/usr/bin/env python

import io
import analysis


def main():

    vb_id = 44099
    init_url = "https://www.ndbc.noaa.gov/station_page.php?station="
    search_url = "{}{}".format(init_url, vb_id)

    data = io.get_wave_table(search_url)

    header = "Current information at buoy {}\n".format(vb_id)
    wave_ht = "Wave Height = {} Feet\n".format(data[0].wvht)
    period = "Average Period = {} secs with a Dominant Period = {} secs\n".format(data[0].apd, data[0].dpd)
    dir = "The waves are out of the {}\n".format(data[0].mwd)
    temp = "The Water temperature = {}".format(data[0].wtmp)

    current = "{}{}{}{}{}".format(header, wave_ht, period, dir, temp)
    print(current)


if __name__ == "__main__":
    main()
