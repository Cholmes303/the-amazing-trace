[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=18568294)
# The Amazing Trace

This project involves developing two core functions to execute and parse traceroute output, aiding in the visualization of routing paths.

### Functions to Implement

1. `execute_traceroute(destination)`: Runs the traceroute command and returns the output.
2. `parse_traceroute(traceroute_output)`: Converts traceroute output into a structured format.

### Expected Output Format

The `parse_traceroute` function returns a list of dictionaries, each containing:
- `hop`: The hop number (integer).
- `ip`: IP address of the router (string or `None` if unavailable).
- `hostname`: Hostname (string or `None` if the same as IP).
- `rtt`: List of round-trip times in milliseconds (`None` for timeouts).

### Running the Code

### Dependencies

Ensure `traceroute` is installed on your system. The script uses:
- Python 3
- `subprocess` for executing commands
- `re` for parsing output

### Expected Visualization

Once implemented correctly, the `amazing-trace.py` script will generate a visualization of traceroute paths in the `output/` directory.

