import sys
import os
from datetime import datetime
from utils import extract_name_from_raw
from shuffler import get_shuffle_response

def validate_and_parse_filename(filename):
    """Validate the input filename and parse the date from it.
    
    Args:
        filename: Input filename (must be in format YYYY-MM-DD-original.txt)
        
    Returns:
        tuple: (cleaned_filename, date) where cleaned_filename is the output filename
               without the -original suffix
    """
    # Check if filename ends with -original.txt
    if not filename.endswith('-original.txt'):
        raise ValueError("Input file must end with '-original.txt'")
    
    # Extract date part (remove -original.txt and get YYYY-MM-DD)
    date_str = filename.replace('-original.txt', '')
    
    # Validate date format
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        raise ValueError("Filename must start with a valid date in format YYYY-MM-DD")
    
    # Generate cleaned output filename
    cleaned_filename = date_str + '.txt'
    
    return cleaned_filename, date

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 main.py YYYY-MM-DD-original.txt")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    try:
        # Validate filename and get output filename and date
        output_file, date = validate_and_parse_filename(input_file)
        
        # Read and process the input file
        with open(input_file, 'r') as f:
            raw_content = f.read()
        
        # Extract names using the utility function
        name_entries = extract_name_from_raw(raw_content)
        names = [name for name, _ in name_entries]
        
        # Write cleaned output file
        with open(output_file, 'w') as f:
            for i, name in enumerate(names, 1):
                f.write(f"{i}. {name}\n")
        
        # Get the shuffle response
        response = get_shuffle_response(names, date)
        
        # Print to console
        print(response)
        
        # Save to output file
        output_filename = date.strftime('%Y-%m-%d') + '-output.txt'
        with open(output_filename, 'w') as f:
            f.write(response)
        print(f"\nOutput also saved to: {output_filename}")
        
    except (ValueError, FileNotFoundError) as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
