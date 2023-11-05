import datetime
import sys

def get_all_dates() -> list:
  start_date = datetime.datetime(2023, 8, 27)
  end_date = datetime.datetime.now()

  dates = []
  while start_date <= end_date:
    dates.append(start_date)
    start_date += datetime.timedelta(weeks=1)
  return dates

def main() -> int:
  dates = get_all_dates()
  print(dates)

if __name__ == '__main__':
  sys.exit(main())
