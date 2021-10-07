from .base import BaseNMEA0183
from .dpt import DPT
from .gga import GGA
from .gst import GST
from .hdt import HDT
from .mwv import MWV
from .pashr import PASHR
from .rmc import RMC
from .rot import ROT
from .vhw import VHW
from .vtg import VTG
from .zda import ZDA
#import inspect
#from sys import modules

# TODO
#def init_nmea_message(sentence):
#    _adjusted = sentence.replace('\n', '').replace('\r', '')
#    message_type = find_sentence_type(sentence)
#    [m[0] for m in inspect.getmembers(modules[__name__], inspect.isclass) if m[1].__module__ == modules[__name__])

def create_nmea_message(sentence):
    """
    Create a NMEA Message instance from the string formatted NMEA sentence.

    :param sentence: Suspected NMEA Sentence.
    :returns: Specific NMEA sentence where the message is parsed when successful. When
    an unknown message or a failed message arrives, None is returned
    """
    _adjusted = sentence.replace('\n', '').replace('\r', '')

    try:
        message_type = find_sentence_type(sentence)

        for _nm in (DPT, GGA, GST, HDT, MWV, PASHR, RMC, ROT, VHW, VTG, ZDA):
            if _nm.__name__ in message_type:
                return _nm(_adjusted)

    except (IndexError, TypeError, NotImplementedError) as e:
        return None


def find_sentence_type(message):
    """
    All empty strings and `-` will be removed. The returned type will include
    the talker id.

    :param message: suspected NMEA 0183 Sentence
    :return: NMEA 0183 message type
    """
    idx = message.find("$")
    
    if idx < 0:
        return None
        
    return message[idx:].split(",")[0].replace("$", "").replace("-", "")
        

__all__ = [
    'create_nmea_message',
    'find_sentence_type',
    'BaseNMEA0183',
    'DPT',
    'GGA',
    'GST',
    'HDT',
    'MWV',
    'PASHR',
    'RMC',
    'ROT',
    'VHW',
    'VTG',
    'ZDA'
]
