import random
from datetime import date, datetime

from utils import extract_name_from_raw

EXCEPTIONAL_NAMES = []


def extract_request_content(request):
  request = request[request.find('1.'):]
  request = request.split('- Venmo')[0]
  return request.strip()


def get_random_seed(date):
  return int(date.strftime('%Y%m%d'))


def remove_exceptional_names(all_names):
  names = []
  for name in all_names:
    if name[0] in EXCEPTIONAL_NAMES:
      continue
    names.append(name)
  return names


def get_shuffle_response(names, date, enable_index_to_name=False):
    """Generate a shuffle response for the given names and date.
    
    Args:
        names: List of names (strings) or a raw request string (for backward compatibility)
        date: The date for the shuffle (used for random seed)
        enable_index_to_name: Whether to include indices in the output names
        
    Returns:
        str: Formatted shuffle response
    """
    # Handle both list of names and raw string input (for backward compatibility)
    if isinstance(names, str):
        # This is a raw request string, extract names from it
        name_entries = extract_name_from_raw(names)
        names = [name for name, _ in name_entries]
    
    if not names:
        return "Error: No valid names provided"
    
    # Remove exceptional names
    names = remove_exceptional_names(names)
    
    # Define the 8 time slots we want to use
    time_slots = [
        '1:30-2:00', '2:00-2:30', '2:30-3:00', '3:00-3:30',
        '3:30-4:00', '4:00-4:30', '4:30-5:00', '5:00-end'
    ]
    
    # Shuffle with fixed seed based on date
    random.seed(get_random_seed(date))
    shuffled_names = names.copy()
    random.shuffle(shuffled_names)
    
    # Generate pairs for each time slot (only up to the number of time slots we have)
    response = [f'On-duty {date} ({len(names)} attended)', '--']
    
    # Only generate pairs for the defined time slots (8 slots = 16 people max)
    max_pairs = len(time_slots)
    for i in range(0, min(2 * max_pairs, len(shuffled_names) - 1), 2):
        time_slot = time_slots[i//2]
        name1 = get_printed_name((shuffled_names[i], str(i+1)), enable_index_to_name)
        name2 = get_printed_name((shuffled_names[i+1], str(i+2)), enable_index_to_name)
        response.append(f'{time_slot}: {name1} + {name2}')
    
    response.extend(['--', get_instructions()])
    return '\n'.join(response)


def get_printed_name(name, enable_index_to_name):
  return name[0] + ' (' + name[1] + ')' if enable_index_to_name else name[0]


def get_instructions():
  return '''--
Instruction

1. If there are more than 4 "unassigned" people, sign every 4 people to a court until a court has 8 of our people and there are no more than 4 "unassigned" people.
2. If a signed court ends in 25 mins, unassigned the first 4 people and reassign them back to the queue.
3. Update all changes within the Instagram group chat.
4. Remind the next on-duty (and pass the pager to them).

1. 在群裡，如果"unassigned"達4人，把每4人sign到未滿8人的場（優先選已經有sign 4人的場，再選附近的快結束的場）。
2. 在電腦上，任何有我們sign的球場，如果剩下時間在25分鐘內，把在場上的4人unassign後再sign回queue去。
3. 做任何變更之後，更新群裡面的訊息。
4. 結束時提醒下一個On-duty，把pager給他。
--
Note: On-Duty需要調整的人，自行跟其他團員協調即可。'''
