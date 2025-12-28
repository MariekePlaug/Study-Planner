# Imports
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.dates as mdates
from datetime import datetime, timedelta


# Load File
BASE_DIR: Path = Path(__file__).resolve().parents[2]
DATA_DIR: Path = BASE_DIR / "data"
WEEK_DAYS: list[str] = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
HOURS = np.arange(0, 24)

file = DATA_DIR / "planner_template - chavez_pope.csv"

user = "Chavez"

df = pd.read_csv(file).set_index("course_name")

# Prepare the data
df["start_time"] = pd.to_datetime(df["start_time"], format="%H:%M")
df["duration"] = pd.to_timedelta(df["duration"], unit="minutes")
df["end_time"] = df["start_time"] + df["duration"]

# dynamic y-axis
earliest_time = datetime(year = 1900, month = 1, day = 2, hour = 0, minute = 0)
latest_time = datetime(year = 1900, month = 1, day = 1, hour = 0, minute = 0)
for subject, row in df.iterrows():
    starttime = row["start_time"]
    endtime = row["end_time"]
    if starttime < earliest_time:
        earliest_time = starttime
    if endtime > latest_time:
        latest_time = endtime
print(earliest_time, latest_time)

y_bounds = [(earliest_time - timedelta(hours = 2)).hour, (latest_time + timedelta(hours = 2)).hour]
print(y_bounds)

yticks = np.arange(y_bounds[0]*60, y_bounds[1]*60 +1, 60)
print(len(yticks))
print(yticks)

figsize_timetable = [8,6]
height_ratios = [1,8]
day_width = figsize_timetable[0] / len(WEEK_DAYS)
text_offset = [day_width /2, height_ratios[0] / 2]

fig = plt.figure(figsize = figsize_timetable)
fig.subplots_adjust(left=0.1, right=0.95)
gs = fig.add_gridspec(2, 1, height_ratios = height_ratios, hspace=0.0)



ax1 = fig.add_subplot(gs[0])
for i in range(len(WEEK_DAYS)):
    rec = Rectangle( (i * day_width, 0), day_width, 1, edgecolor="black", facecolor="skyblue" )
    ax1.add_patch(rec)

    ax1.text(i * day_width + text_offset[0], text_offset[1], f"{WEEK_DAYS[i]}", ha="center", va="center", fontsize=12)

ax1.set_xlim(0, figsize_timetable[0])
ax1.set_ylim(0,1)
ax1.axis("off")
ax1.set_title(f"{user}'s Study Timetable \n", fontsize = 16)

ax2 = fig.add_subplot(gs[1], sharex = ax1)
ax2.set_yticks(yticks)
ax2.set_ylim(yticks[0], yticks[-1])
ax2.invert_yaxis()
ax2.set_yticklabels([f"{int(h/60):02d}:00" for h in yticks])
ax2.set_ylabel("Hour")
ax2.set_xticks([])

# plotting the courses:
# Convert to mdates float values that change dynamically with changing figsize
df["y"] = mdates.date2num(df["start_time"])
df["height"] = mdates.date2num(df["end_time"]) - df["y"]

# Map day names to x positions
day_to_x = {day: i * figsize_timetable[0]/len(WEEK_DAYS) for i, day in enumerate(WEEK_DAYS)}
df["x"] = df["day"].map(day_to_x)




for subject, row in df.iterrows():
    x = row["x"]
    y = row["start_time"].hour * 60 + row["start_time"].minute  # Minutes since midnight
    width = figsize_timetable[0] / len(WEEK_DAYS)  # One day wide
    height = row["duration"].total_seconds() / 60  # Duration in minutes

    period = Rectangle(
        xy=(x, y),
        width=width,
        height=height,
        facecolor="skyblue",
        edgecolor="black",
        label = subject
    )
    ax2.add_patch(period)
    ax2.text(x + width*1/3, y + height*2/3, subject[0:6])
ax2.legend()

plt.show()

