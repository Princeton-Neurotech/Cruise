# Cruise
 
Cruise utilizes user keyboard text input and EEG brain data to increase writing productivity. Custom writing productivity thresholds can be specified. Cruise predicts when the user will approach a roadblock and offers user-specific solutions such as recommending research articles, scaffolding questions, or taking a break. 
 
**Features**
- Users write on a Google Docs document
- Keyboard input and brain data is collected in real-time from the user
- Brain data is collected using the Cyton OpenBCI EEG headset
- User can customize productivity standards which includes the number of words that need to be written and the time interval
- Recommended research articles and scaffolding questions are based on user's written content
- Number of breaks, their duration, and their frequency are measured in order to develop an individualized model for the user, maximizing their productivity
 
**Pipeline**:
- Web Interface: sets flickering in a GoogleDocs document and initiates running data processes for text and brain data collection.
- Extract Text: completes access of user text input data from Google Docs API in real time.
- Realtime Function: keeps track of number of characters, words, sentences, and user standby times (time without typing) in real time from a text input and within a custom time interval. Inserts newly manipulated text data to cloud database.
- Final Brain Features: completes access to user brain (EEG) data and preprocesses data in real time.
- Brain Data Computations: calculates summary statistics for each channel, from an EEG data matrix with a custom number of samples. Examples include: mean, standard deviation, skewness, kurtosis, maximum, minimum, covariance matrix, eigenvalues of covariance matrix, and fft. Inserts newly manipulated EEG data to cloud database.
- Machine Learning: constantly predicts if the user will hit customly predefined definition of roadblock. Recurrently fits machine learning model using joined keyboard text and EEG data. 
