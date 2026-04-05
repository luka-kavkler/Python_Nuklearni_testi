import requests
import re
import geopandas as gpd
import matplotlib.pyplot as plt

def parse_coord(coords):
    """spremeni formatiranje koordinat"""
    vals = []
    for coord in coords:
        coord = coord.replace("~", "").replace("?", "").strip()
        coordsplit = coord.split()
        if len(coordsplit) == 2:
            value, direction = coordsplit
        else: 
            continue
        value = float(value)

        if direction in ["S", "W"]:
            value = -value
        vals.append(value)
    return vals

def getdata():
    """vrne slovar z vrsticami za vsak stolpec v bazi podatkov"""
    urls = ["https://www.johnstonsarchive.net/nuclear/atest45.html", "https://www.johnstonsarchive.net/nuclear/atest56.html", "https://www.johnstonsarchive.net/nuclear/atest58.html"
            "https://www.johnstonsarchive.net/nuclear/atest60.html", "https://www.johnstonsarchive.net/nuclear/atest62.html", "https://www.johnstonsarchive.net/nuclear/atest63.html"]

    text = ""
    for url in urls:
        req = requests.get(url)

        text += req.text

    rows = re.findall(r"<tr.*</tr>", text)
    cols = re.findall(r"<th>(.*?)</th>", rows[0])

    info = dict()
    label = []

    for col in cols:
        info[col.strip()] = []
        label.append(col.strip())

    for row in rows[1:]:
        cols = re.findall(r"<td>(.*?)</td>", row)
        for i in range(len(cols)):
            info[label[i]] += [cols[i]]

    return info

def draw_map(info):
    """narise tocke na zemljevidu iz podatkov"""

    url = "https://naturalearth.s3.amazonaws.com/110m_cultural/ne_110m_admin_0_countries.zip" # nalozi ozadje 
    world = gpd.read_file(url)
    
    info["longitude"] = parse_coord(info["longitude"])
    info["latitude"] = parse_coord(info["latitude"])
    
    points = gpd.GeoDataFrame(
        geometry=gpd.points_from_xy(
            info["longitude"],  # longitude
            info["latitude"]  # latitude
        )
    )
    world.plot()
    points.plot(ax=plt.gca(), color='red')

    plt.show()


info = getdata()
draw_map(info)





