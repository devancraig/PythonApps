import math

class Buy:
  def __init__(self, bal, price, amount):
    self.b = bal
    self.p = price
    self.a = amount

  def myfunc(self):
    i = 0
    while i < self.a:
        if self.b > self.p:
            self.b -= self.p
        i += 1
    return int(self.b)

pd = Buy(1000.00,25,1)
a = pd.myfunc()
print(a)