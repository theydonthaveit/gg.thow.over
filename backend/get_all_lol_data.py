import requests
import os
import json

season = 9
patch = 10
version = 1

champions_url = f"http://ddragon.leagueoflegends.com/cdn/{season}.{patch}.{version}/data/en_US/champion.json"

item_url = f"http://ddragon.leagueoflegends.com/cdn/{season}.{patch}.{version}/data/en_US/item.json"

sum_spell_url = f"http://ddragon.leagueoflegends.com/cdn/{season}.{patch}.{version}/data/en_US/summoner.json"

# champs_res = requests.get(champions_url)
# champions = champs_res.json()
# champ_data = champions.get("data")

# for champion in champ_data.keys():
#     url = f"http://ddragon.leagueoflegends.com/cdn/{season}.{patch}.{version}/data/en_US/champion/{champion}.json"

#     specific_champ_res = requests.get(url)

#     champion_dir = os.path.join("data", "champions")

#     if not os.path.exists(champion_dir):
#         os.makedirs(champion_dir)

#     with open(f"{champion_dir}/{champion}.json", "w+") as champ_file:
#         json.dump(specific_champ_res.json(), champ_file, ensure_ascii=False)


item_res = requests.get(item_url)
items = item_res.json()
item_data = items.get("data")

item_dir = os.path.join("data", "items")

if not os.path.exists(item_dir):
    os.makedirs(item_dir)

with open(f"{item_dir}/items.json", "w+") as item_file:
    json.dump(item_data, item_file, ensure_ascii=False)

# sum_spell_res = requests.get(sum_spell_url)
# sum_spells = sum_spell_res.json()
