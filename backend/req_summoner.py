import requests
from bad_reqs import dump_bad_req, dump_no_response, dump_account_banned


def get_summoner_details(name, headers):
    summoner_name_req = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}"

    req = requests.get(summoner_name_req, headers=headers)

    if not req.ok:
        dump_bad_req(req.json())
        return

    res = req.json()

    if not res:
        dump_no_response(res)
        return

    if "accountId" not in res:
        dump_account_banned(res)
        return

    return res
