from . import *
def main(args):
    label = vars(args)['label']
    if label == 'temperature':
        from . import cal_temp
        cal_temp.main()

    if label == 'FLM_v1':
        from . import FLM
        FLM.main()
    else:
        raise NameError(label)