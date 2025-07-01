def extract_name(line):
    # Clean up the line by removing extra whitespace
    line = line.strip()
    
    # Find the first non-digit character to separate index and name
    index_match = None
    for i in range(len(line)):
        if not line[i].isdigit():
            index_match = line[:i].strip()
            break
    
    # If no index found or index is empty, skip this line
    if not index_match or not index_match.isdigit():
        return '', ''
    
    # Skip the dot and any whitespace after the index
    while i < len(line) and (line[i].isspace() or line[i] == '.'):
        i += 1
    
    # Extract the name part after the index
    name_part = line[i:].strip()
    
    # If we couldn't extract a valid name, return empty strings
    if not name_part:
        return '', ''
    
    return name_part, index_match


def extract_name_from_raw(raw):
    names = []
    lines = raw.split('\n')
    
    for line in lines:
        # Skip empty lines
        if not line.strip():
            continue
            
        # Extract name and index
        name, index = extract_name(line)
        
        # Skip if we couldn't extract a valid name
        if not name:
            continue
            
        # Skip if the name is just a number (likely just the index)
        if name.isdigit():
            continue
            
        # Add to names list
        names.append((name, index))
    
    return names
