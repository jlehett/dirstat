import os
import sys

SPACES = 3
SIZE_PERCENT = 1.0

class Item:
    def __init__(self, path, size, depth):
        self.path = path
        self.size = size
        self.depth = depth

        self.folder = self.path.split('/')[-1]

        self.children = []

    def __repr__(self):
        string = ''
        for i in range(self.depth):
            string += '|'
            for _ in range(SPACES-1):
                string += ' '
        sizeString = str(self.size).split('.')
        string += sizeString[0]
        string += '.'
        string += sizeString[1][0]
        string += '%'
        for _ in range(SPACES):
            string += ' '
        string += self.folder

        if self.depth == 0:
            for _ in range(SPACES):
                string += ' '
            string += 'Minimum Size: ' + str(SIZE_PERCENT) + '%'

        return string


def getData(rootDir):
    dirStats = os.popen('sudo du -BMB ' + rootDir + ' 2>/dev/null').read()
    return dirStats.splitlines()

def buildDictionary(rootDir, data):
    dictionary = {}

    base_depth = len(rootDir.split('/'))

    rootSize = float(data[-1].split('\t')[0][:-2])

    for datum in data[-1:0:-1]:
        flag = False
        if datum == data[-1]:
            flag = True
        datum = datum.split('\t')
        size = float(datum[0][:-2]) / rootSize * 100.0
        path = datum[1]

        if size < SIZE_PERCENT:
            continue

        if flag == False:
            depth = len(path.split('/')) - base_depth + 1
        else:
            depth = 0
        
        item = Item(path, size, depth)

        dictionary[path] = item

        if flag == False:
            paths = path.split('/')
            parentPath = paths[:-1]
            parentPath = '/'.join(parentPath)
            if parentPath == '':
                parentPath = '/'
            dictionary[parentPath].children.append(item)

    return dictionary

def printTree(dictionary, rootDir, starting=True):
    if starting == False:
        print(dictionary[rootDir])
    dictionary[rootDir].children.sort(key=lambda x: x.size, reverse=True)
    for child in dictionary[rootDir].children:
        printTree(dictionary, child.path, False)



if __name__ == '__main__':
    rootDir = sys.argv[1]
    if len(sys.argv) > 2:
        SIZE_PERCENT = float(sys.argv[2])
    data = getData(rootDir)
    dictionary = buildDictionary(rootDir, data)
    print(dictionary[rootDir])
    printTree(dictionary, rootDir)