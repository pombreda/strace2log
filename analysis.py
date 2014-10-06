#!/usr/bin/python

import os
import sys
import manage_files

class Analysis:
    def __init__(self, _path):
        self.file_name = os.path.basename(_path)
        self.dir_name = os.path.splitext(self.file_name)[0]

        if not os.path.isdir(self.dir_name):
            os.mkdir(self.dir_name)
            print('Directory was created => ' + self.dir_name)
        else:
            print('Directory already exists => ' + self.dir_name)
            sys.exit(-1)

        self.opened_files = manage_files.FileNodeList()
        print(self.dir_name)

    def isNumber(self, _number):
        try:
            float(_number)
            return True
        except ValueError:
            return False

    def open_syscall(self, _line):
        # Extract a file name
        start = _line.find('"') + 1
        end = _line.find('"', start)
        file_name = _line[start:end]

        # Extract a file descriptor
        _line = _line.strip().split('=')
        fd = _line[1].replace(' ', '')

        # If fd is a number, this file is added to the opened files list
        if self.isNumber(fd):
            self.opened_files.add_file(fd, file_name)

    def close_syscall(self, _fd):
        self.opened_files.delete_file(fd)


def main():
    try:
        path = sys.argv[1]

    except IndexError as err:
        print('Args error: ' + str(err))
        return


    try:
        with open(path, 'r') as trace_file:
            analysis = Analysis(path)

            for each_line in trace_file:
                if each_line.find('open(') == 0:
                    analysis.open_syscall(each_line)

            analysis.opened_files.list_print()

    except IOError as err:
        print('File error: ' + str(err))
        return

if __name__ == '__main__':
    main()