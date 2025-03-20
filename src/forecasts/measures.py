"""Module measures.py"""
import logging
import os
import json

import numpy as np
import pandas as pd

import src.elements.parts as pr
import config

import src.functions.objects


class Measures:

    def __init__(self):
        """

        """

        self.__configurations = config.Config()
        self.__path = os.path.join(self.__configurations.warehouse, 'forecasts')

        # Instance for writing/reading JSON (JavaScript Object Notation) items.
        self.__objects = src.functions.objects.Objects()

        # Graphing fields; minimal is for futures parts, which do not include error measures because
        # their true values are yet unknown.
        self.__reference = ['milliseconds', 'n_attendances', 'l_estimate', 'u_estimate', 'l_e_error', 'u_e_error',
                            'l_e_error_rate', 'u_e_error_rate']
        self.__minimal = ['milliseconds', 'n_attendances', 'l_estimate', 'u_estimate']

    @staticmethod
    def __errors(data: pd.DataFrame) -> pd.DataFrame:
        """

        :param data: The forecasts w.r.t. training or testing phases.
        :return:
        """

        # ground truth
        ground = data['n_attendances'].to_numpy()[:,None]

        # forecasts
        forecasts = data[['l_estimate', 'u_estimate']].to_numpy()

        # raw errors and error rates; negative/lower, positive/higher
        errors: np.ndarray =  forecasts - ground
        data.loc[:, ['l_e_error', 'u_e_error']] = errors
        data.loc[:, ['l_e_error_rate', 'u_e_error_rate']] = np.true_divide(errors, ground)

        return data

    def __get_node(self, blob: pd.DataFrame) -> dict:
        """

        :param blob: 
        :return:
        """

        string: str = blob.to_json(orient='split')

        return json.loads(string)

    def __persist(self, nodes: dict, code: str):
        """

        :param nodes: An institution's data dictionary consisting of forecasts w.r.t. training,
                      testing, and futures parts; <b>alongside error measures</b>.<br>
        :param code: An institution's identification code.<br>
        :return:
        """

        message = self.__objects.write(nodes=nodes, path=os.path.join(self.__path, f'{code}.json'))

        logging.info('Forecasts Values & Measures -> %s', message)

    def exc(self, parts: pr.Parts, code: str) -> pr.Parts:
        """

        :param parts: An institution's data object consisting of forecasts w.r.t. training,
                      testing, and futures parts.<br>
        :param code: An institution's identification code.<br>
        :return:
        """

        parts = parts._replace(estimates=self.__errors(data=parts.estimates.copy()),
                       tests=self.__errors(data=parts.tests.copy()))

        nodes = {
            'estimates': self.__get_node(parts.estimates[self.__reference]),
            'tests': self.__get_node(parts.tests[self.__reference]),
            'futures': self.__get_node(parts.futures[self.__minimal])}
        self.__persist(nodes=nodes, code=code)

        return parts
