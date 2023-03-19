################################################################################
#                                                                              #
#  Name:         Michael Kasa                                                  #
#  Date:         20 March 2016                                                 #
#  File:         genResults.py                                                 #
#  Description:  This function reads the game results from gameResults.dat     #
#                  and the user brackets from userbrackets.dat and determines  #
#                  which picks were correct and how many points were scored.   #
#                  These results are saved in userResultsPy.dat and            #
#                  userScores.dat, respectively.                               #
#                                                                              #
################################################################################

import operator


def main():
    game_results = get_game_results()
    correct_picks, points_available = generate_picks_and_points(game_results)

    user_names, user_picks = read_user_brackets()
    scores = determine_results(correct_picks, points_available, user_names, user_picks)
    write_results(scores)


def generate_picks_and_points(game_results):
    correct_picks = [0] * 63
    points_available = [0] * 63
    for game in game_results:
        idx, pick, points = map(int, game.split())
        correct_picks[idx - 1] = int(pick)
        points_available[idx - 1] = int(points)
    return correct_picks, points_available


def write_results(scores):
    with open("userScores.dat", "w") as score_file:
        for team, val in sorted(scores.items(), key=operator.itemgetter(1), reverse=True):
            score_file.write(
                f"{team} with {val} points\n"
            )


def determine_results(correct_picks, points_available, user_names, user_picks):
    scores = {}

    with open("userResultsPy.dat", "w") as fh:
        for user, picks in zip(user_names, user_picks):
            # 0 = no result, 1 = correct, 2 = incorrect
            returnS = process_picks(correct_picks, picks)
            scores[user] = calculate_score(points_available, returnS)

            fh.write("".join(map(str, returnS)) + "\n")

    return scores


def process_picks(correct_picks, picks):
    returnS = [0] * 63
    for game_idx in range(63, 0, -1):
        if correct_picks[game_idx - 1] > 0:
            # Wrong pick
            if correct_picks[game_idx - 1] != float(picks[game_idx - 1]):
                returnS[game_idx - 1] = 2
            # Right pick in the first round
            elif game_idx > 31:
                returnS[game_idx - 1] = 1
            # Second round or later
            else:
                # Only correct if the user also match in the earlier round
                if returnS[2 * game_idx + correct_picks[game_idx - 1] - 2] == 1:
                    returnS[game_idx - 1] = 1
                else:
                    returnS[game_idx - 1] = 2
    return returnS


def calculate_score(points_available, returnS):
    return sum((retS % 2) * points for retS, points in zip(returnS, points_available))


def read_user_brackets():
    with open("userbrackets.dat", "r") as fh:
        game_results = fh.read().splitlines()
    user_names = game_results[::2]
    user_picks = game_results[1::2]
    return user_names, user_picks


def get_game_results():
    with open("gameResults.dat", "r") as fh:
        flines = fh.readlines()
    return flines


if __name__ == "__main__":
    main()
