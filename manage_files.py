import os
import gnuplot

'''
FileNode class
This class manages the information of the file that has been opened
'''
class FileNode:

    '''
    When a file is opened, this object is created
    '''
    def __init__(self, _fd, _file_name, _file_size):
        self.fd = _fd                   # file descriptor
        self.file_name = _file_name	# file name
        self.file_size = _file_size	# file size
        self.offset = 0                 # current offset
        self.access = list()            # access history
        self.next = None                # reference to the next node

    def __str__(self):
        return str(self.fd)

'''
FileNodeList
List of FileNode objects
'''
class FileNodeList:
    def __init__(self):
        self.cur_file = None

    def write_to_file(self, _file_info, _dir_name):
        num = 1
        file_name = _file_info.file_name.replace('/', '_')
        log_file_name = _dir_name + '/' + file_name + '.' + str(num)

        while os.path.isfile(log_file_name):
            num = num + 1
            log_file_name = _dir_name + '/' + file_name + '.' + str(num)

        print('- log file name: ' + log_file_name)

        log_file = open(log_file_name, 'w')

        log_file.write('# File Name: ' + str(_file_info.file_name) + '\n')
        log_file.write('# File Size: ' + str(_file_info.file_size) + '\n\n')
        log_file.write('# Count, Offset(R), After Offset(R), Offset(W), After Offset(W)\n')

        count_per_file = 0

        for items in _file_info.access:
            #count = items[1]
            count_per_file = count_per_file + 1
            cur_offset = items[2]
            after_offset = items[3]

            if items[0] == 'read':
                log_file.write(str(count_per_file) + ',' + str(cur_offset) + ',' + str(after_offset) + ',0,0\n')
            else:
                log_file.write(str(count_per_file) + ',0,0,' + str(cur_offset) + ',' + str(after_offset) + '\n');

        log_file.close()
        gnuplot.draw_graph(log_file_name)


    def add_file(self, _fd, _file_name, _file_size):
        new_file = FileNode(_fd, _file_name, _file_size)	# create a new node
        new_file.next = self.cur_file				# link the new node to the 'previous' node.
        self.cur_file = new_file				# set the current node to the new one.
        print('- fd: ' + str(new_file.fd))
        print('- file_name: ' + str(new_file.file_name))
	print('- file_size: ' + str(new_file.file_size))
	print('- This file is added to the opened files list')
        self.list_print()

    def delete_file(self, _fd, _dir_name):
        cur_file = self.cur_file
        next_file = None

        if cur_file == None:
            print('- This list is empty')
            return
        else:
            next_file = cur_file.next

        if cur_file.fd == _fd:
            self.cur_file = next_file
	    print('- fd: ' + str(cur_file.fd))
	    print('- file_name: ' + str(cur_file.file_name))
	    print('- This file is deleted from the opened files list')
            self.write_to_file(cur_file, _dir_name)
            del cur_file
            self.list_print()
            return

        while next_file:
            if next_file.fd == _fd:
                cur_file.next = next_file.next
		print('- fd: ' + str(next_file.fd))
                print('- file_name: ' + str(next_file.file_name))
		print('- This file is deleted from the opened files list')
                self.write_to_file(next_file, _dir_name)
                del next_file
                self.list_print()
                break

            cur_file = next_file
            next_file = next_file.next

    def list_print(self):
        print '- Current list of opened files'
	print '  ',
        file = self.cur_file
        while file:
            print file.fd,
            print '->',
            file = file.next
        print 'None'

    def record_access_info(self, _fd, _type, _count, _offset, _block_size):
        file = self.cur_file
        while file:
            if file.fd == _fd:
                if _offset >= 0:
                    offset = _offset
                else:
                    offset = file.offset

                after_offset = offset + _block_size

		print('- fd: ' + str(file.fd))
		print('- file_name: ' + str(file.file_name))
		print('- operation: ' + str(_type))
                print('- offset: ' + str(offset))
		print('- block_size: ' + str(_block_size))

                access_info = [_type, _count, offset, after_offset]

                if _offset < 0:
                    file.offset = after_offset

                file.access.append(access_info)
    
                print('- history: '),
                print(file.access)
            file = file.next

    def move_file_offset(self, _fd, _offset):
        file = self.cur_file
        while file:
            if file.fd == _fd:
                file.offset = int(_offset)
            file = file.next
        print('- file offset is moved => ' + file.fd)
