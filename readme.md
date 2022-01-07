# Roadblocks Project
Users complete a provided writing prompt and we measure keyboard input and brain data as they write. We develop a machine learning model that predicts when the user will approach a roadblock based on keyboard input and brain data. A roadblock is defined as if the user cannot hit a minimum goal before 5 minutes. If the user hits a roadblock we can offer helpful alternatives such as reading articles related to their keywords or taking a break.
 
The general pipeline involved in this project is:
- Realtime Program: develop a program that can keep track of number of characters, words, sentences, and standby times (defined as if the user has not typed for 1 minute) in real time 
- GUI: Developing a graphical user interface to complement the above program
- Machine Learning:
   - Keyboard Input Features: defined by previous word count, change in word count, words produced, and words deleted
   - Brain Data Features: defined by a variety of computations such as mean, standard deviation, skewness, kurtosis, maximum, minimum, covariance matrix, eigenvalues of    covariance matrix, and fast fourier transform
   - Label: words typed in the future 5 minutes
   - Model: merge keyboard input and brain data feature vectors and train model (Random Forest Regressor) to predict when user is approaching a roadblock
