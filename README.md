# Error Compass

Locate error messages closely matching the provided input from a mapping containing error messages paired with corresponding resolutions. This tool assists in directing users to the appropriate actions needed when encountering specific errors.


### MOTIVATION
The error messages in log files often follow a predictable pattern, as certain parts are hardcoded. When debugging an issue and encountering an error message, we typically follow a specific route to resolve it. However, if someone, whether a new team member or the same individual at a later time, encounters a similar error message, they may need to repeat the same troubleshooting process. This tool aims to address this challenge by storing information about previous resolutions, allowing users to search for and find the solutions previously taken.

### SUMMARY
We utilize this tool to collect all encountered errors along with the corresponding actions and resolutions. The INSERT panel facilitates this process by enabling us to record such information. Subsequently, whenever a user comes across an error in the logs, they can utilize the SEARCH panel to determine if that particular error or a similar one has been encountered previously. To enhance search accuracy, cosine similarity is employed to identify the top five closest errors stored in the file.

#### SEARCH
<img width="1399" alt="Screenshot 2024-02-14 at 7 08 32 PM" src="https://github.com/anshulrao/err-compass/assets/31268509/53f87657-4810-4179-a407-8a6130fb106e">

#### INSERT
<img width="1399" alt="Screenshot 2024-02-14 at 7 08 04 PM" src="https://github.com/anshulrao/err-compass/assets/31268509/f01d7c17-50b1-4b16-880e-d89b9b0cb79e">

