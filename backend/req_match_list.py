import requests
from bad_reqs import dump_bad_req, dump_no_response, dump_account_banned


def get_match_list(account_id, headers):
    match_list_req = f"https://euw1.api.riotgames.com/lol/match/v4/matchlists/by-account/{account_id}"

    req = requests.get(match_list_req, headers=headers)

    if not req.ok:
        dump_bad_req(req.json())

    res = req.json()

    if not res:
        dump_no_response(res)

    if len(res) < 1:
        dump_account_banned(res)

    match_list_data = res.get("matches", [])
    return match_list_data
