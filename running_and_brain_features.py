import time
import numpy as np
import pandas as pd

import brain_data_test 

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
        self.brain_training_features = []

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
        start_time = time.time()
        created_df = False
        self.csv_index = 0

        while True:
            total_brain_data = brain_data_test.calc_feature_vector(myBoard.getCurrentData(1))

            if created_df is False:
                # empty dataframe with correct column names
                self.brain_df = pd.DataFrame(columns=total_brain_data[-1])
                created_df = True
                
            # dataframe now filled with numeric data of each applied function in "brain_data_test"
            self.brain_df.loc[len(self.brain_df)] = total_brain_data[0] 
           
           
            # make csv file of all compiled data every 5 min
            # TEST RUN: OUTPUTS 15880 ROWS IN 5 MIN
            if (int(time.time() - start_time) % 10 == 0.0) and (int(time.time() - start_time) != 0):
                # convert into csv file so we can save every 5 min records
                self.brain_df.to_csv(str(self.csv_index) + ".csv")

                # read csv file and make into pandas dataframe
                every_5_min_df = pd.read_csv((str(self.csv_index) + ".csv"))

                # drop extra column that was made through process
                cols = every_5_min_df.columns[0]
                every_5_min_df.drop(columns=cols, inplace = True)

                # get rolling mean every 5s for every column and compile into summary columns
                for col in every_5_min_df:
                    # each row takes at least 0.00099s, need every 5s, need every 555 rows
                    every_5_min_df['5rSUMMARY ' + col] = every_5_min_df[col].rolling(555).mean() 
            
                # features are past data collected every 5 min, all summary columns
                self.brain_training_features = every_5_min_df.iloc[:, 63:126]
                print(self.brain_training_features)
                
                self.csv_index += 1

if __name__ == "__main__":
    myBoard = braindata(-1, 'COM3')
    myBoard.startStream()
    myBoard.getSamplingRate()
    myBoard.getEEGChannels()
    myBoard.collectData()
    myBoard.stopStream()