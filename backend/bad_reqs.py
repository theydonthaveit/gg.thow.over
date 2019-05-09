import os
import json


def dump_bad_req(res):
    with open("bad_requests.json", "a+") as bad_requests:
        json.dump(res, bad_requests, ensure_ascii=False)
        bad_requests.close()


def dump_no_response(res):
    with open("no_response.json", "a+") as no_response:
        json.dump(res, no_response, ensure_ascii=False)
        no_response.close()


def dump_account_banned(res):
    with open("account_banned.json", "a+") as account_banned:
        json.dump(res, account_banned, ensure_ascii=False)
        account_banned.close()
