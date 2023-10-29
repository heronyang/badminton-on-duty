import random
import sys
from datetime import date

ENABLE_PAIR_ON_DUTY = True

def extract_name(line):
  chunks = line.split(".")
  return chunks[1].strip(), chunks[0].strip()

def get_printed_name(name):
  return name[0] + " (" + name[1] + ")"

def print_instructions():
  print("""--
Instruction
1. 在群裡，如果”unassigned”達4人，把每4人sign到未滿8人的場（優先選已經有sign 4人的場，再選附近的快結束的場）。
2. 在電腦上，任何有我們sign的球場，如果剩下時間在30分鐘內，把在場上的4人unassign後再sign回queue去。
3. 做任何變更之後，更新群裡面的訊息。
4. 結束時提醒下一個On-duty。
--
Note: On-Duty需要調整的人，自行跟其他團員協調即可。""")

def main():
  filename = sys.argv[1]
  
  print('On-duty ' + filename.split('.')[0])

  with open(filename) as f:
    raw = f.read()

  names = [extract_name(line) for line in raw.split("\n")[:-1]]
  slots = ["1:30", "2:00", "2:30", "3:00", "3:30", "4:00", "4:30", "5:00"]

  random.seed(filename)
  selected_num_multipier = 2 if ENABLE_PAIR_ON_DUTY else 1
  selected = random.sample(names, len(slots) * selected_num_multipier)

  for i in range(len(slots)):
    end_slot = slots[i+1] if i + 1 < len(slots) else "end"
    if ENABLE_PAIR_ON_DUTY:
      on_duty_name = get_printed_name(selected[i*2]) + " + " \
          + get_printed_name(selected[i*2 + 1])
    else:
      on_duty_name = get_printed_name(selected[i])
    print(slots[i] + "-" + end_slot + ": " + on_duty_name)

  print_instructions()

if __name__ == "__main__":
  main()
