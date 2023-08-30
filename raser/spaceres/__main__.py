import importlib
def main(args_dict):
    if len(args_dict['option']) == 0:
        print("spaceres main function placeholder")
    else:
        module_name = args_dict['option'][0]
        args_dict['option']=args_dict['option'][1:]
        try:
            module = importlib.import_module(module_name)
            module.main(args_dict)
        except ModuleNotFoundError:
            print("No spaceres subcommand found")