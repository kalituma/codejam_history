#
# Created by khw on 21. 3. 3..
#

"""
 * You are a friendly dragon fighting to protect your lair from a greedy knight!
 * You have Hd health points and an attack power of Ad, and the knight has Hk health points and an attack power of Ak.
 * If your health drops to 0 or below at any point;
 * you are knocked out and you instantly lose; if the knight's health drops to 0 or below at any point, the knight is knocked out and you win!
 *
 * You will battle the knight in a series of turns. On each turn, you go first, and you can choose and execute any one of the following actions.
 *
 * - Attack: Reduce the opponent's health by your own attack power.
 * - Buff: Increase your attack power by B for the rest of the battle.
 * - Cure: Your health becomes Hd.
 * - Debuff: Decrease the opponent's attack power by D for the rest of the battle. If a Debuff would cause the opponent's attack power to become less than 0, it instead sets it to 0.
 *
 * Then, if the knight's health is greater than 0 following your action,
 * the knight will execute an Attack action. After that, the turn ends.
 * (Note that a turn in which you defeat the knight still counts as a turn even though the knight does not get to act.)
 *
 * Note that buffs stack with each other; every buff adds an additional B to your attack power. Similarly, debuffs stack with each other.
 *
 * You would like to defeat the knight as fast as possible (if it is possible)
 * so that you will not be late to help the villagers roast marshmallows at tonight's festival.
 * Can you determine the minimum number of turns in which you can defeat the knight, or that it is IMPOSSIBLE to do so?
"""

"""
 * The first line of the input gives the number of test cases, T. T test cases follow. Each consists of one line with six integers Hd, Ad, Hk, Ak, B, and D, as described above.
"""

"""
 * For each test case, output one line containing Case #x: y,
 * where x is the test case number (starting from 1) and y is either IMPOSSIBLE if it is not possible to defeat the knight,
 * or the minimum number of turns needed to defeat the knight.
 """

"""
 * Memory limit: 1 GB.
 * 1 ≤ T ≤ 100.
 * Small dataset (Test Set 1 - Visible)
 * Time limit: 60 seconds.
 * 1 ≤ Hd ≤ 100.
 * 1 ≤ Ad ≤ 100.
 * 1 ≤ Hk ≤ 100.
 * 1 ≤ Ak ≤ 100.
 * 0 ≤ B ≤ 100.
 * 0 ≤ D ≤ 100.
 *
 * Large dataset (Test Set 2 - Hidden)
 * Time limit: 240 seconds.
 * 1 ≤ Hd ≤ 10^9.
 * 1 ≤ Ad ≤ 10^9.
 * 1 ≤ Hk ≤ 10^9.
 * 1 ≤ Ak ≤ 10^9.
 * 0 ≤ B ≤ 10^9.
 * 0 ≤ D ≤ 10^9.
 """

"""
 * Input
    4
    11 5 16 5 0 0
    3 1 3 2 2 0
    3 1 3 2 1 0
    2 1 5 1 1 1
 """

"""
 * Output
    Case #1: 5
    Case #2: 2
    Case #3: IMPOSSIBLE
    Case #4: 5
 """

"""
 * In Case #1, you have 11 health and 5 attack, and the knight has 16 health and 5 attack. One possible optimal sequence of actions is:
 *
 * Turn 1: Attack, reducing the knight's health to 11. Then the knight attacks and reduces your health to 6.
 * Turn 2: Attack, reducing the knight's health to 6. Then the knight attacks and reduces your health to 1.
 * Turn 3: Cure, restoring your health to 11. Then the knight attacks and reduces your health to 6.
 * (If you had attacked instead this turn, the knight's next attack would have caused you to lose.)
 * Turn 4: Attack, reducing the knight's health to 1. Then the knight attacks and reduces your health to 1.
 * Turn 5: Attack, reducing the knight's health to -4. You instantly win and the knight does not get another attack.
 *
 * In Case #2, one possible optimal sequence of actions is:
 *
 * Turn 1: Buff, increasing your attack power to 3. Then the knight attacks and reduces your health to 1.
 * Turn 2: Attack, reducing the knight's health to 0. You instantly win and the knight does not get another attack.
 * In Case #3, the knight only needs two attacks to defeat you, and you cannot do enough damage fast enough to defeat the knight.
 * You can indefinitely extend the combat by executing the Cure action after every attack, but it is impossible to actually defeat the knight.
 *
 * In Case #4, one possible optimal sequence of actions is: Attack, Debuff, Buff, Attack, Attack.
 """

# code from https://github.com/iwataka/google-code-jam/blob/master/2017/round1a/play_the_dragon.py
import math


def solve(Hd, Ad, Hk, Ak, B, D):
    """Calculates the minimum number of turns to beat the knight.
    Args:
        Hd: the dragon's health.
        Ad: the dragon's attack.
        Hk: the knight's health.
        Ak: the knight's attack.
        B: buff value.
        D: debuff value.

    Returns:
        The minimum number of turns to beat the knight.
        None if the dragon can't beat the knight.
    """
    # The dragon can't beat the knight because the dragon's attack is 0.
    if Ad == 0:
        return None
    # The dragon can beat the knight in just 1 turn.
    if Hk <= Ad:
        return 1
    # The dragon will be beaten in just 1 turn even if debuffing the knight.
    if Hd <= Ak - D:
        return None
    #
    if Hk <= 2 * Ad or Hk <= Ad + B:
        return 2
    #
    if Hd <= 2 * Ak - 3 * D:
        return None

    n_turns_for_attacks_and_buffs = optimize_attacks_and_buffs(Ad, Hk, B)
    return optimize(Hd, Ak, D, n_turns_for_attacks_and_buffs)


def optimize_attacks_and_buffs(Ad, Hk, B):
    """Calculates the minimum numbers of turns taken only for attacks and buffs.
    It is known that the number of turns taken for attacks and buffs decreases
    in proportion to the number of buffs until certain point and then increases.
    Args:
        Ad: the dragon's attack.
        Hk: the knight's health.
        B: buff value
    Returns:
        The minimum number of turns taken only for attacks and buffs
        until the knight's health drops to 0.
    """
    n_buffs = 0
    min_n_turns = None
    while True:
        Ad_after_buffs = Ad + B * n_buffs
        n_attacks = math.ceil(Hk / Ad_after_buffs)
        n_turns = n_buffs + n_attacks
        if min_n_turns == None or min_n_turns > n_turns:
            min_n_turns = n_turns
        else:
            break
        n_buffs += 1
    return min_n_turns


def optimize(Hd, Ak, D, n_turns_for_attacks_and_buffs):
    """Calculates the minimum number of turns taken to beat the knight.
    Args:
        Hd: the dragon's health.
        Ak: the knight's attack.
        D: debuff value.
        n_turns_for_attacks_and_buffs: the minimum number of turns taken for attacks and buffs.
    Returns:
        The minimum number of turns taken to beat the knight
    """
    # No meanings to debuff at all.
    if D == 0:
        return optimize_cures(Hd, Hd, Ak, n_turns_for_attacks_and_buffs)

    Hd_orig = Hd
    n_turns_for_debuffs_and_cures = 0
    max_interval_between_cures = 0
    min_n_turns = math.pow(10, 9) * 2

    # TODO: Make this loop more performant
    while True:
        # No meanings to debuff any more.
        if Ak == 0:
            n_turns = n_turns_for_debuffs_and_cures + n_turns_for_attacks_and_buffs
            return min(min_n_turns, n_turns)

        interval_between_cures = math.ceil(Hd_orig / Ak) - 2
        # Calculates the total number of turns if required.
        if interval_between_cures > max_interval_between_cures:
            max_interval_between_cures = interval_between_cures
            n_turns = n_turns_for_debuffs_and_cures + optimize_cures(Hd, Hd_orig, Ak, n_turns_for_attacks_and_buffs)
            min_n_turns = min(min_n_turns, n_turns)

        # Cure if needed.
        if Hd <= Ak - D:
            Hd = Hd_orig - Ak
            n_turns_for_debuffs_and_cures += 1

        # Debuff.
        Ak = max(0, Ak - D)
        Hd -= Ak
        n_turns_for_debuffs_and_cures += 1

    return min_n_turns


def optimize_cures(Hd, Hd_orig, Ak, n_turns_for_attacks_and_buffs):
    """
    Args:
        Hd: the current dragon's health
        Hd_orig: the original dragon's health
        Ak: the knight's attack
        n_turns_for_attacks_and_buffs: the minimum number of turns taken for attacks and buffs
    """
    n_turns_until_first_attacks = math.ceil(Hd / Ak) - 1
    if n_turns_until_first_attacks + 1 >= n_turns_for_attacks_and_buffs:
        return n_turns_for_attacks_and_buffs
    interval = math.ceil(Hd_orig / Ak) - 2
    if interval == 0:
        return math.pow(10, 9) * 2
    n_intervals = math.floor((n_turns_for_attacks_and_buffs - n_turns_until_first_attacks) / interval)
    if interval == 1:
        return n_turns_until_first_attacks + (interval + 1) * (n_intervals - 1) + 1
    mod = (n_turns_for_attacks_and_buffs - n_turns_until_first_attacks) % interval
    if mod == 1:
        return n_turns_until_first_attacks + (interval + 1) * n_intervals + 1
    elif mod == 0:
        return n_turns_until_first_attacks + (interval + 1) * n_intervals
    else:
        return n_turns_until_first_attacks + (interval + 1) * n_intervals + 1 + mod


if __name__ == '__main__':
    for i in range(int(input())):
        Hd, Ad, Hk, Ak, B, D = [int(x) for x in input().split(" ")]
        ans = solve(Hd, Ad, Hk, Ak, B, D)
        if ans == None:
            print("Case #%d: %s" % (i + 1, "IMPOSSIBLE"))
        else:
            print("Case #%d: %d" % (i + 1, ans))
