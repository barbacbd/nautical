from nautical.io.sources import get_buoy_sources
from nautical.io.web import get_noaa_forecast_url
from json import dumps
from os import remove, mkdir
from os.path import exists
from urllib.request import urlopen
from shutil import rmtree
from urllib.error import HTTPError, URLError


if exists("webpages"):
    rmtree("webpages")
mkdir("webpages")

# list includes past names in the event that these were ever
# artifacts from previous runs
json_files = ["sources.json", "urls.json", "buoys.json"]
for jf in json_files:
    if exists(jf):
        print("Removing {}".format(jf))
        remove(jf)

sources = get_buoy_sources()
data = {"sources": None, "urls": None, "failures": None}
source_data = {}
urls = {}
failures = {}

for k, v in sources.items():
    buoys = [str(b.station) for b in v]
    source_data[str(k)] = buoys

    path = "webpages/{}".format(str(k).replace(" ", "-").replace("/", "-"))
    
    urls[str(k)] = []
    failures[str(k)] = []
    mkdir(path)
    for b in buoys:
        urls[str(k)].append(get_noaa_forecast_url(str(b)))

        try:
            with open("{}/{}.html".format(path, str(b)), "w+") as f:
                f.write(urlopen(get_noaa_forecast_url(str(b))).read().decode('utf-8'))
        except (HTTPError, URLError) as e:
            failures[str(k)].append(str(b))

data["sources"] = source_data
data["urls"] = urls
data["failures"] = failures

with open("buoys.json", "w+") as f:
    f.write(dumps(data, indent=4))


    
