"""Module interface.py"""

import typing

import pandas as pd

import src.data.codes
import src.data.menu
import src.data.reference
import src.data.specifications
import src.elements.s3_parameters as s3p
import src.elements.specifications as se


class Interface:
    """
    Notes<br>
    ------<br>

    An interface to the data/artefacts retrieval class.  <b>Beware, sometimes dask
    will be unnecessary, edit accordingly.</b>
    """

    def __init__(self, s3_parameters: s3p.S3Parameters):
        """

        :param s3_parameters: The overarching S3 (Simple Storage Service) parameters
                              settings of this project, e.g., region code name, buckets, etc.
        """

        self.__s3_parameters: s3p.S3Parameters = s3_parameters

    def exc(self) -> typing.Tuple[pd.DataFrame, list[se.Specifications]]:
        """

        :return:
        """

        codes: list[str] = src.data.codes.Codes().exc()
        reference = src.data.reference.Reference(
            s3_parameters=self.__s3_parameters).exc(codes=codes)
        src.data.menu.Menu().exc(reference=reference)

        specifications_ = src.data.specifications.Specifications().exc(reference=reference)

        return reference, specifications_
