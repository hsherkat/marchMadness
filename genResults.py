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
    CP = [0] * 63
    PA = [0] * 63
    game_results = get_game_results()

    for i in range(len(game_results)):
        gameV = game_results[i].split()
        CP[int(gameV[0]) - 1] = int(gameV[1])
        PA[int(gameV[0]) - 1] = int(gameV[2])

    #  Read the user brackets
    scores, userNames, userPicks = read_user_brackets()

    # Determine results
    fh = open("userResultsPy.dat", "w")
    scoreFile = open("userScores.dat", "w")
    for ii in range(len(userPicks)):
        score = 0
        # 0 = no result, 1 = correct, 2 = incorrect
        returnS = [0] * 63
        myP = userPicks[ii]
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
        scores[userNames[ii]] = score
        fh.write("".join(returnS) + "\n")
    fh.close()
    for teamValPair in sorted(scores.items(), key=operator.itemgetter(1), reverse=True):
        scoreFile.write(
            teamValPair[0] + " with " + str(teamValPair[1]) + " points" + "\n"
        )
    scoreFile.close()


def get_game_results():
    fh = open("gameResults.dat", "r")
    flines = fh.read().splitlines()
    fh.close()
    return flines


if __name__ == "__main__":
    main()
