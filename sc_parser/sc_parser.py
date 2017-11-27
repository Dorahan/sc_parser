# sc-parser.py
import parser

def get_input(param_count, error_message):
    # argument_list = input('$ ').replace('$ ', '').split()
    argument_list = input('filename: ').replace('filename: ', '').split()

    while len(argument_list) != param_count:
        print(error_message)
        argument_list = input('filename: ').replace('filename: ', '').split()

    return argument_list

def sc_parser():
    source_input = get_input(1, 'Error: Type ie. filename.txt to start\n')
    source = source_input
    parser.parse(source)

class Master(object):
    def __init__(self):
        print('--------------------------------------------')
        print('Welcome to Smart Contract Parser\nto parse your contract type the filename:\nie. filename.txt')
        print('--------------------------------------------')



if __name__ == '__main__':
    Master()
    sc_parser()
