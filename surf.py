#!/usr/bin/env python

import io


def main():

    vb_id = 44099
    init_url = "https://www.ndbc.noaa.gov/station_page.php?station="
    search_url = "{}{}".format(init_url, vb_id)

    data = io.get_wave_table(search_url)

    for x in data:
        print(x.to_string())


if __name__ == "__main__":
    main()
