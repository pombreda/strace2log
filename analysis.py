#!/usr/bin/python

import os
import sys
import manage_files

class Analysis:
    def __init__(self, _path, _verbose=False):
        self.file_name = os.path.basename(_path)
        self.dir_name = os.path.splitext(self.file_name)[0]
        self.verbose = _verbose
        self.count = 0

        if not os.path.isdir(self.dir_name):
            os.mkdir(self.dir_name)
            print('init: Directory was created => ' + self.dir_name)
        else:
            print('init: Directory already exists => ' + self.dir_name)
            sys.exit(-1)

        self.opened_files = manage_files.FileNodeList()

    def get_count(self):
        self.count = self.count + 1
        return self.count

    def isNumber(self, _number):
        try:
            float(_number)
            return True
        except ValueError:
            return False

    def print_log(self, _msg):
        if self.verbose == True:
            print(_msg)

    '''
    The open() system call is called,
    this open_syscall() function is invoked.
    '''
    def open_syscall(self, _line):
	print('-' * 20)
        print(_line)

        # Extract a file name
        start = _line.find('"') + 1
        end = _line.find('"', start)
        file_name = _line[start:end]

        # Extract a file descriptor
        _line = _line.strip().split('=')
        fd = _line[len(_line) - 1].replace(' ', '')

        # If fd is a number, this file is added to the opened files list
        if self.isNumber(fd):
            if os.path.isfile(file_name):
                file_size = os.path.getsize(file_name)
            else:
                file_size = 'The file is not exist'
            self.opened_files.add_file(fd, file_name, file_size)

    '''
    The close() system call is called,
    this close_syscall() function is invoked.
    '''
    def close_syscall(self, _line):
	print('-' * 20)
        print(_line)

        # Extract a file descriptor
        start = _line.find('(') + 1
        end = _line.find(')', start)
        fd = _line[start:end]

        self.opened_files.delete_file(fd, self.dir_name)

    '''
    The lseek() system call is called,
    this lseek_syscall() function is invoked.
    '''
    def lseek_syscall(self, _line):
	print('-' * 20)
        print(_line)

    '''
    The read(), readv() system calls are called,
    this read_syscall() function is invoked.
    '''
    def read_syscall(self, _line):
	print('-' * 20)
        print(_line)

        # Extract a file descriptor
        start = _line.find('(') + 1
        end = _line.find(',', start)
        fd = _line[start:end]

        # Extract a size reading
        _line = _line.strip().split('=')
        size_reading = _line[len(_line) - 1].replace(' ', '')

        self.opened_files.record_access_info(fd, 'read', self.get_count(), -1, int(size_reading))

    '''
    The pread() system call is called,
    this pread_syscall() function is invoked.
    '''
    def pread_syscall(self, _line):
	print('-' * 20)
        print(_line)

        # Extract a file descriptor
        start = _line.find('(') + 1
        end = _line.find(',', start)
        fd = _line[start:end]

        # Extract file offset
        _line = _line.strip().replace(' ', '')
        start = _line.rfind(',') + 1
        end = _line.rfind(')') 
        offset = _line[start:end]

        # Extract a size reading
        _line = _line.split('=')
        size_reading = _line[len(_line) - 1].replace(' ', '')

        try:
            self.opened_files.record_access_info(fd, 'read', self.get_count(), int(offset), int(size_reading))
        except:
            print('- [Error] unfinished case...')

    '''
    The write(), writev() system calls are called,
    this write_syscall() function is invoked.
    '''
    def write_syscall(self, _line):
	print('-' * 20)
        print(_line)

        # Extract a file descriptor
        start = _line.find('(') + 1
        end = _line.find(',', start)
        fd = _line[start:end]

        # Extract a size reading
        _line = _line.strip().split('=')
        size_reading = _line[len(_line) - 1].replace(' ', '')

        self.opened_files.record_access_info(fd, 'write', self.get_count(), -1, int(size_reading))

    '''
    The pwrite() system call is called,
    this pwrite_syscall() function is invoked.
    '''
    def pwrite_syscall(self, _line):
	print('-' * 20)
        print(_line)

        # Extract a file descriptor
        start = _line.find('(') + 1
        end = _line.find(',', start)
        fd = _line[start:end]

        # Extract file offset
        _line = _line.strip().replace(' ', '')
        start = _line.rfind(',') + 1
        end = _line.rfind(')') 
        offset = _line[start:end]

        # Extract a size reading
        _line = _line.split('=')
        size_reading = _line[len(_line) - 1].replace(' ', '')

        self.opened_files.record_access_info(fd, 'write', self.get_count(), int(offset), int(size_reading))

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
                start = each_line.find(' ') + 1
                end = len(each_line)
                each_line = each_line[start:end]
                each_line = each_line.strip()

                if each_line.find('open(') == 0:
                    analysis.open_syscall(each_line)

                if each_line.find('close(') == 0:
                    analysis.close_syscall(each_line)

                if each_line.find('lseek(') == 0:
                    analysis.lseek_syscall(each_line)

                if each_line.find('read(') == 0:
                    analysis.read_syscall(each_line)

                if each_line.find('pread(') == 0:
                    analysis.pread_syscall(each_line)

                if each_line.find('write(') == 0:
                    analysis.write_syscall(each_line)

                if each_line.find('pwrite(') == 0:
                    analysis.pwrite_syscall(each_line)

    except IOError as err:
        print('File error: ' + str(err))
        return

if __name__ == '__main__':
    main()
