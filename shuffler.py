import random
from datetime import date, datetime

def extract_name(line):
  chunks = line.split('.')
  return chunks[1].strip(), chunks[0].strip()

def extract_request_content(request):
  request = request[request.find('1.'):]
  request = request.split('- Venmo')[0]
  return request.strip()

def get_shuffle_response(request, date, enable_extraction=False,
                         enable_pair_on_duty=True):
  if enable_extraction:
    request = extract_request_content(request)
  names = [extract_name(line) for line in request.split('\n')[:-1]]
  slots = ['1:30', '2:00', '2:30', '3:00', '3:30', '4:00', '4:30', '5:00']

  random.seed(str(date))
  selected_num_multipier = 2 if enable_pair_on_duty else 1
  selected = random.sample(names, len(slots) * selected_num_multipier)

  response = 'On-duty ' + str(date) + '\n--\n'
  for i in range(len(slots)):
    end_slot = slots[i+1] if i + 1 < len(slots) else 'end'
    if enable_pair_on_duty:
      on_duty_name = get_printed_name(selected[i*2]) + ' + ' \
          + get_printed_name(selected[i*2 + 1])
    else:
      on_duty_name = get_printed_name(selected[i])
    response += slots[i] + '-' + end_slot + ': ' + on_duty_name + '\n'
  return response + get_instructions()

def get_printed_name(name):
  return name[0] + ' (' + name[1] + ')'

def get_instructions():
  return '''--
Instruction
1. 在群裡，如果"unassigned"達4人，把每4人sign到未滿8人的場（優先選已經有sign 4人的場，再選附近的快結束的場）。
2. 在電腦上，任何有我們sign的球場，如果剩下時間在30分鐘內，把在場上的4人unassign後再sign回queue去。
3. 做任何變更之後，更新群裡面的訊息。
4. 結束時提醒下一個On-duty。
--
Note: On-Duty需要調整的人，自行跟其他團員協調即可。'''

