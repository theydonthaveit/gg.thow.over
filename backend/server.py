headers = {
    "Origin": "https://developer.riotgames.com",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Riot-Token": "RGAPI-bbd48856-4684-490c-bac3-3a3117f40cf7",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
}

# summoner_name = "meow side"
# summoner_name_req = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"


# encrypted_summoner_id = "90TymNod-aPQ7a_EiDpxjB2M7RH81zhmFc5vuPt0Jwnd1g6E"
# queue_req = f"https://euw1.api.riotgames.com/lol/league/v4/positions/by-summoner/{encrypted_summoner_id}"


# encrypted_account_id = "GpTD1kU8ZmL6GtlaoEvqCsaKv5lCHKfwHI2SQs9YbpK_yU8"
# match_list_req = f"https://euw1.api.riotgames.com/lol/match/v4/matchlists/by-account/{encrypted_account_id}"


# game_id = "3980344653"
# match_info_req = (
#     f"https://euw1.api.riotgames.com/lol/match/v4/matches/{game_id}"
# )
# match_timeline_req = (
#     f"https://euw1.api.riotgames.com/lol/match/v4/timelines/by-match/{game_id}"
# )

# items_data = (
#     "http://ddragon.leagueoflegends.com/cdn/6.24.1/data/en_US/item.json"
# )
# mastery_data = (
#     "http://ddragon.leagueoflegends.com/cdn/6.24.1/data/en_US/mastery.json"
# )
# rune_data = "http://ddragon.leagueoflegends.com/cdn/6.24.1/data/en_US/rune.json"
# summoner_spell_data = (
#     "http://ddragon.leagueoflegends.com/cdn/6.24.1/data/en_US/summoner.json"
# )
# profile_icon_data = (
#     "http://ddragon.leagueoflegends.com/cdn/6.24.1/data/en_US/profileicon.json"
# )
# champion_data = (
#     "http://ddragon.leagueoflegends.com/cdn/6.24.1/data/en_US/champion.json"
# )

import json
import requests
import time
import os


def inspect_match_history_data(match_history):
    matches = match_history["matches"]

    for match in matches:
        start = time.time()
        if match["queue"] == 420:
            print(match["gameId"])
            lane = match["lane"]
            champ = match["champion"]
            role = match["role"]
            game_id = match["gameId"]
            r = requests.get(
                f"https://euw1.api.riotgames.com/lol/match/v4/matches/{game_id}",
                headers=headers,
            )

            if not r.ok:
                print("req bad")

            res = r.json()

            if not res:
                continue

            if res["gameDuration"] > 600:
                participants = res["participants"]
                players = []

                for participant in participants:
                    if (
                        participant["timeline"]["lane"] == lane
                        and participant["timeline"]["role"] == role
                    ):
                        players.append(participant["timeline"]["participantId"])

                participantMeta = res["participantIdentities"]

                for meta in participantMeta:
                    if meta["participantId"] in players:
                        if meta["player"]["summonerName"] != "meow side":
                            challenger_name = meta["player"]["summonerName"]
                            directory = f"challengers/{challenger_name}"
                            if not os.path.exists(directory):
                                os.makedirs(directory)

                            # we are at the point where we are retrieving the challenger summoner name i.e. the player we are facing and creating a directory for their data
                            # TODO: retrieve info and queue data about the challenger

                            rs = requests.get(
                                f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{challenger_name}",
                                headers=headers,
                            )

                            if not rs.ok:
                                print(f"cant get {challenger_name} data")
                                print(rs.headers)

                            res = rs.json()
                            with open(
                                f"{directory}/account_info.json", "a+"
                            ) as f:
                                f.write(json.dumps(res))

                            if not res:
                                print(challenger_name)
                                continue

                            if "id" not in res:
                                print(challenger_name)
                                continue

                            encrypted_summoner_id = res["id"]
                            rr = requests.get(
                                f"https://euw1.api.riotgames.com/lol/league/v4/positions/by-summoner/{encrypted_summoner_id}",
                                headers=headers,
                            )

                            if not rr.ok:
                                print(f"cant get {challenger_name} queue data")
                                print(rr.headers)

                            ress = rr.json()

                            if not ress:
                                print(challenger_name)
                                continue

                            if "leagueId" not in ress[0]:
                                print(challenger_name)
                                continue

                            with open(
                                f"{directory}/queue_info.json", "a+"
                            ) as f:
                                f.write(json.dumps(ress))

                            # we are storing account info and queue info for each challenger summoner
                            # TODO: build out a report, broken down by role and providing insight into their teir, rank, points, win rate, wins and losses
        time.sleep(3)
        end_time = time.time()
        print(f"completed time: {end_time - start}")


with open("match_list.json") as f:
    inspect_match_history_data(json.load(f))
