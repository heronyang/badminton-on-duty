def extract_name(line):
  chunks = line.split('.')
  return chunks[1].strip(), chunks[0].strip()

def extract_name_from_raw(raw):
  return [extract_name(line) for line in raw.split('\n')[:-1]]
