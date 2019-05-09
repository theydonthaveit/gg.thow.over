import requests
from bad_reqs import dump_bad_req, dump_no_response, dump_account_banned


# class QueueDetails:
#     def __init__(self, queue_data):
#         self.tier = queue_data["tier"]
#         self.hotStreak = queue_data["hotStreak"]
#         self.wins = queue_data["wins"]
#         self.losses = queue_data["losses"]
#         self.veteran = queue_data["veteran"]
#         self.rank = queue_data["rank"]
#         self.position = queue_data["position"]
#         self.leaguePoints = queue_data["leaguePoints"]


def get_queue_details(encrypted_summoner_id, headers):
    queue_req = f"https://euw1.api.riotgames.com/lol/league/v4/positions/by-summoner/{encrypted_summoner_id}"

    req = requests.get(queue_req, headers=headers)

    if not req.ok:
        dump_bad_req(req.json())

    res = req.json()

    if not res:
        dump_no_response(res)

    if len(res) < 1:
        dump_account_banned(res)

    rank_queue_data = {}
    for queue in res:
        if queue["queueType"] == "RANKED_SOLO_5x5":
            rank_queue_data = queue

    return rank_queue_data
