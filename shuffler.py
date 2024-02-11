import random
from datetime import date, datetime

from utils import extract_name_from_raw


def extract_request_content(request):
  request = request[request.find('1.'):]
  request = request.split('- Venmo')[0]
  return request.strip()


def get_random_seed(date):
  return int(date.strftime('%Y%m%d'))


def get_shuffle_response(request,
                         date,
                         enable_extraction=False,
                         enable_pair_on_duty=True,
                         enable_index_to_name=False):
  if enable_extraction:
    request = extract_request_content(request)
  names = extract_name_from_raw(request)
  slots = ['1:30', '2:00', '2:30', '3:00', '3:30', '4:00', '4:30', '5:00']

  random.seed(get_random_seed(date))
  selected_num_multipier = 2 if enable_pair_on_duty else 1
  selected = random.sample(names, len(slots) * selected_num_multipier)

  response = 'On-duty ' + str(date) + ' (' + str(
      len(names)) + ' attended)\n--\n'
  for i in range(len(slots)):
    end_slot = slots[i + 1] if i + 1 < len(slots) else 'end'
    if enable_pair_on_duty:
      on_duty_name = get_printed_name(selected[i*2], enable_index_to_name) + \
          ' + ' + get_printed_name(selected[i*2 + 1], enable_index_to_name)
    else:
      on_duty_name = get_printed_name(selected[i], enable_index_to_name)
    response += slots[i] + '-' + end_slot + ': ' + on_duty_name + '\n'
  return response + get_instructions()


def get_printed_name(name, enable_index_to_name):
  return name[0] + ' (' + name[1] + ')' if enable_index_to_name else name[0]


def get_instructions():
  return '''--
Instruction
1. 在群裡，如果"unassigned"達4人，把每4人sign到未滿8人的場（優先選已經有sign 4人的場，再選附近的快結束的場）。
2. 在電腦上，任何有我們sign的球場，如果剩下時間在30分鐘內，把在場上的4人unassign後再sign回queue去。
3. 做任何變更之後，更新群裡面的訊息。
4. 結束時提醒下一個On-duty。
--
Note: On-Duty需要調整的人，自行跟其他團員協調即可。'''
