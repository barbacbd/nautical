
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

            if "units" in str(k):
                continue

            units = getattr(self, k+"_units")
            if units is not None:
                ret = ret + "{} = {} {}\n".format(k, v, units)
            else:
                ret = ret + "{} = {}\n".format(k, v)

        return ret


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




