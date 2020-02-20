import numpy as np
import logging

logger = logging.getLogger('textlogger')

class UtilityConversion:
    @staticmethod
    def conversion_matrix(content):
        from scipy.sparse import csr_matrix
        density_map = csr_matrix((content['data'], content['inds'], content['indptr']),
                                 shape=content['shape']).todense()
        mask = content['mask']
        mask = csr_matrix((mask['data'], mask['inds'], mask['indptr']), shape=mask['shape']).todense() - 1
        final_density_map = mask + density_map
        return final_density_map


    @staticmethod
    def convert_matrix_to_string(mat):
        np.set_printoptions(threshold=np.inf)
        A = np.squeeze(np.asarray(mat))

        string_matrix = np.array2string(A)
        return string_matrix

    @staticmethod
    def convert_queryset_string_matrix(text_matrix_to_convert):

        try:
            text_matrix_to_convert = text_matrix_to_convert.replace('\n', '')
            text_matrix_to_convert = text_matrix_to_convert.replace('   ', ' ')
            text_matrix_to_convert = text_matrix_to_convert.replace('  ', ' ')
            text_matrix_to_convert = text_matrix_to_convert.replace('[ ', '[')
            text_matrix_to_convert = text_matrix_to_convert.replace(' ', ',')
            text_matrix_to_convert = text_matrix_to_convert.replace('],[', ';')
            text_matrix_to_convert = text_matrix_to_convert.replace('[', '')
            text_matrix_to_convert = text_matrix_to_convert.replace(']', '')

            #logger.debug(text_matrix_to_convert)

            matrix_imported = np.matrix(text_matrix_to_convert)
        except Exception as ex:
            logger.error("Exception convert_queryset_string_matrix: {0}".format(ex))
            return None

        return matrix_imported

    @staticmethod
    def convert_datetime_to_isoformat(datetime):

        datetime_str = str(datetime)

        datetime_str = datetime_str.replace(' ', 'T')

        return  datetime_str