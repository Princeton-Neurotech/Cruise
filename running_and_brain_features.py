import time
import numpy as np
import pandas as pd
import statistics

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
        # self.params.other_info = 0
        # self.params.file = 'C:/Users/hudso/Desktop/Princeton/NeuroTech/Our_Data/10.31.21 Colin/OpenBCISession_Colin Gamma/OpenBCI-RAW-2021-10-31_13-45-28'
        self.board = BoardShim(self.myBoardID, self.params)

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

        csv_index = 0
        while True:
            total_brain_data = brain_data_test.calc_feature_vector(myBoard.getCurrentData(1))

            if created_df is False:
                # empty dataframe with correct column names
                self.brain_df = pd.DataFrame(columns=total_brain_data[-1])
                created_df = True
                
            self.brain_df.loc[len(self.brain_df)] = total_brain_data[0] 

            # print(self.brain_df) 

            if int(time.time() - start_time) % 300 == 0.0:
                self.brain_df.to_csv(str(csv_index))
                csv_index += 1
                # every_5_min_df = self.computeData(self.brain_df)
                # print(every_5_min_df)

                # TO-DO:
                # need to substract every 5 min
                # compute mean of every column every 5s, compile into dataframe every 5 min
    
    """
    def meanData(self, brain_df):
        for col in self.brain_df:
            self.brain_df['5rSUMMARY ' + col] = self.brain_df[col].rolling(5).mean() 
        brain_training_features = self.brain_df.iloc[:, 63:126]

        return brain_training_features
    """
        
    # features are past data collected every 5 min
    # if (round(time.time() - start_time, 2)) % 300 == 0:
        # all summary columns
    # print(brain_training_features)

if __name__ == "__main__":
    myBoard = braindata(-1, 'COM3')
    myBoard.startStream()
    sampling_rate = myBoard.getSamplingRate()
    eeg_channels = myBoard.getEEGChannels()
    collect_data = myBoard.collectData()
    # compute_data = myBoard.computeData()
    myBoard.stopStream()