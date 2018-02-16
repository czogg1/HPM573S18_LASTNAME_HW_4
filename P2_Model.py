from enum import Enum
import numpy as np

class HorT(Enum):
    """result of the coin flip"""
    HEAD = 0
    TAIL = 1


class Game(object):
    """running the 20 flip game, single player"""
    def __init__(self, id, head_prob):
        self._id = id                                       # Player number
        self._headProb = head_prob                          # Probability H
        self._HorT = HorT.HEAD                              # Default start H, meaningless

        self._TCount = 0                                    # T count, starts at zero
        self._WinCount = 0                                  # Win count, starts at zero
        self._TotalFlips = 20                               # 20 flips per game
        self._FlipCount = 1                                 # Flip count, starts at one

        self._rnd = np.random                               # Declaring random number generator, will be changed
        self._rnd.seed(self._id * self._FlipCount)          # Repeatable seed of random number generator for flip


    def flip_advance(self):
        # If the prior toss was T
        if self._HorT == HorT.TAIL:
            # determine if the toss was H during this time-step
            if self._rnd.random_sample() < self._headProb:
                if self._TCount >= 2:
                    self._WinCount += 1                     # If T-->H follows ≥2T, update win count
                self._HorT = HorT.HEAD                      # Change status to H
                self._TCount = 0                            # Reset T count

            # determine if the toss was T during this time-step
            if self._rnd.random_sample() > self._headProb:
                self._HorT = HorT.TAIL                      # Keep status T (could delete)
                self._TCount += 1                           # Update T count

        # If the prior toss was H                           # First pass defaults here
        if self._HorT == HorT.HEAD:
            # determine if the toss was H during this time-step
            if self._rnd.random_sample() < self._headProb:
                self._HorT = HorT.HEAD                      # Keep status H (could delete)
                self._TCount = 0                            # Reset T count (could delete, already 0)

            # determine if the toss was T during this time-step
            if self._rnd.random_sample() > self._headProb:
                self._HorT = HorT.TAIL                      # Change status to H
                self._TCount = 1                            # Update T count to 1

        self._FlipCount += 1                                # Update flip count


    def run_game(self):
        for i in range(1, self._TotalFlips+1):              # Game of 20 tosses
            self._rnd = np.random
            self._rnd.seed(self._id * self._FlipCount)

            self.flip_advance()


    def game_reward(self):
        self.run_game()                                     # Call run game

        self._reward = -250                                 # Ticket price
        self._reward += 100*self._WinCount                  # Update with winnings

        return self._reward


# Testing with single player
#TestSubject = Game(id=120, head_prob=0.5)
#print(TestSubject.game_reward())


# Defining the simulation cohort
class Cohort:
    def __init__(self, id, pop_size, head_prob):
        """ define the cohort

        :param id: Cohort identifier
        :param pop_size: Number of players
        :param head_prob: Probability H """

        self._players = []                                  # List of players
        n = 1                                               # Current population

        while n <= pop_size:
            # create new player (use id * pop_size + n as patient id)
            player = Game(id=id * pop_size + n, head_prob=head_prob)

            self._players.append(player)                    # Add player to cohort
            n += 1                                          # Increase cohort population size


    def simulate(self):
        """ run sumulation on cohort """
        game_rewards = []                                   # List of simulated game rewards

        for player in self._players:                        # Run game for all players, add to list
            game_rewards.append(player.game_reward())

        return sum(game_rewards)/len(game_rewards)          # Return average game reward



# Testing cohort
TestCohort = Cohort(id=1, pop_size=1000, head_prob=0.5)
print('Average game reward in dollars:', TestCohort.simulate())

TestCohort = Cohort(id=2, pop_size=1000, head_prob=0.5)
print('Average game reward in dollars:', TestCohort.simulate())
