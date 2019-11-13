
class NOAAData(object):

    def __str__(self) -> str:
        """
        It appears that all of the attributes that we added through setattr are stored in
        a dictionary called self.__dict__ ... let's loop over that to print out the
        attrivutes that we have stored.

        NOTE: just in case, we can filter out some of our values here if we wanted to
        by making sure that no private variables are displayed ... filter for the __
        inside of the key (leaving this out for now though)

        :return: string representation of this object
        """
        ret = ""
        for k, v in self.__dict__.items():
            ret = ret + "{} = {}\n".format(k, v)

        return ret

    def __setattr__(self, key, value):
        """
        Probably don't neeed to override this function, but for debugging purposes I will leave
        this hear in case the user wishes to print out the data as it is set.

        We will not keep values that are empty

        We will also not keep blank values that NOAA stores as - on their website

        :param key: dictionary key the attirbute is stored as
        :param value: value of the attribute
        :return: None
        """

        if value is None or value == '-':
            return

        # print("WaveData {} = {}".format(key, value))
        super().__setattr__(key, value)


class CombinedNOAAData:

    def  __init__(self) -> None:
        """
        This class is meant to serve as the combination of past and present NOAA
        data for a particular buoy location. This will will include:

        present wave data
        present swell data
        past data [currently wave data and swell data]
        """
        self.present_wave_data = None
        self.present_swell_data = None
        self.past_data = None




