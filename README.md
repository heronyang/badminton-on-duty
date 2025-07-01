# Badminton On-Duty Scheduler

A Python tool for generating badminton court duty schedules from a list of participants.

## Features

- Processes input files with `-original.txt` suffix (e.g., `2025-07-20-original.txt`)
- Generates cleaned output files without the `-original` suffix
- Creates formatted schedule output with `-output.txt` suffix
- Handles various name formats including usernames and display names
- Consistent shuffling based on date for reproducible results

## Prerequisites

- Python 3.6+

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/badminton-on-duty.git
   cd badminton-on-duty
   ```

## Usage

### Generate a new on-duty schedule

1. Create an input file with the format `YYYY-MM-DD-original.txt` containing the list of participants, one per line.
   Example (`2025-07-20-original.txt`):
   ```
   1. @user1
   2. @user2 (Display Name)
   3. Display Name (@username)
   ```

2. Run the script:
   ```bash
   python3 main.py 2025-07-20-original.txt
   ```

3. The script will generate two files:
   - `2025-07-20.txt`: Cleaned list of participants
   - `2025-07-20-output.txt`: Formatted schedule output

4. The schedule will also be printed to the console.

### Example

```bash
# Create input file
echo "1. @user1\n2. @user2\n3. Display Name (@username)" > 2025-07-20-original.txt

# Generate schedule
python3 main.py 2025-07-20-original.txt

# View the output
cat 2025-07-20-output.txt
```

## Input Format

The input file should contain one participant per line, with an optional index number:

```
1. @username
2. Display Name (@username)
3. @username (Display Name)
4. Just a name
```

## Output Format

The output will be a formatted schedule with time slots and assigned pairs:

```
On-duty 2025-07-20 (8 attended)
--
1:30-2:00: @user1 + @user2
2:00-2:30: Display Name (@username) + Another User
...
--
[Instructions]
```

## Running Tests

To run the test suite:

```bash
python -m unittest discover -s tests
```

Or run individual test files:

```bash
python -m unittest tests/test_utils.py
python -m unittest tests/test_shuffler.py
python -m unittest tests/test_main.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
