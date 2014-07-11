import pylab
import random

class Lever:
  def __init__(self, mean, variance):
    self.mean = mean
    self.variance = variance

  def pull(self):
    return random.normalvariate(self.mean, self.variance)

  def __repr__(self):
    return "<lever mean=%s>"%(self.mean)

class BanditProblem:
  @classmethod
  def randomBandit(cls, num_of_levers, mean_variance):
    newLever = lambda : Lever(random.normalvariate(1, mean_variance), 1)
    return cls([newLever() for x in range(num_of_levers)])

  def __init__(self, levers):
    self.levers = levers

  def num_of_levers(self):
    return len(self.levers)

  def pull(self, n):
    return self.levers[n].pull()

  def __repr__(self):
    return "<problem "+"".join(repr(x) for x in self.levers) + "</problem>"

class RLAgent:
  def __init__(self, epsilon):
    self.epsilon = epsilon

  def play(self, problem, time):
    num_of_levers = problem.num_of_levers()

    value_table = [(0, 0)] * num_of_levers


    choices = []
    rewards = []

    for x in range(time):
      # in the future, it would be fun to extend this such that epsilon may
      # depend on stuff which is happening, like the round number or the value table
      if random.random() < self.epsilon(1):
        choice = random.randrange(num_of_levers)
      else:
        choice = max(range(num_of_levers), key=lambda x: value_table[x])

      new_reward = problem.pull(choice)

      previous_average, num_pulls = value_table[choice]
      value_table[choice] = ((previous_average * num_pulls + new_reward) / (num_pulls + 1),
                              num_pulls + 1)

      choices.append(choice)
      rewards.append(new_reward)

    return (choices, rewards)

  # I initially made the mistake of using the same problem every time. Oops.
  def play_repeatedly(self, num_of_levers, time, repeats):
    problem = lambda : BanditProblem.randomBandit(num_of_levers, 1)
    trials = [self.play(problem(), time)[1] for x in range(repeats)]
    results = zip(*trials) # this is crazy bullshit
    return [sum(x) / repeats for x in results]


def different_number_of_arms():
  "In which we discover that more options is better for you"
  r = RLAgent(lambda (x) : 0.1)

  averages = r.play_repeatedly(3, 100, 300)
  pylab.plot(averages, label = "three arms")

  averages = r.play_repeatedly(10, 100, 300)
  pylab.plot(averages, label = "ten arms")

  averages = r.play_repeatedly(100, 100, 300)
  pylab.plot(averages, label = "one hundred arms")

  pylab.legend(loc="lower right")

  pylab.show()

def different_epsilons():
  "In which we see that higher epsilons start out better, then do worse"
  for epsilon in [0.05, 0.01, 0.1]:
    averages = RLAgent(lambda (x) : epsilon).play_repeatedly(10, 300, 100)
    pylab.plot(averages, label = "epsilon = %f"%epsilon)

  pylab.legend(loc="lower right")

  pylab.show()

different_epsilons()