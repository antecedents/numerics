import logging

import numpy as np
import pandas as pd

import src.elements.parts as pr


class Metrics:

    def __init__(self):
        pass

    @staticmethod
    def __root_mse(data: pd.DataFrame) -> pd.DataFrame:
        """
        This function calculates
            square root (mean ( a set of square errors ) )
        per set of square errors.

        :param data:
        :return:
        """

        se: np.ndarray = np.power(data[['l_e_error', 'u_e_error']].to_numpy(), 2)
        mse = np.expand_dims(
            np.sum(se, axis=0)/se.shape[0], axis=0)

        frame = pd.DataFrame(data=np.sqrt(mse), columns=['l_e_metrics', 'u_e_metrics'], index=['r_mse'])

        return frame

    @staticmethod
    def __npe(data: pd.DataFrame) -> pd.DataFrame:
        """

        :param data:
        :return:
        """

        ner = data[['l_e_error_rate', 'u_e_error_rate']].to_numpy()
        tiles = np.percentile(a=ner, q=[10, 25, 50, 75, 90], axis=0)
        frame = pd.DataFrame(data=100*tiles, columns=['l_e_metrics', 'u_e_metrics'],
                             index=['l_whisker', 'l_quarter', 'median', 'u_quarter', 'u_whisker'])

        return frame

    def exc(self, parts: pr.Parts):
        """

        :param parts:
        :return:
        """

        data = parts.estimates
        self.__root_mse(data=data)
        self.__npe(data=data)
