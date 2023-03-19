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
    #  Load the correct picks (CP) and the points available (PA) into an array.
    #    Remember that the games are 1-indexed, but python arrays are 0-indexed
    game_results = get_game_results()
    correct_picks, points_available = generate_picks_and_points(game_results)

    scores, user_names, user_picks = read_user_brackets()
    determine_results(correct_picks, points_available, scores, user_names, user_picks)
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
    with open("userScores.dat", "w") as scoreFile:
        for team, val in sorted(scores.items(), key=operator.itemgetter(1), reverse=True):
            scoreFile.write(
                team + " with " + str(val) + " points" + "\n"
            )


def determine_results(CP, PA, scores, user_names, user_picks):
    with open("userResultsPy.dat", "w") as fh:
        for ii in range(len(user_picks)):
            score = 0
            # 0 = no result, 1 = correct, 2 = incorrect
            returnS = [0] * 63
            myP = user_picks[ii]
            for iGame in range(63, 0, -1):
                if CP[iGame - 1] > 0:
                    # Wrong pick
                    if CP[iGame - 1] != float(myP[iGame - 1]):
                        returnS[iGame - 1] = 2
                    # Right pick in the first round
                    elif iGame > 31:
                        returnS[iGame - 1] = 1
                    # Second round or later
                    else:
                        # Only correct if the user also match in the earlier round
                        if returnS[2 * iGame + CP[iGame - 1] - 2] == 1:
                            returnS[iGame - 1] = 1
                        else:
                            returnS[iGame - 1] = 2
            for ll in range(len(returnS)):
                score = score + (returnS[ll] % 2) * PA[ll]
                returnS[ll] = str(returnS[ll])
            scores[user_names[ii]] = score
            fh.write("".join(returnS) + "\n")


def read_user_brackets():
    with open("userbrackets.dat", "r") as fh:
        game_results = fh.read().splitlines()
    user_names = []
    user_picks = []
    scores = {}
    print(game_results)
    for ii in range(1, len(game_results), 2):
        user_picks.append(game_results[ii])
    for ii in range(0, len(game_results), 2):
        user_names.append(game_results[ii])
    return scores, user_names, user_picks


def get_game_results():
    with open("gameResults.dat", "r") as fh:
        flines = fh.readlines()
    return flines


if __name__ == "__main__":
    main()
