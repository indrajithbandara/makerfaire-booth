import sys
sys.path.insert(0, "../burgerdata")
from burger_data import BurgerElement
import itertools

class ExhaustiveBurger():
  def __init__(self):
    members = BurgerElement.__members__
    self.all_burgers = []
    burgers = itertools.product(members.values(), repeat=8)
    for burger in burgers:
      self.all_burgers.append(burger)

    self.i = 0

  def next_burger(self):
    if self.i == len(self.all_burgers):
      raise StopIteration
    burger = self.all_burgers[self.i]
    self.i += 1
    return burger