import sys
from datetime import datetime

from shuffler import get_shuffle_response

def get_date_from_filename(filename):
  date_str = filename.split('.')[0]
  return datetime.strptime(date_str, '%Y-%m-%d').date()

def main():
  filename = sys.argv[1]
  date = get_date_from_filename(filename)
  
  with open(filename) as f:
    raw = f.read()

  response = get_shuffle_response(request=raw, date=date)
  print(response)

if __name__ == '__main__':
  main()
