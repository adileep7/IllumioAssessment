import csv

def load_protocol_mapping(csv_file):
    protocol_mapping = {}
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        # Map the protocol number to its corresponding protocol name
        for row in reader:
            protocol_number = row['protocol_number']
            protocol_name = row['protocol_name'].lower()
            protocol_mapping[protocol_number] = protocol_name
    return protocol_mapping

def load_lookup_table(csv_file):
    lookup_table = {}
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            if len(row) == 3:
                dstport = int(row[0])  # Convert dstport to int from str
                protocol = row[1].lower() 
                tag = row[2]
                key = (dstport, protocol) 
                lookup_table[key] = tag
    return lookup_table

def parse_flow_log(log_file, lookup_table, protocol_mapping):
    tag_counts = {}  
    port_protocol_counts = {}  

    with open(log_file, mode='r', encoding='utf-8') as file:
        for line in file:
            parts = line.split()
            if len(parts) >= 8:  # A check to ensure that there are enough elements to prevent runtime errors
                dstport = int(parts[6])  # Convert dstport to int
                protocol_number = parts[7]
                protocol = protocol_mapping.get(protocol_number, None) 

                # Count the port/protocol combination
                port_protocol_key = (dstport, protocol_number)
                if port_protocol_key not in port_protocol_counts:
                    port_protocol_counts[port_protocol_key] = 0
                port_protocol_counts[port_protocol_key] += 1

                # Special Cases: Check for unassigned/unknown protocol numbers
                if protocol is None:
                    # Check if it's in the unassigned range
                    if 146 <= int(protocol_number) <= 252:
                        tag = 'Unassigned'
                    else:
                        tag = 'Unknown Protocol'
                else:
                    key = (dstport, protocol.lower())  
                    tag = lookup_table.get(key, 'Untagged')

                # Count the tag
                if tag not in tag_counts:
                    tag_counts[tag] = 0
                tag_counts[tag] += 1  # Increment the count for the tag

    return tag_counts, port_protocol_counts

def write_output(output_file, tag_counts, port_protocol_counts, protocol_mapping):
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write tag counts
        writer.writerow(["Count of matches for each tag"])
        writer.writerow(["Tag", "Count"])
        for tag, count in tag_counts.items():
            writer.writerow([tag, count])
        
        writer.writerow([])  # Empty row for separation

        # Write port/protocol combination counts
        writer.writerow(["Count of matches for each port/protocol combination"])
        writer.writerow(["Port", "Protocol", "Count"])
        for (port, protocol_number), count in port_protocol_counts.items():
            protocol_name = protocol_mapping.get(protocol_number, 'Unknown Protocol')
            writer.writerow([port, protocol_name, count])

def main():
    flow_log_file = 'flow_log.txt'  # Path to the given flow log file
    lookup_file = 'lookup.csv'  # Path to the given CSV lookup file
    protocol_file = 'protocol_mapping.csv'  # Path to the protocol mapping CSV file
    output_file = 'output.csv'  # Path for the output CSV file

    missing_files = []
    
    # Check for missing files using try-except
    try:
        with open(lookup_file):
            pass
    except FileNotFoundError:
        missing_files.append(lookup_file)

    try:
        with open(flow_log_file):
            pass
    except FileNotFoundError:
        missing_files.append(flow_log_file)

    if missing_files:
        print(f"Error: The following required files are missing: {', '.join(missing_files)}.")
        return

    try:
        # Load protocol mapping
        protocol_mapping = load_protocol_mapping(protocol_file)
        # Load lookup table
        lookup_table = load_lookup_table(lookup_file)
        # Parse the flow log
        tag_counts, port_protocol_counts = parse_flow_log(flow_log_file, lookup_table, protocol_mapping)
        # Write output to file
        write_output(output_file, tag_counts, port_protocol_counts, protocol_mapping)
        # Success message
        print(f"Success: The results have been written to {output_file}.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
