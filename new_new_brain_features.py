import time
import schedule 
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
        self.start_time = time.time()
        self.summation_index = 0
        self.brain_df = pd.DataFrame()
        self.summary_brain_df = pd.DataFrame()
        self.appended_summary_brain_df = pd.DataFrame()
        self.transposed_mean_appended_summary_brain_df = pd.DataFrame()
        self.dropna_appended_summary_brain_df = pd.DataFrame()
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

        # while true creates problems
        for i in range (0, 1000000):
            total_brain_data = brain_data_computations.calc_feature_vector(myBoard.getCurrentData(1))

            # empty dataframe with correct column names
            self.brain_df = pd.DataFrame(columns=total_brain_data[-1])
            # previous empty dataframe now filled with numeric data of each applied function in "brain_data_test"
            self.brain_df.loc[len(self.brain_df)] = total_brain_data[0]

            for col in self.features_list:
                self.summary_brain_df['5rSUMMARY ' + col] = self.brain_df[col] 
                self.appended_summary_brain_df = self.appended_summary_brain_df.append(self.summary_brain_df)
            self.dropna_appended_summary_brain_df = self.appended_summary_brain_df.dropna()
            # print(self.dropna_appended_summary_brain_df)
    
            # do this every 5s - for loop is preferable
            if (int(time.time() - self.start_time) % 5 == 0.0) and (int(time.time() - self.start_time) != 0):
                for col in self.features_list:
                    # summary columns of means of each column
                    mean_appended_summary_brain = self.dropna_appended_summary_brain_df.mean(axis=0)
                # mean returns a pandas series, convert back to dataframe
                mean_appended_summary_brain_df = mean_appended_summary_brain.to_frame()
                # opposite dimensions, transpose
                self.transposed_mean_appended_summary_brain_df = mean_appended_summary_brain_df.T
                # 5s of data
                # print(self.transposed_mean_appended_summary_brain_df)

                # need every 5s of data for 5 min!!!
                for self.summation_index in range (0, 60, self.summation_index):
                    brain_training_features = self.transposed_mean_appended_summary_brain_df.append(self.transposed_mean_appended_summary_brain_df)
                    print(brain_training_features)
            self.summation_index += 1
        

if __name__ == "__main__":
    myBoard = braindata(-1, 'COM3')
    myBoard.startStream()
    # myBoard.getSamplingRate()
    # myBoard.getEEGChannels()
    myBoard.collectData()
    time.sleep(5)
    myBoard.fiveSecData()
    myBoard.fiveMinData()
    # myBoard.stopStream() 