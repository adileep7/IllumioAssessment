# IllumioAssessment
## How to Run:
1. Clone this repository
2. Add the following files to the project directory:
flow_log.txt (for flow log data) and 
lookup.csv (for the lookup table)
4. Ensure you have Python 3.x installed.
5. Run the application by executing the main script with the command: python3 tag_mapper.py
6. To view the program's results, open the generated output.csv file
7. To execute the unit test cases, use: python3 test_tag_mapper.py

## Assumptions made:
- The program only supports default log format, not custom and the only version that is supported is 2.
- According to the IANA (https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml), protocol numbers with values 146-252 are Unassigned. In my code, I check for this case and label them as 'Unassigned'. I also use the label 'Unknown Protocol', which is used when the protocol number found in the flow log is not recognized in the protocol mapping. I used the IANA CSV file to map protocol numbers to their corresponding names (keywords). Rows without a keyword were excluded and are therefore classified as 'Unknown Protocols'.

## Tests Done/Analyses:
I conducted tests across various scenarios, including unrecognized protocol numbers, duplicate entries, and case insensitivity. File Not Found handling is implemented to ensure that users are notified if either of the two input files is missing. Additionally, I added unit test cases to ensure the functionality of the core features. Also, although I did not add these in my code, the following enhancements will make the code more robust and easier to debug when issues arise.
1. Value Errors:
   ValueError handling when converting strings to integers, which can occur if the data is not formatted correctly.
2. General Exception Handling:
   Catch-all exceptions to inform users of unexpected issues.
3. Output Writing Errors:
   Exception handling for file writing to ensure any issues during output generation are caught.
