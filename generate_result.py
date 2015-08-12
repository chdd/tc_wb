__author__ = 'Des'


def generate_result(f_name, content):
    try:
        f = open(f_name, 'w')
        f.writelines(content)
        f.close()
    except IOError as err:
        print err.message


def append_result(f_name, content):
    try:
        f = open(f_name, 'a')
        f.write('\n')
        f.write(content)
        f.close()
    except IOError as err:
        print err.message
