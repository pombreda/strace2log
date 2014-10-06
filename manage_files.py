'''
FileNode class
This class manages the information of the file that has been opened
'''
class FileNode:

    # When a file is opened, this object is created
    def __init__(self, _fd, _name, _size):
        self.fd = _fd                   # file descriptor
        self.name = _name               # file name
        self.size = _size               # file size
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

    def add_file(self, _fd, _name, _size):
        new_file = FileNode(_fd, _name, _size) # create a new node
        new_file.next = self.cur_file   # link the new node to the 'previous' node.
        self.cur_file = new_file        # set the current node to the new one.
        print('A file is added => ' + str(new_file.fd) + ' size=' + _size)
        self.list_print()

    def delete_file(self, _fd):
        cur_file = self.cur_file
        next_file = None

        if cur_file == None:
            print('This list is empty')
            return
        else:
            next_file = cur_file.next

        if cur_file.fd == _fd:
            self.cur_file = next_file
            print('A file is deleted => ' + str(cur_file.fd))
            del cur_file
            self.list_print()
            return

        while next_file:
            if next_file.fd == _fd:
                cur_file.next = next_file.next
                print('A file is deleted => ' + str(next_file.fd))
                del next_file
                self.list_print()
                break

            cur_file = next_file
            next_file = next_file.next

    def list_print(self):
        print '[cur list]'
        file = self.cur_file
        while file:
            print file.fd,
            print '->',
            file = file.next
        print 'None'

    def record_access_info(self, _fd, _type, _size):
        file = self.cur_file
        while file:
            if file.fd == _fd:
                file.access.append(_access)
            file = file.next

    def move_file_offset(self, _fd, _offset):
        file = self.cur_file
        while file:
            if file.fd == _fd:
                file.offset = _offset
            file = file.next
        print('file offset is moved => ' + file.fd)

'''
ll = FileNodeList()
ll.add_file(1, 'file1')
#ll.add_file(2, 'file2')
#ll.add_file(3, 'file3')
#ll.add_file(4, 'file4')
#ll.add_file(5, 'file5')

#ll.delete_file(3)
ll.delete_file(1)
ll.delete_file(2)

#ll.add_file(3, 'file3')
'''

'''
ll = FileNodeList()
ll.add_node(1, 'test01')
ll.add_node(2, 'test02')
ll.record_access_info(1, ['read', 0, 4096])
ll.record_access_info(2, ['write', 512, 512])
ll.record_access_info(1, ['read', 4096, 4096])


ll.list_print()
'''