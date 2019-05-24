import requests
import os
import json
import time
import arrow


def write_to_file(file_type, response, summoner_name, game_id=None):
    utc = arrow.utcnow()
    local = utc.to("Europe/London")

    player_directory = os.path.join("players", f"{summoner_name}")
    player_directory_exists = os.path.exists(player_directory)

    if not player_directory_exists:
        os.makedirs(player_directory)

    if file_type == "summoner_details":
        write_to_summoner_file(player_directory, response, local)
    elif file_type == "queue_details":
        write_to_queue_file(player_directory, response, local)
    elif file_type == "match_list":
        write_to_match_list_file(player_directory, response, local)
    elif file_type == "match_details":
        write_to_match_details_file(player_directory, response, local, game_id)
    elif file_type == "match_timeline":
        write_to_match_timeline_file(player_directory, response, local, game_id)


def write_to_summoner_file(player_directory, response, local):
    summoner_info = os.path.join(f"{player_directory}", "summoner_info.json")
    summoner_info_exists = os.path.isfile(summoner_info)

    if summoner_info_exists:
        data = {}
        with open(f"{summoner_info}", "r") as summoner_file:
            data = json.load(summoner_file)
            summoner_file.close()

        with open(f"{summoner_info}", "w") as summoner_file:
            data.update({"lastUpdated": local.timestamp})
            json.dump(data, summoner_file, ensure_ascii=False)
            summoner_file.close()
    else:
        with open(f"{summoner_info}", "w") as summoner_file:
            response.update({"createdAt": local.timestamp})
            json.dump(response, summoner_file, ensure_ascii=False)
            summoner_file.close()


def write_to_match_list_file(player_directory, response, local):
    match_list = os.path.join(f"{player_directory}", "match_list.json")
    match_list_exists = os.path.isfile(match_list)

    if match_list_exists:
        data = {}
        with open(f"{match_list}", "r") as match_list_file:
            data = json.load(match_list_file)
            match_list_file.close()

        with open(f"{match_list}", "w") as match_list_file:
            json.dump(data, match_list_file, ensure_ascii=False)
            match_list_file.close()
    else:
        with open(f"{match_list}", "w") as match_list_file:
            json.dump(response, match_list_file, ensure_ascii=False)
            match_list_file.close()


def write_to_queue_file(player_directory, response, local):
    queue_info = os.path.join(f"{player_directory}", "queue_info.json")
    queue_info_exists = os.path.isfile(queue_info)

    if queue_info_exists:
        data = {}
        with open(f"{queue_info}", "r") as queue_file:
            data = json.load(queue_file)
            queue_file.close()

        with open(f"{queue_info}", "w") as queue_file:
            json.dump(data, queue_file, ensure_ascii=False)
            queue_file.close()
    else:
        with open(f"{queue_info}", "w") as queue_file:
            json.dump(response, queue_file, ensure_ascii=False)
            queue_file.close()


def write_to_match_details_file(player_directory, response, local, game_id):
    match_dir = os.path.join(f"{player_directory}", "matches")

    if not os.path.exists(match_dir):
        os.makedirs(match_dir)

    match_details = os.path.join(
        f"{player_directory}", "matches", f"{game_id}.json"
    )
    queue_info_exists = os.path.isfile(match_details)

    if queue_info_exists:
        data = {}
        with open(f"{match_details}", "r") as queue_file:
            data = json.load(queue_file)
            queue_file.close()

        with open(f"{match_details}", "w") as queue_file:
            json.dump(data, queue_file, ensure_ascii=False)
            queue_file.close()
    else:
        with open(f"{match_details}", "w") as queue_file:
            json.dump(response, queue_file, ensure_ascii=False)
            queue_file.close()


def write_to_match_timeline_file(player_directory, response, local, game_id):
    timeline_dir = os.path.join(f"{player_directory}", "timeline")

    if not os.path.exists(timeline_dir):
        os.makedirs(timeline_dir)

    timeline = os.path.join(
        f"{player_directory}", "timeline", f"{game_id}.json"
    )
    timeline_exists = os.path.isfile(timeline)

    if timeline_exists:
        data = {}
        with open(f"{timeline}", "r") as queue_file:
            data = json.load(queue_file)
            queue_file.close()

        with open(f"{timeline}", "w") as queue_file:
            json.dump(data, queue_file, ensure_ascii=False)
            queue_file.close()
    else:
        with open(f"{timeline}", "w") as queue_file:
            json.dump(response, queue_file, ensure_ascii=False)
            queue_file.close()


def log_to_file(file_type, response=None, summoner_name=None):
    log_directory = os.path.join("logs", f"{file_type}.json")
    log_exists = os.path.isfile(log_directory)

    if log_exists:
        data = []
        with open(f"{log_directory}", "r") as log:
            data = json.load(log)
            data.append(response or summoner_name)
            log.close()

        with open(f"{log_directory}", "w") as log:
            json.dump(data, log, ensure_ascii=False)
            log.close()
    else:
        with open(f"{log_directory}", "w") as log:
            data = response or summoner_name
            json.dump([data], log, ensure_ascii=False)
            log.close()


class HTTPResponse:
    def __init__(self, response, summoner_name):
        self.response = response
        self.summoner_name = summoner_name
        self.main()

    def main(self):
        if self.response.ok:
            return True

        response = self.response.json()
        status_code = response.get("status").get("status_code")

        if status_code:
            if status_code == 400:
                # bad requests
                log_to_file(
                    file_type="bad_request", summoner_name=self.summoner_name
                )
                return False
            elif status_code == 401:
                # notification
                # unauth
                log_to_file(file_type="unauthorized", response=response)
                return False
            elif status_code == 403:
                # notification
                # forbidden
                log_to_file(file_type="forbidden", response=response)
                return False
            elif status_code == 404:
                # data not found
                log_to_file(
                    file_type="banned", summoner_name=self.summoner_name
                )
                return False
            elif status_code == 429:
                # notification
                # rate exceed
                log_to_file(file_type="rate_exceed")
                return False
            elif status_code == 503:
                # notification
                # service unavailable
                log_to_file(file_type="service_unavailable")
                return False
            elif status_code != 200:
                # everything else
                log_to_file(file_type="general", response=response)
                return False


class User:
    dbh = None
    url = None
    response = None
    match_ids = []
    account_id = None
    summoner_name = None
    encrypted_summoner_id = None

    def __init__(self, summoner_name):
        self.summoner_name = summoner_name
        self.headers = {
            "Origin": "https://developer.riotgames.com",
            "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Riot-Token": "RGAPI-1bd6cba8-cd27-4d4c-9846-ca46c0122bab",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        }

    def __enter__(self):
        # DB init: self.dbh = database
        self.main()
        pass

    def __exit__(self, exception_type, exception_value, traceback):
        # Handle class exit
        pass

    def make_request(self):
        response = requests.get(self.url, headers=self.headers)
        if HTTPResponse(response, self.summoner_name):
            self.response = response.json()

    def set_url(self, url):
        self.url = url

    def clear_url(self):
        self.url = None

    def store_summoner_details(self, file_type, summoner_name):
        write_to_file(
            file_type=file_type,
            response=self.response,
            summoner_name=summoner_name,
        )

    def store_queue_details(self, file_type, summoner_name):
        write_to_file(
            file_type=file_type,
            response=self.response,
            summoner_name=summoner_name,
        )

    def store_match_list(self, file_type, summoner_name):
        write_to_file(
            file_type=file_type,
            response=self.response,
            summoner_name=summoner_name,
        )

    def store_match_details(self, file_type, summoner_name, game_id):
        write_to_file(
            file_type=file_type,
            response=self.response,
            summoner_name=summoner_name,
            game_id=game_id,
        )

    def store_match_timeline(self, file_type, summoner_name, game_id):
        write_to_file(
            file_type=file_type,
            response=self.response,
            summoner_name=summoner_name,
            game_id=game_id,
        )

    def get_summoner_details(self):
        url = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{self.summoner_name}"
        self.set_url(url)
        self.make_request()
        self.store_summoner_details("summoner_details", self.summoner_name)
        self.encrypted_summoner_id = self.response.get("id")
        self.account_id = self.response.get("accountId")

    def get_queue_details(self):
        url = f"https://euw1.api.riotgames.com/lol/league/v4/positions/by-summoner/{self.encrypted_summoner_id}"
        self.set_url(url)
        self.make_request()
        self.store_summoner_details("queue_details", self.summoner_name)

    def get_match_list(self):
        url = f"https://euw1.api.riotgames.com/lol/match/v4/matchlists/by-account/{self.account_id}?season=13"
        self.set_url(url)
        self.make_request()
        self.store_match_list("match_list", self.summoner_name)
        time.sleep(2.4)

        if self.summoner_name == "meow side":
            for match in self.response.get("matches"):
                self.get_match_details(match.get("gameId"))
                self.get_match_timeline(match.get("gameId"))

    def get_match_details(self, game_id):
        url = f"https://euw1.api.riotgames.com/lol/match/v4/matches/{game_id}"

        self.set_url(url)
        self.make_request()
        self.store_match_details("match_details", self.summoner_name, game_id)

    def get_match_timeline(self, game_id):
        url = f"https://euw1.api.riotgames.com/lol/match/v4/timelines/by-match/{game_id}"

        self.set_url(url)
        self.make_request()
        self.store_match_timeline("match_timeline", self.summoner_name, game_id)
        time.sleep(3.4)

    def main(self):
        self.get_summoner_details()
        self.get_queue_details()
        self.get_match_list()


if __name__ == "__main__":
    matches = [
        os.path.join(r, file)
        for r, d, f in os.walk(os.path.join("players", "meow side", "matches"))
        for file in f
        if file
    ]

    for match_file in matches:
        print(match_file)
        with open(match_file, "r") as file:
            data = None
            try:
                data = json.load(file)
            except Exception as E:
                print(E)
                continue

            for participant in data.get("participantIdentities"):
                player = participant.get("player").get("summonerName")

                if player == "meow side":
                    continue

                with User(player) as user:
                    user
