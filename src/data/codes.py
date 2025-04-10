"""Module codes.py"""
import glob
import os
import pathlib

import config


class Codes:
    """
    <b>Notes</b><br>
    ------<br>
    Determines the institutions list.<br>
    """

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()
        self.__path_m = os.path.join(self.__configurations.data_, 'models')
        self.__path_d = os.path.join(self.__configurations.data_, 'data')

    def __get_codes(self) -> list[str] | None:
        """

        :return:
        """

        listings = glob.glob(pathname=os.path.join(self.__path_m, '**'))
        stems = [os.path.basename(listing) for listing in listings]

        codes = []
        for stem in stems:
            state = (pathlib.Path(os.path.join(self.__path_m, stem, 'scf_estimates.json')).exists() &
                     pathlib.Path(os.path.join(self.__path_m, stem, 'tcf_forecasts.csv')).exists() &
                     pathlib.Path(os.path.join(self.__path_d, stem, 'data.csv')).exists() &
                     pathlib.Path(os.path.join(self.__path_d, stem, 'features.csv')).exists())
            if state:
                codes.append(stem)
        return codes

    def exc(self) -> list[str] | None:
        """

        :return:
        """

        return self.__get_codes()
