headers = {
    "Origin": "https://developer.riotgames.com",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Riot-Token": "RGAPI-dea3d63b-9791-4e6a-93fd-1954343061a1",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
}

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
# http://ddragon.leagueoflegends.com/cdn/9.9.1/data/en_US/champion/Neeko.json

import json
import requests
import time
import os

TIER = [
    "IRON",
    "BRONZE",
    "SILVER",
    "GOLD",
    "PLATINUM",
    "DIAMOND",
    "MASTER",
    "GRANDMASTER",
    "CHALLENGER",
]

RANK = ["I", "II", "III", "IV", "V"]

active_player_tier_index = TIER.index("GOLD")
active_player_rank_index = RANK.index("IV")
active_player_points = 20


def write_to_file(filename, content):
    print(f"{filename} {content}")
    with open(f"{filename}.txt", "a+") as file:
        file.write(f"{content},")


def inspect_match_history_data(match_history):
    matches = match_history["matches"]

    for match in matches:
        start = time.time()
        if match["queue"] == 420:
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
                                with open("bad_reqest.log", "a+") as br_log:
                                    br_log.write(
                                        f"cant get {challenger_name} data: {rs.headers}"
                                    )

                            res = rs.json()

                            if not res:
                                print(f"{challenger_name} req response")
                                print(challenger_name)
                                print(res)
                                continue

                            if "id" not in res:
                                print(
                                    f"{challenger_name} req response with no id"
                                )
                                print(res)
                                continue

                            if "message" in res:
                                print(
                                    f"{challenger_name} req response with no message"
                                )
                                print(res)
                                if (
                                    res["status"]["message"]
                                    == "Data not found - summoner not found"
                                ):
                                    with open(
                                        "removed_accounts.txt", "a+"
                                    ) as ra_txt:
                                        ra_txt.write(challenger_name)
                            else:
                                with open(
                                    f"{directory}/account_info.json", "a+"
                                ) as f:
                                    f.write(json.dumps(res))

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
                                print(f"cant get {challenger_name} queue data")
                                print(ress)
                                continue

                            if "leagueId" not in ress[0]:
                                print(f"cant get {challenger_name} queue data")
                                print("no leagueID")
                                print(challenger_name)
                                continue

                            with open(
                                f"{directory}/queue_info.json", "a+"
                            ) as f:
                                f.write(json.dumps(ress))

                            # we are storing account info and queue info for each challenger summoner
                            # TODO: build out a report, broken down by role and providing insight into their teir, rank, points, win rate, wins and losses

                            for queue in ress:
                                if "queueType" in queue:
                                    if queue["queueType"] == "RANKED_SOLO_5x5":
                                        tier = queue["tier"]
                                        rank = queue["rank"]
                                        points = queue["leaguePoints"]
                                        challenger_player_tier_index = TIER.index(
                                            tier
                                        )
                                        challenger_player_rank_index = RANK.index(
                                            rank
                                        )

                                        challenger_rank = f"{challenger_name} {tier} {rank} {points}"

                                        if (
                                            challenger_player_tier_index
                                            > active_player_tier_index
                                        ):
                                            # TODO plyaer better than me
                                            write_to_file(
                                                "better", challenger_rank
                                            )
                                            continue

                                        if (
                                            challenger_player_tier_index
                                            < active_player_tier_index
                                        ):
                                            # TODO player is worse
                                            write_to_file(
                                                "worse", challenger_rank
                                            )
                                            continue

                                        if (
                                            challenger_player_tier_index
                                            == active_player_tier_index
                                        ):
                                            # # TODO player at same rank
                                            # write_to_file(
                                            #     "same", challenger_rank
                                            # )

                                            if (
                                                challenger_player_rank_index
                                                > active_player_rank_index
                                            ):
                                                # TODO player better than me
                                                write_to_file(
                                                    "worse", challenger_rank
                                                )
                                            elif (
                                                challenger_player_rank_index
                                                < active_player_rank_index
                                            ):
                                                # TODO player worse than me
                                                write_to_file(
                                                    "better", challenger_rank
                                                )
                                            else:
                                                # TODO player is the same as me
                                                # write_to_file(
                                                #     "same", challenger_rank
                                                # )
                                                if (
                                                    active_player_points
                                                    > points
                                                ):
                                                    # TODO better player
                                                    write_to_file(
                                                        "worse", challenger_rank
                                                    )
                                                elif (
                                                    active_player_points
                                                    < points
                                                ):
                                                    # TODO worse player
                                                    write_to_file(
                                                        "better",
                                                        challenger_rank,
                                                    )
                                                else:
                                                    # TODO same
                                                    write_to_file(
                                                        "same", challenger_rank
                                                    )

        time.sleep(4)
        end_time = time.time()
        print(f"completed time: {end_time - start}")


with open("match_list.json") as f:
    inspect_match_history_data(json.load(f))

