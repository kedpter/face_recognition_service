import pickle
import codecs


def base64_encode(obj):
    '''
    :param obj: object
    :return: string
    '''
    return codecs.encode(pickle.dumps(obj), "base64").decode()


def base64_decode(obj):
    '''
    :param obj: pickled string
    :return object
    '''
    return pickle.loads(codecs.decode(obj.encode(), "base64"))
