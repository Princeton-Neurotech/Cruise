# HAVE ONE DATAFRAME THAT APPENDS:  brain_data_computations.calc_feature_vector(myBoard.getCurrentData(1))
# CONSTANTLY
# ROWS SYMBOLIZE 
# UNITED DATAFRAME HAS ONE ROW FOR EACH 5 SECONDS KEEPS GROWING
# BRAIN DATA PART: FEATURE VECTOR FOR LAST 5 SECONDS
# KEYBOARD DATA PART: LAST ROW OF KEYBOARD DATAFRAME (APPROX 5 SEC)

#THEN 



import time
import sched
import numpy as np
import pandas as pd

import brain_data_computations

import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations

class braindata:

    def __init__(self, boardID=-1, serial=''):
        self.isRunning = False
        self.myBoardID = boardID
        BoardShim.enable_dev_board_logger()
        self.params = BrainFlowInputParams()
        self.params.serial_port = serial
        # parameters for playing back a file
        # self.params.other_info = 0 # board id of headset used in file
        # self.params.file = 'OpenBCI-RAW-2021-10-31_13-45-28' # file name
        self.board = BoardShim(self.myBoardID, self.params)
        self.brain_training_features = pd.DataFrame()
        self.compressed_brain_training_features = pd.DataFrame()
        self.features_list = ['mean_0', 'mean_d_h2h1_0', 'mean_q1_0', 'mean_q2_0', 'mean_q3_0',
        'mean_q4_0', 'mean_d_q1q2_0', 'mean_d_q1q3_0', 'mean_d_q1q4_0',
        'mean_d_q2q3_0', 'mean_d_q2q4_0', 'mean_d_q3q4_0', 'std_0',
        'std_d_h2h1_0', 'max_0', 'max_d_h2h1_0', 'max_q1_0', 'max_q2_0',
        'max_q3_0', 'max_q4_0', 'max_d_q1q2_0', 'max_d_q1q3_0', 'max_d_q1q4_0',
        'max_d_q2q3_0', 'max_d_q2q4_0', 'max_d_q3q4_0', 'min_0', 'min_d_h2h1_0',
        'min_q1_0', 'min_q2_0', 'min_q3_0', 'min_q4_0', 'min_d_q1q2_0',
        'min_d_q1q3_0', 'min_d_q1q4_0', 'min_d_q2q3_0', 'min_d_q2q4_0',
        'min_d_q3q4_0', 'topFreq_1_0', 'topFreq_2_0', 'topFreq_3_0',
        'topFreq_4_0', 'topFreq_5_0', 'topFreq_6_0', 'topFreq_7_0',
        'topFreq_8_0', 'topFreq_9_0', 'topFreq_10_0', 'freq_011_0',
        'freq_021_0', 'freq_032_0', 'freq_043_0', 'freq_053_0', 'freq_064_0',
        'freq_075_0', 'freq_085_0', 'freq_096_0', 'freq_107_0', 'freq_117_0',
        'freq_128_0', 'freq_139_0', 'freq_149_0', 'freq_160_0']
        self.feature_summ_list = ['5rSUMMARY mean_0',
                '5rSUMMARY mean_d_h2h1_0',
                '5rSUMMARY mean_q1_0',
                '5rSUMMARY mean_q2_0',
                '5rSUMMARY mean_q3_0',
                '5rSUMMARY mean_q4_0',
                '5rSUMMARY mean_d_q1q2_0',
                '5rSUMMARY mean_d_q1q3_0',
                '5rSUMMARY mean_d_q1q4_0',
                '5rSUMMARY mean_d_q2q3_0',
                '5rSUMMARY mean_d_q2q4_0',
                '5rSUMMARY mean_d_q3q4_0',
                '5rSUMMARY std_0',
                '5rSUMMARY std_d_h2h1_0',
                '5rSUMMARY max_0',
                '5rSUMMARY max_d_h2h1_0',
                '5rSUMMARY max_q1_0',
                '5rSUMMARY max_q2_0',
                '5rSUMMARY max_q3_0',
                '5rSUMMARY max_q4_0',
                '5rSUMMARY max_d_q1q2_0',
                '5rSUMMARY max_d_q1q3_0',
                '5rSUMMARY max_d_q1q4_0',
                '5rSUMMARY max_d_q2q3_0',
                '5rSUMMARY max_d_q2q4_0',
                '5rSUMMARY max_d_q3q4_0',
                '5rSUMMARY min_0',
                '5rSUMMARY min_d_h2h1_0',
                '5rSUMMARY min_q1_0',
                '5rSUMMARY min_q2_0',
                '5rSUMMARY min_q3_0',
                '5rSUMMARY min_q4_0',
                '5rSUMMARY min_d_q1q2_0',
                '5rSUMMARY min_d_q1q3_0',
                '5rSUMMARY min_d_q1q4_0',
                '5rSUMMARY min_d_q2q3_0',
                '5rSUMMARY min_d_q2q4_0',
                '5rSUMMARY min_d_q3q4_0',
                '5rSUMMARY topFreq_1_0',
                '5rSUMMARY topFreq_2_0',
                '5rSUMMARY topFreq_3_0',
                '5rSUMMARY topFreq_4_0',
                '5rSUMMARY topFreq_5_0',
                '5rSUMMARY topFreq_6_0',
                '5rSUMMARY topFreq_7_0',
                '5rSUMMARY topFreq_8_0',
                '5rSUMMARY topFreq_9_0',
                '5rSUMMARY topFreq_10_0',
                '5rSUMMARY freq_011_0',
                '5rSUMMARY freq_021_0',
                '5rSUMMARY freq_032_0',
                '5rSUMMARY freq_043_0',
                '5rSUMMARY freq_053_0',
                '5rSUMMARY freq_064_0',
                '5rSUMMARY freq_075_0',
                '5rSUMMARY freq_085_0',
                '5rSUMMARY freq_096_0',
                '5rSUMMARY freq_107_0',
                '5rSUMMARY freq_117_0',
                '5rSUMMARY freq_128_0',
                '5rSUMMARY freq_139_0',
                '5rSUMMARY freq_149_0',
                '5rSUMMARY freq_160_0']

        self.brain_df = pd.DataFrame(columns=self.features_list)


    def startStream(self):
        """
        Tells the bord to being streaming data
        """
        BoardShim.enable_dev_board_logger()
        self.board.prepare_session()
        # initiate stream
        self.board.start_stream(45000, '')
        self.isRunning = True
        self.board.log_message(LogLevels.LEVEL_INFO, "Start sleeping in the main thread")
        # time.sleep(sleepTime)  # sleep 30 seconds
        # get the data
        self.data = self.board.get_board_data()

    def getData(self):
        """
        Gets the data from the board (presumably all of it since stream
        was started
        :return: The data from the board
        """
        return self.board.get_board_data()

    def getCurrentData(self, num_samples: int):
        """
        Gets the current (updated) data from the board
        :param num_samples: The amount of samples the returned ndarray will hold
        :return: The current board data
        """
        return self.board.get_current_board_data(num_samples)

    def getSamplingRate(self):
        """
        Get the rate at which the board samples data
        (i.e.: The muse has an SR of about 256 Hz
        :return: The sampling rate of a certain board
        """
        return self.board.get_sampling_rate(self.myBoardID)

    def getEEGChannels(self):
        """
        Gets the EEG channels from the board being used
        :return: The amt of channels for streaming EEG on the board
        """
        return self.board.get_eeg_channels(self.myBoardID)

    def stopStream(self):
        """
        Tells the board to stop streaming data
        """
        if self.isRunning:
            print('Stopping Stream')
            self.board.stop_stream()
            self.board.release_session()
        else:
            print("BOARD WAS NEVER STARTED")

    def run(self, streamTime: int):
        """
        Tells the board to run a specific test for a specific amt of time
        [FOR DEBUGGING]
        :param streamTime: The time the board will be streaming
        """
        BoardShim.enable_dev_board_logger()
        params = BrainFlowInputParams()

        # BOARD IDs internally in brainflow
        SYNTH_BOARD = int(-1)
        CYTON = int(0)
        MUSE2 = int(22)

        myCytonSerialPort = 'COM3'
        noSerial = ''

        params.serial_port = noSerial

        # create our board
        # board = BoardShim(SYNTH_BOARD, params)
        board = BoardShim(self.myBoardID, params)
        board.prepare_session()

        # initiate stream
        board.start_stream(45000, '')
        board.log_message(LogLevels.LEVEL_INFO, "Start sleeping in the main thread")
        time.sleep(streamTime)  # sleep 30 seconds

        # get the data
        self.data = board.get_board_data()

        # board.stop_stream()
        # board.release_session()

        print(self.data)  # for now print the data we can write it to a file

    def getBoard(self):
        """
        Lets us know what board we are using
        :return: The id of the board being used
        """
        if self.myBoardID == -1:
            print("Default Board is being used: SYNTHETIC")
        elif self.myBoardID == 0:
            print("OpenBCI Cyton is being used: CYTON")
        elif self.myBoardID == 22:
            print("Interaxon Muse 2 with bluetooth dongle is being used: MUSE2")
        elif self.myBoardID == 38:
            print("Interaxon Muse 2 without bluetooth dongle is being used: MUSE2")
        return self.myBoardID

    def setBoard(self, boardID: int):
        """
        Change the ID of the Board we are using
        :param boardID: -1 for Synth, 0 for Cyton, 22 for MUSE2
        """
        self.myBoardID = boardID

    def collectData(self):
        """
            Collect data, taking mean, every 5s, organize a sliding window queue in which the window 
            length is 10s and there is an overlap of 2 ie. 0-10, 5-15, 10-20 etc. for every 300s (5 min). 
        """ 
        myBoard = braindata(-1, 'COM3')

        # run process every 10s
        # event_schedule = sched.scheduler(time.time, time.sleep(10))
        # event_schedule.run()

        start_time = time.time()
        created_df = False
        self.csv_index = 0
        self.raw_brain_df = []

        # while true creates problems
        for i in range (0, 1000000):
            total_brain_data = brain_data_computations.calc_feature_vector(myBoard.getCurrentData(1))


            if len(total_brain_data[0]) == 63:
                self.brain_df.loc[len(self.brain_df)] = total_brain_data[0] 
                

    
                #if created_df is False:
                    # empty dataframe with correct column names
                    #self.brain_df = pd.DataFrame(columns=total_brain_data[-1])
                    #created_df = True
                    
                # previous empty dataframe now filled with numeric data of each applied function in "brain_data_test"
                #self.brain_df.loc[len(self.brain_df)] = total_brain_data[0] 
                
                # make csv file of all compiled data every 5 min - take every 650th row
                if (int(time.time() - start_time) % 10 == 0.0) and (int(time.time() - start_time) != 0):
                    # convert into csv file so we can save every 5 min records
                    #every_5_min_df = pd.read_csv((str(self.csv_index) + ".csv"))
                    self.every_5_min_df = pd.DataFrame({})
                    for col in self.features_list:
                        self.every_5_min_df['5rSUMMARY ' + col] = self.brain_df[col].rolling(5).mean() # rolling mean is # of rows mean and then goes down by 1 and does so again
                    

                    #self.brain_df.to_csv(str(self.csv_index) + ".csv")

                    # read csv file and make into pandas dataframe
                    

                    # drop extra column that was made through process
                    #cols = every_5_min_df.columns[0]
                    #every_5_min_df.drop(columns=cols, inplace = True)

                    # get rolling mean every 650 rows for every column and compile into summary columns
                    # 7800th rows for 1 hr
                    #for col in self.features_list:
                    #    every_5_min_df['5rSUMMARY ' + col] = every_5_min_df[col].rolling(21).mean() # rolling mean is # of rows mean and then goes down by 1 and does so again
                
                    # features are past data collected every 5 min, all summary columns
                    self.brain_training_features = self.every_5_min_df.iloc[:, 63:126]
                    
                    for i in range (0, 60):
                        # take every 400th row
                        self.compressed_brain_training_features = self.compressed_brain_training_features.append(self.brain_training_features.iloc[[10*i],:]) 
                    print(self.compressed_brain_training_features)

                    # convert into csv file so we can save every 5 min records
                    self.compressed_brain_training_features.to_csv("brain " + str(self.csv_index) + ".csv")
                    self.csv_index += 1

if __name__ == "__main__":
    myBoard = braindata(-1, 'COM3')
    myBoard.startStream()
    # print(myBoard.getSamplingRate())
    # print(myBoard.getEEGChannels())
    myBoard.collectData()
    # myBoard.stopStream()