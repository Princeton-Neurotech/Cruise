# Cruise
Cruise utilizes user keyboard text input and EEG data to increase writing productivity. The application predicts when the user will approach a writing roadblock and offers user-specific solutions such as recommending research articles, scaffolding questions, or taking a break. Custom writing productivity thresholds can be specified by the user. Additionally, a user-specific break model will be developed through keeping track of when, how many, and at what frequency breaks are taken; this will help direct the user during their writing process. This functionality is available through a Chrome Extension, where the user works on a Google Doc, receiving updates and guidance in real time.
 
**Features**
- Google Docs compatible
- Keyboard input and EEG data (through the Muse consumer headset) is collected in real-time from the user
- User can customize productivity standards (estimated total time, wordcount, pagecount, font settings)
- Recommended research articles and scaffolding questions are based on user's written content
- Number of breaks, their duration, and their frequency are measured in order to develop an individualized model for the user, maximizing their productivity
 
**Pipeline**:
- Web Interface: initiates Chrome web browser for text data collection from a Google Docs
- Extract Text: completes access of user text input data from Google Docs API in real time
- Keyboard Features: calculates number of characters, words, sentences, and user standby times (time without typing) in real time from a text input and within a custom time interval; inserts newly manipulated text data to cloud database
- EEG Data Collection: accesses user EEG data and preprocesses data in real-time
- Machine Learning: applies Principal Component Analysis to reduce dimensionality of features. Uses an existent generalized model developed from a set of baseline users and regularly improves upon this model through fitting it with user keyboard text and EEG data using one-shot learning, making the model more user-specific overtime. Periodically predicts if the user will hit customly predefined definition of roadblock. 
- ReactJS is used to develop the Chrome Extension
