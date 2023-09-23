import random
import sys
from datetime import date

def main():
  filename = sys.argv[1]
  print("Filename (use for random seed as well): " + filename)

  with open(filename) as f:
    raw = f.read()

  names = [(line.split(".")[1].strip(), line.split(".")[0].strip()) for line in raw.split("\n")[:-1]]
  slots = ["1:30", "2:00", "2:30", "3:00", "3:30", "4:00", "4:30", "5:00"]

  random.seed(filename)
  selected = random.sample(names, len(slots))

  print('Names:')
  for name in names:
    print(name)

  for i in range(len(slots)):
    end_slot = slots[i+1] if i + 1 < len(slots) else "end"
    print(slots[i] + "-" + end_slot+": " + selected[i][0] + " (" + selected[i][1] + ")")

if __name__ == "__main__":
  main()
