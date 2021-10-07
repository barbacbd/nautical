from enum import IntEnum

# TODO: add to the class below
def talker_from_string(data):
    """
    :param data: String that may or may not contain the Talker
    ID for the message
    :return: TalkingIdentifier if found, otherwise None
    """

    if data.startswith("$"):
        _data = data[1:]
    else:
        _data = data

    for tk in TalkerIdentifier:
        if _data.startswith(str(tk.name)):
            return tk

    return None


class TalkerIdentifier(IntEnum):
    """
    Enumeration for 0183 Talker Identifier Mnemonics
    """
    AB = 0   # Independent AIS Base Station
    AD = 1   # Dependent AIS Base Station
    AG = 2   # Heading Track Controller (autopilot): General
    AP = 3   # Heading Track Controller (autopilot): Magnetic
    AI = 4   # Mobile Class A or B AIS Station
    AN = 5   # AIS Aids to Navigation Station
    AR = 6   # AIS Receiving Station
    AS = 7   # AIS Station (ITU_R M1371, ("Limited Base Station")
    AT = 8   # AIS Transmitting Station
    AX = 9   # AIS Simplex Repeater Station
    BI = 10  # Bilge Systems
    BN = 11  # Bridge Navigational Watch Alarm System
    CA = 12  # Central Alarm Management
    CD = 13  # Digital Selective Calling (DSC)
    CR = 14  # Date Receiver
    CS = 15  # Satellite
    CT = 16  # Radio-Telephone (MF/HF)
    CV = 17  # Radio-Telephone (VHF)
    CX = 18  # Scanning Receiver
    DF = 19  # Direction Finder
    DU = 20  # Duplex Repeater Station
    DP = 21  # Dynamic Position
    EC = 22  # Electronic Chart System (ECS)
    EI = 23  # Electronic Chart Display and Information Systems (ECDIS)
    EP = 24  # Emergency Position Indicating Beacon (EPIRB)
    ER = 25  # Engine Room Monitoring Systems
    FD = 26  # Fire Door Controller/Monitoring Point
    FE = 27  # Fire Extinguisher System
    FR = 28  # Fire Detection Point
    FS = 29  # Fire Sprinkler System
    GA = 30  # Galileo Positioning System
    GB = 31  # BDS (BeiDou System)
    GI = 32  # NavIC (IRNSS)
    GL = 33  # GLONASS Receiver
    GN = 34  # Global Navigation Satellite System (GNSS)
    GP = 35  # Global Positioning System (GPS)
    GQ = 36  # QZSS
    HC = 37  # Compass, Magnetic
    HE = 38  # Gyro, North Seeking
    HF = 39  # Fluxgate
    HN = 40  # Gyro, Non-North Seeking
    HD = 41  # Hull Door Controller/Monitoring Panel
    HS = 42  # Hull Stress Monitoring
    II = 43  # Integrated Instrumentation
    IN = 44  # Integrated Navigation
    JA = 45  # Alarm and Monitoring System (reserved for future use)
    JB = 46  # Reefer Monitoring System (reserved for future use)
    JC = 47  # Power Management System (reserved for future use)
    JD = 48  # Propulsion Control System (reserved for future use)
    JE = 49  # Engine Control Console (reserved for future use)
    JF = 50  # Propulsion Boiler (reserved for future use)
    JG = 51  # Auxiliary Boiler (reserved for future use)
    JH = 52  # Electronic Governor System (reserved for future use)
    LC = 53  # Loran C
    MX = 54  # Multiplexer
    NL = 55  # Navigation Light Controller
    NV = 56  # Night Vision
    P = 57   # Proprietary Code
    RA = 58  # Radar and/or Radar Plotting
    RB = 59  # Record Book (reserved for future use)
    RC = 60  # Propulsion Machinery Including Remote Control
    RI = 61  # Rudder Angle Indicator (reserved for future use)
    SA = 62  # Physical Shore AIS Station
    SC = 63  # Steering Conrtol System/Device (reserved for future use)
    SD = 64  # Sounder, depth
    SG = 65  # Steering Gear/Steering Engine
    SN = 66  # Electronic Positioning System, other/general
    SS = 67  # Sounder, scanning
    TC = 68  # Track Control System (reserved for future use)
    TI = 69  # Turn Rate Indicator
    UP = 70  # Microprocessor Controller
    U1 = 71  # User confirmed talker identifier
    U2 = 72  # User confirmed talker identifier
    U3 = 73  # User confirmed talker identifier
    U4 = 74  # User confirmed talker identifier
    U5 = 75  # User confirmed talker identifier
    U6 = 76  # User confirmed talker identifier
    U7 = 77  # User confirmed talker identifier
    U8 = 78  # User confirmed talker identifier
    VD = 79  # Doppler, other/general
    VM = 80  # Speed Log, Water, Magnetic
    VW = 81  # Speed Log, Water Mechanical
    VA = 82  # ASM
    VS = 83  # Satellite
    VT = 84  # Terrestrial
    VR = 85  # Voyage Data Recorder
    WD = 86  # Watertight Door Controller/Moniroting Panel
    WI = 87  # Weather Instruments
    WL = 88  # Water Level Detection Systems
    YX = 89  # Transducer
    ZA = 90  # Atomics Clock
    ZC = 91  # Chronometer
    ZQ = 92  # Quartz
    ZV = 93  # Radio Update
