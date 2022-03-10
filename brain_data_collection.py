from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels
from brainflow.data_filter import DataFilter
import brainflow
import brain_data_computations
import time
import numpy as np
import pandas as pd
from scipy import signal

from sys import exit
import warnings
warnings.filterwarnings('ignore')

class braindata:

    def __init__(self, boardID=38, serial='dev/cu.usbserial-DM03H3ZF'):
        self.isRunning = False
        self.myBoardID = boardID
        BoardShim.enable_dev_board_logger()
        self.params = BrainFlowInputParams()
        self.params.serial_port = serial
        # parameters for playing back a file
        # self.params.other_info = 0 # board id of headset used in file
        # self.params.file = 'OpenBCI-RAW-2021-10-31_13-45-28' # file name
        self.board = BoardShim(self.myBoardID, self.params)
        self.global_muse_data = pd.DataFrame()

    def startStream(self):
        """
        Tells the bord to being streaming data
        """
        BoardShim.enable_dev_board_logger()
        self.board.prepare_session()
        # initiate stream
        self.board.start_stream(45000, '')
        self.isRunning = True
        self.board.log_message(LogLevels.LEVEL_INFO,
                               "Start sleeping in the main thread")
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

        myCytonSerialPort = 'dev/'
        noSerial = ''

        params.serial_port = noSerial

        # create our board
        # board = BoardShim(SYNTH_BOARD, params)
        board = BoardShim(self.myBoardID, params)
        board.prepare_session()

        # initiate stream
        board.start_stream(45000, '')
        board.log_message(LogLevels.LEVEL_INFO,
                          "Start sleeping in the main thread")
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
        myBoard = braindata(38, 'dev/cu.usbserial-DM03H3ZF')

        for i in range (0, 10000000):
            eeg_channels = braindata.getEEGChannels(self)

            # get all columns of raw data for 5s time period
            total_brain_data = myBoard.getCurrentData(1)

            # only choose columns 1-9 for openbci data
            openbci_brain_data = total_brain_data[1:9]
            # only choose columns 1-4 for muse data
            # ['TP9', 'AF7', 'AF8', 'TP10', 'Right AUX']
            muse_brain_data = total_brain_data[1:5]

            # create initial csv file for records 
            np.savetxt('brain.csv', muse_brain_data.T, delimiter=",")

            for count, channel in enumerate(eeg_channels):
                # bandpass filter to remove any other existing artifacts
                DataFilter.perform_bandpass(muse_brain_data[count], 250, 22, 45, 2, FilterTypes.BESSEL.value, 0)

            muse_brain_data_df = pd.DataFrame(muse_brain_data)
            self.global_muse_data = pd.concat([self.global_muse_data, muse_brain_data_df.T])
            print(self.global_muse_data)

# macos openbci port: /dev/cu.usbserial-DM03H3ZF
if __name__ == "__main__":
    myBoard = braindata(38, 'dev/cu.usbserial-DM03H3ZF')
    myBoard.startStream()
    # myBoard.getSamplingRate()
    # myBoard.getEEGChannels()
    myBoard.collectData()
    # myBoard.stopStream()
