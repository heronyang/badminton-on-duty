import random
import sys
from datetime import date

ENABLE_PAIR_ON_DUTY = True

def extract_name(line):
  chunks = line.split(".")
  return chunks[1].strip(), chunks[0].strip()

def get_printed_name(name):
  return name[0] + " (" + name[1] + ")"

def main():
  filename = sys.argv[1]
  print("Filename (use for random seed as well): " + filename)

  with open(filename) as f:
    raw = f.read()

  names = [extract_name(line) for line in raw.split("\n")[:-1]]
  slots = ["1:30", "2:00", "2:30", "3:00", "3:30", "4:00", "4:30", "5:00"]

  random.seed(filename)
  selected_num_multipier = 2 if ENABLE_PAIR_ON_DUTY else 1
  selected = random.sample(names, len(slots) * selected_num_multipier)

  print('Names:')
  for name in names:
    print(name)

  for i in range(len(slots)):
    end_slot = slots[i+1] if i + 1 < len(slots) else "end"
    if ENABLE_PAIR_ON_DUTY:
      on_duty_name = get_printed_name(selected[i*2]) + " + " \
          + get_printed_name(selected[i*2 + 1])
    else:
      on_duty_name = get_printed_name(selected[i])
    print(slots[i] + "-" + end_slot + ": " + on_duty_name)

if __name__ == "__main__":
  main()
