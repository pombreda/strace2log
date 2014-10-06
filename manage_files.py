'''
FileNode class
This class manages the information of the file that has been opened
'''
class FileNode:

    # When a file is opened, this object is created
    def __init__(self, _fd, _name):
        self.fd = _fd                   # file descriptor
        self.name = _name               # file name
        self.offset = 0                 # current offset
        self.access = list()            # access history
        self.next = None                # reference to the next node

'''
FileNodeList
List of FileNode objects
'''
class FileNodeList:
    def __init__(self):
        self.cur_file = None

    def add_file(self, _fd, _name):
        new_file = FileNode(_fd, _name) # create a new node
        new_file.next = self.cur_file   # link the new node to the 'previous' node.
        self.cur_file = new_file        # set the current node to the new one.
        print('A file is added => ' + new_file.fd)

    def list_print(self):
        file = self.cur_file
        while file:
            print file.fd
            print file.name
            print file.access
            print '=' * 10
            file = file.next

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
ll.add_node(1, 'test01')
ll.add_node(2, 'test02')
ll.record_access_info(1, ['read', 0, 4096])
ll.record_access_info(2, ['write', 512, 512])
ll.record_access_info(1, ['read', 4096, 4096])


ll.list_print()
'''