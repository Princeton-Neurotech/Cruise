# HAVE ONE DATAFRAME THAT APPENDS: brain_data_computations.calc_feature_vector(myBoard.getCurrentData(1))
# CONSTANTLY
# ROWS SYMBOLIZE 5 SEC
# UNITED DATAFRAME HAS ONE ROW FOR EACH 5 SECONDS KEEPS GROWING
# BRAIN DATA PART: FEATURE VECTOR FOR LAST 5 SECONDS
# KEYBOARD DATA PART: LAST ROW OF KEYBOARD DATAFRAME (APPROX 5 SEC)

# 1 keyboard row happens every 5s? 
# brain data: very multiple of 5 of time, append set of rows and however many rows are appended
# in that time take the mean and in all those meaned rows will be 60 rows
# keyboard is lists, but can't we append the same way to a dataframe? not sure 

import time
import numpy as np
import pandas as pd

import brain_data_computations

import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations

class braindata:

    def __init__(self, boardID=-1, serial=''):
        self.start_time = time.time()
        self.created_df = False
        self.check_5 = False
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
            Collect raw data, perform computations, add row every 5s that contains rolling mean, 
            do this for 5 min so it results in 60 rows by 63 columns
        """ 
        myBoard = braindata(-1, 'COM3')
        self.csv_index = 0

        # while True:
        for i in range (0, 1000000):
            if (int(time.time() - self.start_time) % 5 == 0.0):
                # self.check_5 = True
            # elif (int(time.time() - self.start_time) % 5 == 0.0) and self.check_5 == True:
                # perform computations contained in "brain_data_test"
                # np array of values, list of column names
                total_brain_data = brain_data_computations.calc_feature_vector(myBoard.getCurrentData(1))
                # print(total_brain_data[0])

                if self.created_df is False:
                    # empty dataframe with correct column names
                    self.brain_df = pd.DataFrame(columns=total_brain_data[-1])
                    self.created_df = True

                # fill dataframe with numeric data of each applied function in "brain_data_test"
                if len(total_brain_data[0]) == 63:
                    self.brain_df.loc[len(self.brain_df)] = total_brain_data[0]
                    # 1 by 63 dataframe - want 1 row every 5s so 60 by 63 after 5 min
                # print(self.brain_df)

                # convert into csv file so we can save every 5 min records
                # self.brain_df.to_csv("brain " +str(self.csv_index) + ".csv")
                # self.csv_index += 1

                # self.check_5 = False

                for i in range (0, 63):
                    for col in self.features_list:
                        # calculate number of rows we need to mean to get 60 rows each worth 5 min
                        # need to multiply index so rows go down by calculated number, not just 1
                        self.brain_df['5rSUMMARY ' + col] = self.brain_df[col].rolling(10*i).mean()
                    
                    # features are past data collected every 5 min, choose only summary columns
                    self.brain_training_features = self.brain_df.iloc[:, 63:126]
                print(self.brain_training_features)
                
                """
                # outputs total of 60 rows in 5 min, 1 row every 5s
                if (int(time.time() - self.start_time) % 5 == 0.0):
                    for i in range (0, 60):
                        # take every 400th row
                        self.compressed_brain_training_features = self.compressed_brain_training_features.append(self.brain_training_features.iloc[[10*i],:]) 
                        # update and return every 5s - outputs 1 row every 5s
                        # return self.compressed_brain_training_features
                    print(self.compressed_brain_training_features)
                """

        # add one row of self.brain_df's summary columns every 5s
        # self.brain_training_features = self.brain_df[[self.feature_summ_list]]
        # print(self.brain_training_features)
 
# if __name__ == "__main__":
    # myBoard = braindata(-1, 'COM3')
    # myBoard.startStream()
    # print(myBoard.getSamplingRate())
    # print(myBoard.getEEGChannels())
    # myBoard.collectData()
    # myBoard.stopStream()