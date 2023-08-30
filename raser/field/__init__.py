def main(args_dict):
    module_name = args_dict['option'][0]
    args_dict['option']=args_dict['option'][1:]
    module = __import__(module_name)
    module.main(args_dict)