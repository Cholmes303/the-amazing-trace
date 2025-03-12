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
Parses traceroute output into structured data to be graphed:
- `hop`: Hop number (integer)
- `ip`: IP address of the router (string or `None` if unavailable)
- `hostname`: Hostname (string or `None` if same as IP)
- `rtt`: List of round-trip times in milliseconds (`None` for timeouts)

For this function, it is important that I explain two main things: why use the ```re.match()``` function and the regex ```.group()``` function. Before explaining these though, there will be more on the regex string that extracts the data from the traceroute output later on in the README. 

#### re.match()
Now, ```re.match()``` is a function that will match the regex string ```pattern = r'(\d+)\s+([^\s]+)\s+\(([^)]+)\)\s+((?:\d+\.\d+\s+ms\s+)+|\*+\s+\*+\s+\*+|\s*)'``` to the output of traceroute resulting in extracting the desired information from the string. The function only matches with the beginning of the string which is why I have split the output of traceroute multiple times. More on the ```re.match()``` function can be found [here](https://www.geeksforgeeks.org/re-match-in-python/). 

#### .group()
Continuing onto the ```.group()``` function, this function is used to find specific groups within the matched regex string. Groups are defined in the regex string by surrounding "()". For example in the first part of the string: ```r'(\d+)\s+...'``` the first group is defined as ```\d+``` because it is surrounded by "()". This continues on for the rest of the string. More on the ```.group()``` function can be found [here](https://www.geeksforgeeks.org/re-matchobject-group-function-in-python-regex/). Something to note is for the IP address section there are "()" that are escaped by a "\". This is done so the IP address when matched is surrounded by () when bring put into the dictionary that will be appended to the list hops. As mentioned before, there will be an indepth explanation of the regex string found below due to the complexity. 

### Back to the function
Here is the function:
```python
def parse_traceroute(traceroute_output):
    # Initialize an empty list to store hop data
    hops = []

    # Regex pattern to capture hop data
    # Order: group 1 (hop), group 2 (hostname), group 3 (ip), group 4 (rrt)
    pattern = r'(\d+)\s+([^\s]+)\s+\(([^)]+)\)\s+((?:\d+\.\d+\s+ms\s+)+|\*+\s+\*+\s+\*+|\s*)'

    # Process each line of traceroute output
    for line in traceroute_output.splitlines():
        # Match is used to find the start of the string. Strip() is used to make each individual "word" its own line.
        match = re.match(pattern, line.strip())

        # Groups each piece of data in trace route by Regex pattern.
        if match:
            hop = int(match.group(1))
            hostname = match.group(2) 
            ip = match.group(3)
            rtt_values_str = match.group(4)

            # Handles timeout cases (noted by asterisks "*")
            if '*' in rtt_values_str:
                rtt = [None, None, None]  # Timeout case
            else:
                # Parse the rtt values (remove 'ms' and convert to float)
                rtt = [float(rtt.strip()) for rtt in rtt_values_str.split('ms') if rtt.strip()]

            # Handle the case when hostname is the same as IP
            if hostname == ip:
                hostname = None

            # Create dictionary of hop data and move dictionary into list. 
            hops.append({
                'hop': hop,
                'ip': ip,
                'hostname': hostname,
                'rtt': rtt
            })
    return hops

```

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

This regex string is what extracts the data from the ```traceroute_output``` variable. More on regex can be found [here](https://learn.microsoft.com/en-us/dotnet/standard/base-types/regular-expression-language-quick-reference). Additionally [here](https://regex101.com/) is a website that can explain regex code in real time. Regex was most definitely the biggest challenge when writing this script, I hope this helps. 

