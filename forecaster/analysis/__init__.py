from forecaster.wave_data import WaveData


def analyze_wave_height(data, observations = 1) -> str:
    """
    Provide a string to the user that describes what the data has done over the last x hours
    :param data: list of wave data points in half hour increments
    :param observations: number of data points to compare, defaults to 1 if larger than data or smaller that 1
    :return: string describing the data
    """
    obs = 1 if observations > len(data) or observations < 1 else observations

    fdata = []
    for x in range(obs):
        try:
            f = float(data[x].wvht)
            fdata.append(f)
        except ValueError:
            continue

    total = 0
    for x in fdata:
        total = total + x
    total = total / obs

    if fdata[0] > total:
        return "Over the last {} hours the wave height has increased about {} feet".format(int(obs/2), fdata[0]-total)
    elif fdata[0] < total:
        return "Over the last {} hours the wave height has decreased about {} feet".format(int(obs / 2), total-fdata[0])
    else:
        return "Over the last {} hours the wave height has remained constant {} feet".format(int(obs/2), fdata[0])


def analyze_water_temp(data, observations=1) -> str:
    """
    Provide a string to the user that describes what the data has done over the last x hours
    :param data: list of wave data points in half hour increments
    :param observations: number of data points to compare, defaults to 1 if larger than data or smaller that 1
    :return: string describing the data
    """
    obs = 1 if observations > len(data) or observations < 1 else observations

    fdata = []
    for x in range(obs):
        try:
            f = float(data[x].wtmp)
            fdata.append(f)
        except ValueError:
            continue

    total = 0
    for x in fdata:
        total = total + x
    total = total / obs

    if fdata[0] > total:
        return "Over the last {} hours the water temperature has increased about {} Deg F".format(int(obs / 2), fdata[0] - total)
    elif fdata[0] < total:
        return "Over the last {} hours the water temperature has decreased about {} Deg F".format(int(obs / 2), total - fdata[0])
    else:
        return "Over the last {} hours the water temperature has remained constant {} Deg F".format(int(obs / 2), fdata[0])


def analyze_dominant_wave_period(data, observations=1) -> str:
    """
    Provide a string to the user that describes what the data has done over the last x hours
    :param data: list of wave data points in half hour increments
    :param observations: number of data points to compare, defaults to 1 if larger than data or smaller that 1
    :return: string describing the data
    """
    obs = 1 if observations > len(data) or observations < 1 else observations

    fdata = []
    for x in range(obs):
        try:
            f = float(data[x].dpd)
            fdata.append(f)
        except ValueError:
            continue

    total = 0
    for x in fdata:
        total = total + x
    total = total / obs

    if fdata[0] > total:
        return "Over the last {} hours the dominant wave period has increased about {} secs".format(int(obs / 2), fdata[0] - total)
    elif fdata[0] < total:
        return "Over the last {} hours the dominant wave period has decreased about {} secs".format(int(obs / 2), total - fdata[0])
    else:
        return "Over the last {} hours the dominant wave period has remained constant {} secs".format(int(obs / 2), fdata[0])


def analyze_avg_wave_period(data, observations=1):
    """
    Provide a string to the user that describes what the data has done over the last x hours
    :param data: list of wave data points in half hour increments
    :param observations: number of data points to compare, defaults to 1 if larger than data or smaller that 1
    :return: string describing the data
    """
    obs = 1 if observations > len(data) or observations < 1 else observations

    fdata = []
    for x in range(obs):
        try:
            f = float(data[x].apd)
            fdata.append(f)
        except ValueError:
            continue

    total = 0
    for x in fdata:
        total = total + x
    total = total / obs

    if fdata[0] > total:
        return "Over the last {} hours the avg wave period has increased about {} secs".format(int(obs / 2), fdata[0] - total)
    elif fdata[0] < total:
        return "Over the last {} hours the avg wave period has decreased about {} secs".format(int(obs / 2), total - fdata[0])
    else:
        return "Over the last {} hours the avg wave period has remained constant {} secs".format(int(obs / 2), fdata[0])
