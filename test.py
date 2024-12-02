import random

def make_color(labels):
  colors = [[random.randint(0,255) for _ in range(3)] for _ in labels]
  color = random.choice(colors)
  return color

labels = ['개', '고양이', '의자']

test = [ [random.randint(0,255) for _ in range(3)] for _ in labels ]

print(test)
print(random.choice(test))