from enum import Enum


class NMEAMessageType(Enum):
    """
    Enumerated values for messages found at:
    https://www.gpsinformation.org/dale/nmea.htm
    """
    NONE = 0
    AAM = 1
    ALM = 2
    APB = 3
    BOD = 4
    BWC = 5
    GGA = 6
    GLL = 7
    GSA = 8
    GSV = 9
    MSK = 10
    MSS = 11
    RMB = 12
    RMC = 13
    RTE = 14
    VTG = 15
    WPL = 16
    XTE = 17
    ZDA = 18
