def extract_name(line):
  chunks = line.split('.')
  return chunks[1].strip(), chunks[0].strip()


def extract_name_from_raw(raw):
  names = []
  for line in raw.split('\n')[:-1]:
    name = extract_name(line)
    if name[0].strip():
      names.append(name)
  return names
