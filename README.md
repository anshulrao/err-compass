# Error Compass

Locate error messages closely matching the provided input from a mapping containing error messages paired with corresponding resolutions. This tool assists in directing users to the appropriate actions needed when encountering specific errors.


### MOTIVATION
The error messages in log files often follow a predictable pattern, as certain parts are hardcoded. When debugging an issue and encountering an error message, we typically follow a specific route to resolve it. However, if someone, whether a new team member or the same individual at a later time, encounters a similar error message, they may need to repeat the same troubleshooting process. This tool aims to address this challenge by storing information about previous resolutions, allowing users to search for and find the solutions previously taken.

### SUMMARY
We utilize this tool to collect all encountered errors along with the corresponding actions and resolutions. The INSERT panel facilitates this process by enabling us to record such information. Subsequently, whenever a user comes across an error in the logs, they can utilize the SEARCH panel to determine if that particular error or a similar one has been encountered previously. To enhance search accuracy, cosine similarity is employed to identify the top five closest errors stored in the file. The FILTER panel scans a log file to sift through all error or failure messages and then attempts to match and locate them in the file. The top five errors, ranked using the same cosine similarity logic, are displayed for each error message found in the log file.


#### INSERT
<img width="1063" alt="Screenshot 2024-02-18 at 7 39 04 PM" src="https://github.com/anshulrao/error-compass/assets/31268509/f8fc8e68-5d2b-45c8-81cc-197fcfa81a20">


#### SEARCH
<img width="1062" alt="Screenshot 2024-02-18 at 7 42 13 PM" src="https://github.com/anshulrao/error-compass/assets/31268509/31b25784-4891-4db9-b561-1d2a006d1809">


#### FILTER
<img width="1063" alt="Screenshot 2024-02-18 at 7 42 44 PM" src="https://github.com/anshulrao/error-compass/assets/31268509/a0b88114-f442-428e-b720-483d384ebf23">



