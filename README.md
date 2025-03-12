[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=18568294)

# The Amazing Trace

This project runs a script that executes and parses traceroute outputs while providing graphed visuals of the routing paths.

## Features
- Executes traceroute using ICMP packets.
- Parses traceroute output into structured data.
- Runs multiple traceroutes and visualizes results.

## Functions Implemented

### `execute_traceroute(destination)`
Executes a traceroute command and returns the output. The -I command is to change the default UDP packets that are being used to ICMP packets. The reason ICMP packers are used over UDP packets is due to UDP packets being used to quickly transfer data. However, here we want to trouble shoot a path which ICMP packets are made to do. Another note, -i is not the same as -I when being used with traceroute. The -i command expects an interface name (ex. eth0). Here is the function: 
```python
def execute_traceroute(destination):

    # Runs traceroute command. 
    result = subprocess.run(["traceroute", "-I", destination], capture_output=True, text=True, check=True)
    return result.stdout
```

### `parse_traceroute(traceroute_output)`
Parses traceroute output into structured data:
- `hop`: Hop number (integer)
- `ip`: IP address of the router (string or `None` if unavailable)
- `hostname`: Hostname (string or `None` if same as IP)
- `rtt`: List of round-trip times in milliseconds (`None` for timeouts)

### `visualize_traceroute(destination, num_traces=3, interval=5, output_dir='output')`
- Runs multiple traceroutes to analyze routing stability.
- Plots hop count vs. average RTT over multiple traces.
- Saves the output visualization as a PNG file.

## Accessing the Script
To access this script you will need to clone down the repository. Run the following command in a terminal to do so:
```
git clone https://github.com/WTCSC/the-amazing-trace-Cholmes303.git
```

## Running the Code
Once you have cloned the repository nagivate to the correct directory and run the script. Here is the command to run the code:
```sh
python3 amazing_trace.py
```

## Dependencies
A Vagrant file, that is attached to the repository, is used to create a virtual machine (VM) that installs all dependecies needed. [Here](https://developer.hashicorp.com/vagrant/install) is the website to install and use Vagrant.
A VM is required to run Vagrant. I suggest [Oracle VM](https://www.oracle.com/virtualization/technologies/vm/downloads/virtualbox-downloads.html) as it provides access to mulitple operating systems (OS) and VMs that you wish to use. 

If you do not wish to use Vagrant then ensure the following are installed:
- Python 3
- `matplotlib`, `pandas`, `numpy`
- `subprocess` for executing commands (installed with Python's library)
- `re` for parsing output (installed with Python's library)
- `traceroute` (ensure it is installed on your system)

## Expected Output
- A structured output of traceroute results including hops, IPs, hostnames, and round trip times (rtt).
- A visualization of traceroute paths saved in the `output/` directory.

## Example Usage
By default, the script traces routes to:
- `google.com`
- `amazon.com`
- `bbc.co.uk`

## Changing the trace routes
To change the default trace routes, edit the list of destinations. This is found at the end of the code:
```python
# Test the functions
if __name__ == "__main__":
    # Test destinations
    destinations = [
        "google.com",
        "amazon.com",
        "bbc.co.uk"  # International site
    ]
```
Edit each string to whatever website you would like. 

## Regex Explanation
Regex came as a very complex but very useful module inside of the Python library. I will explain how my regex function works and provide resources in hopes that they will help you understand the tools that regex provides. The following regex pattern is used to parse the traceroute output:
```python
pattern = r'(\d+)\s+([^\s]+)\s+\(([^)]+)\)\s+((?:\d+\.\d+\s+ms\s+)+|\*+\s+\*+\s+\*+|\s*)'
```

### Breakdown:
- `(\d+)` - Captures the hop number (the "\d" indicates any number 0-9 and the "+" indicates one or more digits).
- `\s+` - Matches one or more whitespace characters.
- `([^\s]+)` - Captures the hostname (a string without spaces).
- `\s+\(([^)]+)\)` - Captures the IP address inside parentheses (the "\" is used around the parathesis to escape them).
- `\s+((?:\d+\.\d+\s+ms\s+)+|\*+\s+\*+\s+\*+|\s*)` - Captures the round-trip times (rtt) or asterisks indicating timeouts (the "|" means or):
  - `(?:\d+\.\d+\s+ms\s+)+` - Matches rtt values (e.g., `12.3 ms 15.6 ms`).
  - `\*+\s+\*+\s+\*+` - Matches `* * *` for timeouts.
  - `\s*` - Matches optional whitespace for cases with missing rtt values.

This regex string is what extracts the data from the traceroute_output variable. More on regex can be found [here](https://learn.microsoft.com/en-us/dotnet/standard/base-types/regular-expression-language-quick-reference). Additionally [here](https://regex101.com/) is a website that can explain regex code in real time. Regex was most definitely the biggest challenge when writing this script, I hope this helps. 

