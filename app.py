import requests
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.image as mplimg
import matplotlib.animation as animation
import threading
import pygame
import re
from datetime import datetime
from collections import deque
from linecache import getline


# ── Audio setup 
pygame.mixer.init()
pygame.mixer.set_num_channels(200)   # do 200 simultanih piskov

_sound = None  

def load_sound(wav_path):
    global _sound
    _sound = pygame.mixer.Sound(wav_path)

def play_sound():

    if _sound:
        _sound.play() 

# ── Datumi
def parse_date(date):
    podatki = date.split()
    try:    year  = podatki[0]
    except: year  = None
    try:    month = podatki[1].capitalize()
    except: month = None
    try:    day   = podatki[2]
    except: day   = None

    if year and month and day:
        return datetime.strptime(f"{year} {month} {day}", "%Y %b %d")
    elif year and month:
        return datetime.strptime(f"{year} {month}", "%Y %b")
    elif year:
        return datetime.strptime(f"{year}", "%Y")
    return None

# ── podatki
def getdata():
    urls = [
        "https://www.johnstonsarchive.net/nuclear/tests/USA-ntests1.html",
        "https://www.johnstonsarchive.net/nuclear/tests/USA-ntests2.html",
        "https://www.johnstonsarchive.net/nuclear/tests/USA-ntests3.html",
        "https://www.johnstonsarchive.net/nuclear/tests/USA-ntestsH.html",
        "https://www.johnstonsarchive.net/nuclear/tests/USSR-ntests1.html",
        "https://www.johnstonsarchive.net/nuclear/tests/USSR-ntests2.html",
        "https://www.johnstonsarchive.net/nuclear/tests/USSR-ntests3.html",
        "https://www.johnstonsarchive.net/nuclear/tests/USSR-ntestsH.html",
        "https://www.johnstonsarchive.net/nuclear/tests/UK-ntests1.html",
        "https://www.johnstonsarchive.net/nuclear/tests/FR-ntests1.html",
        "https://www.johnstonsarchive.net/nuclear/tests/PRC-ntests1.html",
        "https://www.johnstonsarchive.net/nuclear/tests/PRC-ntestsH.html",
        "https://www.johnstonsarchive.net/nuclear/tests/OTH-ntests1.html",
    ]
    novtext = ""
    for u in urls:
        req = requests.get(u)
        text = req.text
        for line in text.splitlines():
            line = line[:-2] + "   " + re.search(r'/([A-Z]+)-', u).group(1) + "\n"
            novtext += line
        
    info = {"id": [], "series": [], "shot": [], "date": [], "lat": [], "lon": [], "country": []}

    for line in novtext.splitlines():
        if not line.strip() or not line.strip()[0].isdigit():
            continue
        try:
            id_    = line[0:5].strip()
            series = line[7:23].strip()
            shot   = line[23:48].strip()
            date   = line[46:59].strip()
            lat    = line[84:94].strip()
            lon    = line[94:105].strip()
            country = line[-4:].strip()

            if not lat or not lon:
                continue

            try:
                lat, lon = float(lat), float(lon)
            except ValueError:
                try:
                    lat = float(lat.split()[-1])
                    lon = float(lon.split()[-1])
                except:
                    continue

            if not date:
                continue
            if date[0].isdigit() and date[1].isdigit():
                date = parse_date(date)
            else:
                date = parse_date(line[48:61].strip())

            if date is None:
                continue

            info["id"].append(int(id_))
            info["series"].append(series)
            info["shot"].append(shot)
            info["date"].append(date)
            info["lat"].append(lat)
            info["lon"].append(lon)
            info["country"].append(country)
        except Exception:
            continue

    return info

# ── Animation 
def animate_map(info, duration, map_path, fps=30):
    load_sound("Media/beep-10.wav")
    print(len(info["country"]))
    fig, ax = plt.subplots(figsize=(12, 6))
    dates = info["date"]
    lats  = np.array(info["lat"])
    lons  = np.array(info["lon"])
    country = np.array(info["country"])

    ax.imshow(mplimg.imread(map_path), extent=[-180, 180, -90, 90])
    scat = ax.scatter([], [], color='purple', s=10)
    flash_scat = ax.scatter([], [], color='yellow', s=80, zorder=5, alpha=0.9) # tocka za flash efekt
    ax.set_xlim(-180, 180)
    ax.set_ylim(-90, 90)
    ax.set_aspect('auto')

    start_date  = min(dates)
    end_date    = max(dates)
    total_frames = fps * duration
    frame_times = [
        start_date + (end_date - start_date) * (i / total_frames)
        for i in range(total_frames)
    ]

    FLASH_FRAMES      = 4
    MAX_BEEPS_PER_FRAME = 20
    prev_count = [0]
    prev_mask  = [np.zeros(len(dates), dtype=bool)]  # ← track last frame's mask
    flash_buffer = deque()                            
    L=plt.legend(loc=1) 
    count_bombs_country = dict()
    
    def update(frame_idx):
        current_time = frame_times[frame_idx]
        mask = np.array([d <= current_time for d in dates])

        x, y = lons[mask], lats[mask]

        # ── guard against empty array ──
        if len(x) > 0:
            scat.set_offsets(np.column_stack((x, y)))

        else:
            scat.set_offsets(np.empty((0, 2)))

        ax.set_title(f"Date: {current_time.strftime('%Y %b %d')}")

         # flash ko nova tocka se pojavi -------------------------------
        new_mask = mask & ~prev_mask[0]
        new_x    = lons[new_mask]
        new_y    = lats[new_mask]

        nove_bombe = country[new_mask] # posodobi legendo bomb po državah
        for bomba in nove_bombe:
            if bomba in count_bombs_country:
                count_bombs_country[bomba] += 1
            else:
                count_bombs_country[bomba] = 1

        # rebuild legend
        labels = [f"{k if k != "OTH" else "IN/PAK/NK"}: {v}" for k, v in count_bombs_country.items()]
        handles = [plt.Line2D([], [], color='none') for _ in labels]

        ax.legend(handles, labels, loc=1)

        for nx, ny in zip(new_x, new_y):
            flash_buffer.append((frame_idx + FLASH_FRAMES, nx, ny))

        # Remove expired flashes
        while flash_buffer and flash_buffer[0][0] <= frame_idx:
            flash_buffer.popleft()

        if flash_buffer:
            flash_scat.set_offsets(np.column_stack(([e[1] for e in flash_buffer],
                                                     [e[2] for e in flash_buffer])))
        else:
            flash_scat.set_offsets(np.empty((0, 2)))

        prev_mask[0] = mask.copy()

        new_count  = int(mask.sum())
        new_points = min(new_count - prev_count[0], MAX_BEEPS_PER_FRAME)
        for _ in range(new_points):
            # fire-and-forget; pygame is thread-safe
            threading.Thread(target=play_sound, daemon=True).start()
        prev_count[0] = new_count

        return scat,

    ani = animation.FuncAnimation(
        fig, update,
        frames=total_frames,
        interval=1000 / fps,
        repeat=False
    )
    plt.show()
    return ani


info = getdata()
animate_map(info, 30, "D:/Xander/Python_Nuklearni_testi/Media/map5.jpg")