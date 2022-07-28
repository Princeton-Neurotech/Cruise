# Cruise
## Context
Writing is a major component relevant to all domains, ranging from students to large corporations. It’s difficult for one to develop the self-discipline necessary to keep up their writing efficiency and quality for a long period of time. Therefore, we aim to increase the user’s writing productivity through utilizing their keyboard input and EEG brain data. Especially since COVID-19, a lot of us are working from home and it’s easy to become distracted and lose efficiency. Cruise helps the customer overcome this issue.

## Description
Cruise utilizes user keyboard text input and EEG data to increase writing productivity. The application predicts when the user will approach a writing roadblock and offers user-specific solutions such as recommended research articles, scaffolding questions, or simply taking a break. Custom writing productivity thresholds (word count and page count) can be specified by the user. A user-specific break model keeps track of when, how many, and at what frequency breaks are taken; this helps direct the user during their writing process. This functionality is available through a Chrome Extension, where the user works on a Google Doc, receiving updates and guidance in real-time. 

## Pipeline
** Backend
- Web Interface: initiates Chrome web browser for text data collection from a Google Doc
- Extract Text: completes access of user text input data using Google Docs API in real-time
- Keyboard Features: calculates number of characters, words, sentences, and user standby times (defined as the time without typing) in real-time from keyboard text input
EEG Data Collection: accesses user EEG data through the Muse headset and preprocesses data in real-time, calculating a number of features
- Machine Learning: uses an existent generalized model developed from a set of baseline users and regularly improves upon this model through fitting it with user keyboard text input and EEG data, making the model more user-specific overtime. Periodically predicts if the user will hit a roadblock. Another model is responsible for predicting the min time the user will take to complete their task.
** Frontend
- ReactJS used to develop the Chrome Extension and is responsible for custom writing productivity thresholds set by the user (word count and page count) as well as roadblock and completion notifications

## Requirements
Requirements are stored in the requirements.txt file and can be installed using the following command: pip install -r requirements.txt

## User Instructions
1. Run server through deploying runserver.py
2. On Google Chrome, login into account open Google Drive, and open Google Doc the user wishes to work on
3. Open extension through extensions icon and input desired word count and page count goals for work session
4. Begin working and keep note of roadblock notifications until you get a completion notification
