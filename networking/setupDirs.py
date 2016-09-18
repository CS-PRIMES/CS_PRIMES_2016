import os
import sys
import shutil

if __name__ == '__main__':
    if not os.path.exists('./solver/'):
        os.makedirs("./solver/")
    if not os.path.exists('./con_test/'):
        os.makedirs("./con_test/")
