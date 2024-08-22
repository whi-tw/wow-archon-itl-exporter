import sys
from datetime import datetime

import requests
from bs4 import BeautifulSoup as bs4

from exporter import CategoryCreator, LoadoutData

creator = CategoryCreator()

session = requests.sessions.Session()
session.headers = {"User-Agent": "Mozilla/5.0"}

c_class = "demon-hunter"
c_spec = "vengeance"
c_week = "this-week"

dungeons = [
    "all-dungeons",
    "algethar-academy",
    "brackenhide-hollow",
    "halls-of-infusion",
    "neltharus",
    "ruby-life-pools",
    "the-azure-vault",
    "the-nokhud-offensive",
    "uldaman",
]

url_format = "https://www.archon.gg/wow/builds/{char_spec}/{char_class}/mythic-plus/overview/10/{dungeon}/{week}"

data: LoadoutData = LoadoutData(
    name=f"Archon M+ @{datetime.now().strftime('%Y-%m-%d %H:%M')}", loadouts={}
)

if len(sys.argv) > 1:
    c_spec, c_class = sys.argv[1:]
for i, dungeon in enumerate(dungeons):
    url = url_format.format(
        char_spec=c_spec, char_class=c_class, week=c_week, dungeon=dungeon
    )
    r = session.get(url)
    r.raise_for_status()
    soup = bs4(r.text, "html.parser")
    export_div = soup.find("div", {"class": "talent-tree__interactions-export"})
    export_href = export_div.find("a")["href"]
    export_string = export_href.split("/")[-1]
    data.loadouts[f"{i}: {dungeon}"] = export_string

export = creator.create_export_string(data)

print(f"{c_spec} {c_class} M+: {export}")
