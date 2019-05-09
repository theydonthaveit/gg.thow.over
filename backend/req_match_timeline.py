import requests
from bad_reqs import dump_bad_req, dump_no_response, dump_account_banned


def get_timeline_info(game_id, headers):
    match_timeline_req = f"https://euw1.api.riotgames.com/lol/match/v4/timelines/by-match/{game_id}"

    req = requests.get(match_timeline_req, headers=headers)

    if not req.ok:
        dump_bad_req(req.json())

    res = req.json()

    if not res:
        dump_no_response(res)

    if len(res) < 1:
        dump_account_banned(res)

    return res
