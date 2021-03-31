# Utility to create a global map of ips connecting to an Apache2 webserver based on ip geolocation 

import pandas as pd;
import geopandas as gpd;
from shapely.geometry import Point;
import matplotlib.pyplot as plt;
import requests
import json
import time

# Filepaths
ACCESS_PATH = "access.log";
EXPORT_PATH = "map.png";

# Generate worldmap
worldMap = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"));

# Parse access file into ip list
with open(ACCESS_PATH) as accessFile:
    logList = accessFile.readlines();

ipList = ["1"]; # Init list

i = 0;
# Parse through logList
while(i < len(logList)):
    line = logList[i];
    curIp = line.split(" ", 1)[0];
    # Check if ip is previously occuring in list
    if(("192.168" not in curIp) or (curIp != ipList[-1])):
        ipList.append(curIp);
    i+=1;

# Remove init value
del ipList[0];

# Create dict used to create geo data frame
ipDict = {"col1":[] , "geometry": []};

# Get geodata from ip string
for ip in ipList:
    # API request for ip info https://www.abstractapi.com/ip-geolocation-api
    #FIXME Insert your own api key here
    response = requests.get("https://ipgeolocation.abstractapi.com/v1?api_key=INSERT_KEY_HERE_&ip_address={}&fields=longitude,latitude".format(ip));
    # Check for valid status code 200
    if(200 == response.status_code):
        jsonDict = json.loads(response.content);
        ipPoint = Point(jsonDict["longitude"], jsonDict["latitude"]);
        # Add to ip dict
        ipDict["col1"].append(len(ipDict["geometry"]));
        ipDict["geometry"].append(ipPoint);
    # Sleep 1 sec for api
    time.sleep(1.1);

# Convert dict into geopandas dataframe
ipMap = gpd.GeoDataFrame(ipDict, crs=worldMap.crs);

# Print ips on world map
base = worldMap.plot(color="white", edgecolor="black");
ipMap.plot(ax=base, marker="o", color="red", markersize=3);

# Hide axis
plt.axis("off");

# Show map
# plt.show();

# Export map to image png
plt.savefig(EXPORT_PATH, bbox_inches="tight");


