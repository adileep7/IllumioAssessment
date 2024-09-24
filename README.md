# IllumioAssessment
## How to Run:
1. Clone the repository
2. Prepare Data Files
Add the following files to the project directory:
flow_log.txt (for flow log data)
lookup.csv (for the lookup table)
4. Run the application by executing the main script with the command: python3 tag_mapper.py
5. To execute the unit test cases, use: python3 test_tag_mapper.py

## Assumptions made:
The program only supports default log format, not custom and the only version that is supported is 2.

## Tests Done/Analyses:
I added unit test cases to ensure the functionality of the core features. In addition, although I did not add these in my code, the following enhancements will make the code more robust and easier to debug when issues arise.
1. File Not Found Handling:
   FileNotFoundError handling to ensure that users are informed if a specified file does not exist.
2. Value Errors:
   ValueError handling when converting strings to integers, which can occur if the data is not formatted correctly.
3. General Exception Handling:
   Catch-all exceptions to inform users of unexpected issues.
4. Output Writing Errors:
   Exception handling for file writing to ensure any issues during output generation are caught.
