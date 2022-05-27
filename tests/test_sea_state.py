from nautical.sea_state import sea_state
from nautical.units.units import DistanceUnits


def test_sea_state_m_0_real():
    '''
    Test that the proper sea state value was found
    '''
    assert sea_state(0) == 0

    
def test_sea_state_m_0_negative():
    '''
    Test that the proper sea state value was found
    '''
    assert sea_state(-121312) == 0

    
def test_sea_state_m_1_real():
    '''
    Test that the proper sea state value was found
    '''
    assert sea_state(0.05) == 1

    
def test_sea_state_m_2_real():
    '''
    Test that the proper sea state value was found
    '''
    assert sea_state(0.49) == 2

    
def test_sea_state_m_3_real():
    '''
    Test that the proper sea state value was found
    '''
    assert sea_state(0.51) == 3


def test_sea_state_m_4_real():
    '''
    Test that the proper sea state value was found
    '''
    assert sea_state(2) == 4


def test_sea_state_m_5_real():
    '''
    Test that the proper sea state value was found
    '''
    assert sea_state(3.99) == 5


def test_sea_state_m_6_dang_thats_rough():
    '''
    Test that the proper sea state value was found
    '''
    assert sea_state(4.001) == 6


def test_sea_state_m_7_scared_as():
    '''
    Test that the proper sea state value was found
    '''
    assert sea_state(7.5) == 7


def test_sea_state_m_8_scared_to_death():
    '''
    Test that the proper sea state value was found
    '''
    assert sea_state(12) == 8


def test_sea_state_m_9_god_save_us_all():
    '''
    Test that the proper sea state value was found
    '''

    assert sea_state(123123123) == 9

    
def test_sea_state_other_feet():
    '''
    Test that the proper sea state can be found given a different unit
    below and above the value of meters.
    '''
    assert sea_state(6.234, DistanceUnits.FEET) == 4

def test_sea_state_other_miles():
    '''
    Test that the proper sea state can be found given a different unit
    below and above the value of meters.
    '''
    assert sea_state(0.0028353168, DistanceUnits.MILES) == 6

