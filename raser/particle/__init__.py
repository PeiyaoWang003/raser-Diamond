from . import *
from . import calculate_temperature

def main(args):
    label = vars(args)['label']

    if label == 'foo':
        foo.main()
    elif label == 'temperature':
        calculate_temperature.main()
    else:
        raise NameError(label)