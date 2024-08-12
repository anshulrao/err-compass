# Error Compass

Locate error messages closely matching the provided input from a mapping containing error messages paired with corresponding resolutions. This tool assists in directing users to the appropriate actions needed when encountering specific errors.


### MOTIVATION
The error messages in log files often follow a predictable pattern, as certain parts are hardcoded. When debugging an issue and encountering an error message, we typically follow a specific route to resolve it. However, if someone, whether a new team member or the same individual at a later time, encounters a similar error message, they may need to repeat the same troubleshooting process. This tool aims to address this challenge by storing information about previous resolutions, allowing users to search for and find the solutions previously taken.

### SUMMARY
We utilize this tool to collect all encountered errors along with the corresponding actions and resolutions.

* **INSERT** Panel: Enables users to record errors along with their corresponding resolutions.
* **SEARCH** Panel: When a user encounters an error, they can search the logs using this panel. The search employs cosine similarity to find and display the top five closest matching errors from previously stored data. To compute sentence vectors, three methods are used:
    * **Bag of Words**: This method represents each sentence as a vector of word counts, capturing the frequency of each word in the sentence.
    * **GloVe** (Global Vectors for Word Representation): This is a pre-trained word embedding model with 100 dimensions, which maps each word to a vector. For out-of-vocabulary (OOV) words, a zero vector is used. To obtain a single vector for a sentence, the vectors of all words in the sentence are averaged.
  * **Word2Vec**: Unlike GloVe, the Word2Vec embeddings are specifically trained on the stored errors.
* **FILTER** Panel: This scans a log file to identify error or failure messages. It then matches and ranks these errors using cosine similarity, displaying the top five matches for each error found in the log file. The same three vectorization methods (Bag of Words, GloVe, and Word2Vec) are utilized for this process.

#### COSINE SIMILARITY
Cosine similarity is a metric used to measure the similarity between two vectors in a vector space. It calculates the cosine of the angle between the two vectors, which gives an indication of how similar they are. In essence, two vectors in n-dimensional space are closer if the angle θ between them is small. This concept forms the fundamental principle behind this metric measurement.

$$\text{cosine similarity}(\mathbf{X}, \mathbf{Y}) = \frac{\mathbf{X} \cdot \mathbf{Y}}{\|\mathbf{X}\| \|\mathbf{Y}\|}$$

where:
- $\ \mathbf{X} \ and \ \mathbf{Y} \ are \ vectors \ in \ the \ same \ vector \ space.$
- $\( \cdot \) \ denotes \ the \ dot \ product \ of \ vectors \ \ \mathbf{X} \ and \ \mathbf{Y} \.$
- $\ \|\mathbf{X}\| \ and \ \|\mathbf{Y}\| \ denote \ the \ Euclidean \ norms \ (magnitudes) \ of \ vectors \ \ \mathbf{X} \ and \ \mathbf{Y} \ \ respectively.$

<br/>

  Example,
  
    Sentence 1: *"The cat sat on mat."*<br>
    Sentence 2: *"The dog sat on mat."*<br>
    Sentence 3: *"A bird flew over house."*<br>

    Now, let's convert these sentences into vectors based on word counts.<br>
    We'll consider a simple bag-of-words approach where each dimension of the vector<br>
    represents the count of a specific word in the sentence.

    Assuming a vocabulary of `["the", "cat", "sat", "on", "mat", "dog", "a", "bird", "flew", "over", "house"]`,<br>
    the vectors would be:

    S<sub>1</sub> = `[1,1,1,1,1,0,0,0,0,0,0]`<br>
    S<sub>2</sub> = `[1,0,1,1,1,1,0,0,0,0,0]`<br>
    S<sub>3</sub> = `[0,0,0,0,0,0,1,1,1,1,1]`<br>

    cosine_similarity(S<sub>1</sub>, S<sub>2</sub>) = `0.8`<br>
    cosine_similarity(S<sub>1</sub>, S<sub>3</sub>) = `0`<br>
    cosine_similarity(S<sub>2</sub>, S<sub>3</sub>) = `0`<br>


#### INSERT
<img width="1063" alt="Screenshot 2024-02-18 at 7 39 04 PM" src="https://github.com/anshulrao/error-compass/assets/31268509/f8fc8e68-5d2b-45c8-81cc-197fcfa81a20">


#### SEARCH
<img width="1063" alt="Screenshot 2024-08-12 at 4 38 20 PM" src="https://github.com/user-attachments/assets/0b6af02c-90ac-4fd9-a98c-aebaef8a8f13">


#### FILTER
<img width="991" alt="Screenshot 2024-08-12 at 5 06 56 PM" src="https://github.com/user-attachments/assets/a6923412-8b66-4ca7-9984-a4d0c5b1b83d">


