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

    def get_samplingRate(self):
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
            print("Interaxon Muse 2 is being used: MUSE2")
        return self.myBoardID

    def setBoard(self, boardID: int):
        """
        Change the ID of the Board we are using
        :param boardID: -1 for Synth, 0 for Cyton, 22 for MUSE2
        """
        self.myBoardID = boardID

    def GetDataFrame(self):
        """demo how to convert it to pandas DF and plot data
        """
        eeg_channels = BoardShim.get_eeg_channels(BoardIds.SYNTHETIC_BOARD.value)
        df = pd.DataFrame(np.transpose(self.data))
        print('Data From the Board')
        print(df.head(10))

    def collectData(self):
        """
        Collect data every 5s, organize a sliding window queue in which the window length
        is 10s and there is an overlap of 2 ie. 0-10, 5-15, 10-20 etc. for every 300s (5 min)
        """
        start_time = time.time()
        created_df = False
        
        while True:
            brain_columns = brain_data_test.calc_feature_vector(myBoard.getCurrentData(10),  "feature vectors")
            # feature_list = training_features[-1].copy()
            # first three sec lengths of lists change (unknown why) but afterwards doesn't change
            if time.time() - start_time > 3: 
                if created_df is False:
                    total_brain_data = pd.DataFrame(columns = brain_columns[-1])
                    created_df = True
                # print(total_brain_data)
                """
                goal: take the mean of every column in total_brain_data pandas dataframe for every 5s 
                (each row takes 1s to complete), then add 5s time intervals in a sliding window fashion 
                (0-10, 5-15, 10-20, etc.) for a total of 5 min (redoing this entire process every 5 min)
                current problem: can print first 5 rows, but when wanting to iterate in for or while 
                loop to print every 5 rows, stops working and prints NaN!
                """
                i = 0
                every_5s_data = []
                # for i in range (0, 295, 5): # sum every 5 rows (each row 1s) in every column for 5 min
                # while time.time() - start_time < 300:
                total_brain_data.loc[len(total_brain_data)] = brain_columns[0] 
                pd5 = total_brain_data[i:i+5]
                print(pd5.mean(axis=1)) 
                # every_5s_data.append(pd5.mean())
                # print(pd5.mean().values.tolist())
                    
            """
                all_batches = []
                data_index = 0
                for i in range (0, 60):
                    first_batch = every_5s_data[data_index] + every_5s_data[data_index + 1] # ex. 0-10
                    second_batch = every_5s_data[data_index + 1] + every_5s_data[data_index + 2] # ex. 5-15
                    all_batches.append(first_batch)
                    all_batches.append(second_batch)
                    data_index += 2
                print(all_batches)
                # print(len(brain_fv[0]),len(brain_fv[-1]))
                # print(str(str(counter1) + '_' + str(round(time.time()-start_time,2))) * 1000)
            """

if __name__ == "__main__":
    myBoard = braindata(-1, 'COM3')
    myBoard.startStream()
    sampling_rate = myBoard.get_samplingRate()
    eeg_channels = myBoard.getEEGChannels()
    current_data = myBoard.getCurrentData(10)
    collect_data = myBoard.collectData()
    myBoard.stopStream()