import unittest
import csv
import os

from tag_mapper import load_lookup_table, parse_flow_log

class TestFlowLogParser(unittest.TestCase):

    def setUp(self):
        self.lookup_file = 'test_lookup.csv'
        self.flow_log_file = 'test_flow_log.txt'
        
        # Sample lookup table
        with open(self.lookup_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['dstport', 'protocol', 'tag'])
            writer.writerow(['22', 'tcp', 'sv_P1'])
            writer.writerow(['23', 'tcp', 'sv_P2'])
            writer.writerow(['25', 'udp', 'sv_P3']) 

        # Sample flow log
        with open(self.flow_log_file, 'w', newline='') as f:
            f.write("... ... ... ... ... ... 22 6\n")   # Matches sv_P1
            f.write("... ... ... ... ... ... 23 6\n")  # Matches sv_P2
            f.write("... ... ... ... ... ... 25 17\n")  # Matches sv_P3
            f.write("... ... ... ... ... ... 80 260\n")   # Unknown protocol
            f.write("... ... ... ... ... ... 80 146\n")  # Unassigned protocol

    def tearDown(self):
        os.remove(self.lookup_file)
        os.remove(self.flow_log_file)

    def test_load_lookup_table(self):
        lookup_table = load_lookup_table(self.lookup_file)
        self.assertEqual(lookup_table[(22, 'tcp')], 'sv_P1')
        self.assertEqual(lookup_table[(23, 'tcp')], 'sv_P2')
        self.assertEqual(lookup_table[(25, 'udp')], 'sv_P3')  
        self.assertNotIn((80, 'tcp'), lookup_table)

    def test_parse_flow_log(self):
        # Using a fixed protocol mapping for testing
        fixed_protocol_mapping = {
            '6': 'tcp',
            '17': 'udp',
            '1': 'icmp'
        }
        
        lookup_table = load_lookup_table(self.lookup_file)
        tag_counts, port_protocol_counts = parse_flow_log(self.flow_log_file, lookup_table, fixed_protocol_mapping)

        # Debugging output
        print("Tag Counts:", tag_counts)
        print("Port/Protocol Counts:", port_protocol_counts)

        # Check tag counts
        self.assertIn('sv_P1', tag_counts)
        self.assertEqual(tag_counts['sv_P1'], 1)
        
        self.assertIn('sv_P2', tag_counts)
        self.assertEqual(tag_counts['sv_P2'], 1)

        self.assertIn('sv_P3', tag_counts)
        self.assertEqual(tag_counts['sv_P3'], 1) 

        self.assertEqual(tag_counts['Unassigned'], 1)  # For port 80 with protocol 146
        self.assertEqual(tag_counts['Unknown Protocol'], 1)  # For port 80 with protocol 260

        # Check port/protocol combination counts
        self.assertEqual(port_protocol_counts[(22, '6')], 1)  # From sv_P1
        self.assertEqual(port_protocol_counts[(23, '6')], 1)  # From sv_P2
        self.assertEqual(port_protocol_counts[(25, '17')], 1)  # From sv_P3
        self.assertEqual(port_protocol_counts[(80, '260')], 1)  # Unknown protocol count
        self.assertEqual(port_protocol_counts[(80, '146')], 1)  # Unassigned protocol count

if __name__ == '__main__':
    unittest.main()