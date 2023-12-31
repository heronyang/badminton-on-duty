import itertools
import pandas as pd

from collections import Counter
from utils import extract_name_from_raw

ALL_FILENAMES = [
    '2023-08-27.txt', '2023-09-03.txt', '2023-09-10.txt', '2023-09-17.txt',
    '2023-09-24.txt', '2023-10-01.txt', '2023-10-08.txt', '2023-10-15.txt',
    '2023-10-22.txt', '2023-10-29.txt', '2023-11-05.txt', '2023-11-12.txt',
    '2023-11-19.txt', '2023-11-26.txt', '2023-12-03.txt', '2023-12-10.txt',
    '2023-12-17.txt'
]
NAME_RANK_CUT = 0.70
COUPLE_RANK_CUT = 0.1
TOGETHER_YES_CUT = 3
APART_CUT = 15

OUTPUT_COUPLE_RANK = 'couples-rank.csv'


def get_names(raw):
  return [chunk[0].lower() for chunk in extract_name_from_raw(raw)]


def get_date_names(filename):
  date = filename.split('.')[0]
  with open(filename) as f:
    names = get_names(f.read())
  return date, names


def update_name_count(names, name_count):
  for name in names:
    name_count[name] = name_count.get(name, 0) + 1
  return name_count


def rank_name_with_count(name_count):
  return dict(
      sorted(name_count.items(), key=lambda item: item[1], reverse=True))


def print_name_rank(name_count, total_dates):
  print('[Rank: Name]')
  for name in name_count:
    attend_ratio = name_count[name] / total_dates
    if attend_ratio < NAME_RANK_CUT:
      break
    print(name + '\t' + format(attend_ratio, ".0%"))


def get_together_times(date_names, couple):
  together = 0
  apart = 0
  for _, names in date_names:
    if couple[0] in names and couple[1] in names:
      together += 1
    if (couple[0] in names and couple[1] not in names) or \
       (couple[0] not in names and couple[1] in names):
      apart += 1
  return together, apart


def print_4_column_row(values):
  print('| {:8} | {:8} | {:10} | {:15} |'.format(*values))


def drop_reverse_matches(df):
  indexes_to_drop = []
  matched = {}
  for index, row in df.iterrows():
    n1, n2 = row['Name 1'], row['Name 2']
    if n1 in matched and n2 in matched[n1]:
      indexes_to_drop.append(index)
      continue
    matched[n2] = matched.get(n2, set())
    matched[n2].add(n1)
  return df.drop(df.index[indexes_to_drop]).reset_index(drop=True)


def drop_if_matched_with_a_higher_score(df):
  indexes_to_drop = []
  matched_score = {}
  for index, row in df.iterrows():
    n1, n2 = row['Name 1'], row['Name 2']
    score = [row['Together'], row['Apart']]
    if (n1 in matched_score and matched_score[n1] != score) or\
       (n2 in matched_score and matched_score[n2] != score):
      indexes_to_drop.append(index)
      continue
    matched_score[n1] = score
    matched_score[n2] = score
  return df.drop(df.index[indexes_to_drop]).reset_index(drop=True)


def print_global_couples(df):
  # Filter out the ones out of the cuts.
  df['Rank'] = (df['Together'] - df['Apart']) / df['Together']
  df = df[(df['Apart'] <= APART_CUT) & (df['Together'] >= TOGETHER_YES_CUT) &
          (df['Rank'] >= COUPLE_RANK_CUT)]
  df = df.sort_values(by='Rank', ascending=False).reset_index(drop=True)

  df = drop_reverse_matches(df)
  df = drop_if_matched_with_a_higher_score(df)

  print('[Rank: Couple]')
  print(df.to_string(index=False, formatters={'Rank': '{:,.2%}'.format}))
  df.to_csv(OUTPUT_COUPLE_RANK)


def get_couples(names):
  return [(n1, n2) for n1 in names for n2 in names if n1 != n2]


def get_couple_together_times(date_names, names):
  lines = []
  for couple in get_couples(names):
    together, apart = get_together_times(date_names, couple)
    lines.append([couple[0], couple[1], together, apart])
  return pd.DataFrame(lines, columns=['Name 1', 'Name 2', 'Together', 'Apart'])


def main():
  name_count = {}
  date_names = []

  for filename in ALL_FILENAMES:
    date, names = get_date_names(filename)
    date_names.append([date, names])
    name_count = update_name_count(names, name_count)

  print_name_rank(name_count=rank_name_with_count(name_count),
                  total_dates=len(ALL_FILENAMES))

  couple_together_times = get_couple_together_times(date_names,
                                                    names=name_count.keys())
  print_global_couples(couple_together_times)


if __name__ == '__main__':
  main()
