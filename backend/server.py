import os
import json
import time

from req_summoner import get_summoner_details
from req_queue import get_queue_details
from req_match_list import get_match_list
from req_match_info import get_match_info
from req_match_timeline import get_timeline_info
from req_participant_info import get_participant_info

from bad_reqs import dump_bad_req, played_other

headers = {
    "Origin": "https://developer.riotgames.com",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Riot-Token": "RGAPI-11b31056-0ecb-4b45-9989-fbe925224283",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
}

summoner_details = get_summoner_details("meow side", headers)
print(summoner_details)
encrypted_summoner_id = summoner_details.get("id")
account_id = summoner_details.get("accountId")
name = summoner_details.get("name")

base_directory = "players/"
base_directory_exists = os.path.exists(base_directory)

if not base_directory_exists:
    os.makedirs(base_directory)

player_directory = os.path.join(base_directory, name)
player_directory_exists = os.path.exists(player_directory)

if not player_directory_exists:
    os.makedirs(player_directory)

try:
    with open(
        f"{player_directory}/summoner_info.json", "w"
    ) as summoner_info_file:
        json.dump(summoner_details, summoner_info_file, ensure_ascii=False)
except Exception as e:
    print(e)

queue_data = get_queue_details(encrypted_summoner_id, headers)

try:
    with open(f"{player_directory}/queue_info.json", "w") as queue_info_file:
        json.dump(queue_data, queue_info_file, ensure_ascii=False)
except Exception as e:
    print(e)

match_list_data = get_match_list(account_id, headers)

try:
    with open(f"{player_directory}/match_list.json", "w") as match_list_file:
        json.dump(match_list_data, match_list_file, ensure_ascii=False)
except Exception as e:
    print(e)

match_directory = os.path.join(player_directory, "matches")
match_directory_exists = os.path.exists(match_directory)

timeline_directory = os.path.join(player_directory, "timeline")
timeline_directory_exists = os.path.exists(timeline_directory)

if not match_directory_exists:
    os.makedirs(match_directory)

if not timeline_directory_exists:
    os.makedirs(timeline_directory)

for match in match_list_data:
    game_id = match.get("gameId", None)
    queueId = match.get("queue")

    if queueId == 420:
        match_info_data = get_match_info(game_id, headers)

        try:
            with open(
                f"{match_directory}/{game_id}.json", "w"
            ) as match_info_file:
                json.dump(match_info_data, match_info_file, ensure_ascii=False)
        except Exception as e:
            print(e)

        match_timeline_data = get_timeline_info(game_id, headers)

        try:
            with open(
                f"{timeline_directory}/{game_id}.json", "w"
            ) as timeline_file:
                json.dump(
                    match_timeline_data, timeline_file, ensure_ascii=False
                )
        except Exception as e:
            print(e)

        participant_identities = match_info_data.get("participantIdentities")

        for participant in participant_identities:
            get_participant_info(participant, headers)
    else:
        played_other(queueId, name)
