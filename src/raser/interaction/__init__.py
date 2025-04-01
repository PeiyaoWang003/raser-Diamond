
def main(kwargs):
    label = kwargs['label']
    if label == 'temperature':
        from . import cal_temp
        cal_temp.main()
    elif label == "energy_deposit":
        from . import g4_sic_energy_deposition
        g4_sic_energy_deposition.main()
    else:
        raise NameError(label)