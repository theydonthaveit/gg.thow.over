        start_time = time.time()
        summoner_name = participant.get("player").get("summonerName")

        summoner_details = get_summoner_details(summoner_name, headers)
        encrypted_summoner_id = summoner_details.get("id")
        account_id = summoner_details.get("accountId")

        player_directory = os.path.join(base_directory, name)
        player_directory_exists = os.path.exists(player_directory)

        if not player_directory_exists:
            os.makedirs(player_directory)

        try:
            with open(
                f"{player_directory}/summoner_info.json", "w"
            ) as summoner_info_file:
                json.dump(
                    summoner_details, summoner_info_file, ensure_ascii=False
                )
        except Exception as e:
            print(e)

        queue_data = get_queue_details(encrypted_summoner_id, headers)

        try:
            with open(
                f"{player_directory}/queue_info.json", "w"
            ) as queue_info_file:
                json.dump(queue_data, queue_info_file, ensure_ascii=False)
        except Exception as e:
            print(e)

        match_list_data = get_match_list(account_id, headers)

        try:
            with open(
                f"{player_directory}/match_list.json", "w"
            ) as match_list_file:
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
            start_time = time.time()
            game_id = match.get("gameId", None)

            if not game_id:
                dump_bad_req({"bad_match": match})
                continue

            match_info_data = get_match_info(game_id, headers)

            try:
                with open(
                    f"{match_directory}/{game_id}.json", "w"
                ) as match_info_file:
                    json.dump(
                        match_info_data, match_info_file, ensure_ascii=False
                    )
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

