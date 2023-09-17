import random
import sys
from datetime import date

def main():
  filename = sys.argv[1]
  print("Filename (use for random seed as well): " + filename)

  with open(filename) as f:
    raw = f.read()
  names = [line.split(".")[1].strip() for line in raw.split("\n")[:-1]]
  slots = ["1:30", "2:00", "2:30", "3:00", "3:30", "4:00", "4:30", "5:00"]

  random.seed(filename)
  selected = random.sample(names, len(slots))

  for i in range(len(slots)):
    print(slots[i]+ " : " + selected[i])

if __name__ == "__main__":
  main()
