import pickle


def read_args(filename):
    assert isinstance(filename, str)

    class DotDict(dict):
        __getattr__ = dict.get
        __setattr__ = dict.__setitem__
        __delattr__ = dict.__delitem__

    args = DotDict()
    for line in open(filename, 'r').read().splitlines():
        key,value = line.split(': ')
        try:
            # test if the number is float
            split_num = value.split('.')
            is_float = split_num[1]
            value = float(value) 

        except IndexError:
            # string does not have "." - value can be either a float or int
            try:
                value = int(value)
            except ValueError:
                value = str(value)

        except ValueError:
            # string does have "." -- cannot be converted to float
            value = str(value)
        args[key] = value
    return args


def pickle_files(filename, stuff):
    '''
    Save files to be loaded in the future
    :param filename: name of file to save
    :type filename: str
    :param stuff: Datastructure to be saved
    :return: None
    '''
    assert isinstance(filename, str)

    with open(filename, 'wb') as f:
        pickle.dump(stuff, f)


def load_files(filename):
    '''
    Load files from pickle
    :param filename: name of pickle to load
    :type filename: str
    :return: None
    '''
    assert isinstance(filename,str)

    with open(filename, "rb") as f:
        return pickle.load(f)
