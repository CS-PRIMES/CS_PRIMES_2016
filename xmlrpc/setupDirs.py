import os
import sys
import shutil

if __name__ == '__main__':
        N = int(sys.argv[1])
        if(os.path.exists('./tmp/')):
                shutil.rmtree('./tmp/')
        os.makedirs('./tmp/')
        for id in range(1, N+1):
                os.makedirs('./tmp/h'+str(id)+'/')
