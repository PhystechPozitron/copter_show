import sys # to work with command prompt
import zipfile # to unpack <>.zip
import os # to make and remove temporary directory
import re # to read from "main.txt"

N_max = 1000
fps_max = 24
sizeX_max = 100
sizeY_max = 100 # restrictions for the parameters of show

# functions

def convertBytesBMP(array,i,cnt):
    result = "".encode('utf-8')
    for j in range(len(array)):
        subarray = array[cnt*j + 1:cnt*j + 3] #(G,R)
        if i % 2 == 0:
            result = result + subarray + array[cnt*j:cnt*j + 1] 
            # even strings : (B,G,R) => (G,R,B)
        else:
            result = result + array[cnt*j:cnt*j + 1] + subarray[::-1]  
            # odd strings : (B,G,R) => (B,R,G)
    if i % 2 == 1:
        result = result[::-1] # invert odd strings
    return result

def readBMP(fname,sizeX,sizeY):
    result = "".encode('utf-8') # output bytes
    try:
        with open(fname,"rb") as f:
            # read BITMAPFILEHEADER
            f.read(10) 
            bfOffBits = int.from_bytes(f.read(4)[::-1],byteorder = "big") # beginning of data
            # read BITMAPINFOHEADER
            bcSize = int.from_bytes(f.read(4)[::-1],byteorder = "big") # BMP version
            if bcSize == 12: # CORE version
                width = int.from_bytes(f.read(2)[::-1],byteorder = "big") # sizeX
                height = int.from_bytes(f.read(2)[::-1],byteorder = "big") # sizeY 
            else: # versions 3,4,5
                width = int.from_bytes(f.read(4)[::-1],byteorder = "big") # sizeX
                height = int.from_bytes(f.read(4)[::-1],byteorder = "big") # sizeY
            if (width != sizeX)or(height != sizeY):
                raise Exception("Wrong size of file")
            f.read(2)
            byteCount = int.from_bytes(f.read(2)[::-1],byteorder = "big")//8 # byte to pixel
            if (byteCount != 3)and(byteCount != 4):
                raise Exception("Wrong number of bytes to pixel")
            f.seek(bfOffBits)
            # read PIXELS
            for i in range(sizeY):
                result = result + convertBytesBMP(f.read(byteCount*sizeX),i,byteCount)
    except Exception as er:
        print("Error in file {}! {}".format(fname,str(er)))
        result = "".encode('utf-8')
    finally:
        return result

def readMain(fname):
    N, fps, sizeX, sizeY = 0, 0, 0, 0
    string = ""
    try:
        with open(fname,"r") as f:
            # read from "main.txt"
            string = f.read()
            pattern = "N\s*=\s*(\d+).*fps\s*=\s*(\d+).*sizeX\s*=\s*(\d+).*sizeY\s*=\s*(\d+)" 
            match = re.search(pattern,string)
            if (1 <= int(match.group(1)))and(int(match.group(1)) <= N_max):
                N = int(match.group(1)) 
            else:
                raise Exception("Wrong N")
            if (1 <= int(match.group(2)))and(int(match.group(2)) <= fps_max):
                fps = int(match.group(2)) 
            else:
                raise Exception("Wrong fps")
            if (1 <= int(match.group(3)))and(int(match.group(3)) <= sizeX_max):
                sizeX = int(match.group(3)) 
            else:
                raise Exception("Wrong sizeX")
            if (1 <= int(match.group(4)))and(int(match.group(4)) <= sizeY_max):
                sizeY = int(match.group(4)) 
            else:
                raise Exception("Wrong sizeY")
    except Exception as er:
        print("Error in file {}! {}".format(fname,str(er)))
        N, fps,sizeX, sizeY = 0, 0, 0, 0
    finally:
        return N, fps, sizeX, sizeY

def readZIP(fname):
    result = "".encode('utf-8')
    try:
        with zipfile.ZipFile(fname,"r") as f:
            path = os.getcwd()
            os.mkdir("temp")
            os.chdir("temp") # "temp" is a working directory
            # write fps and size to result...
            f.extract("main.txt")
            N, fps, sizeX, sizeY = readMain("main.txt")
            if N == 0:
                raise Exception("Try to fix main.txt")
            # ...according to structure
            result = result + fps.to_bytes(2,byteorder = "big")
            result = result + sizeX.to_bytes(2,byteorder = "big") + sizeY.to_bytes(2,byteorder = "big") 
            os.remove("main.txt")
            # write BMP files to result
            N_copy = N
            for i in range(1,N + 1):
                f.extract(str(i) + ".bmp")
                frame = readBMP(str(i) + ".bmp",sizeX,sizeY) 
                if frame != "".encode('utf-8'):
                    result = result + frame # add "i.bmp" to result
                else:
                    N_copy = N_copy - 1 # if "i.bmp" isnt read, decrement N_copy
                os.remove(str(i) + ".bmp")
            # write N_copy to result    
            result = N_copy.to_bytes(2,byteorder = "big") + result
            os.chdir(path) # return to main directory
            os.rmdir("temp")
    except Exception as er:
        print("Error in file {}! {}".format(fname,str(er)))
        result = "".encode('utf-8')
    finally:
        return result
                        
# main block
# input format: python <>.py <>.zip <>(.show)

name_in = sys.argv[1]
name_out = sys.argv[2]

if len(sys.argv) == 3: 
    with open(name_out + ".show","wb") as f:
        if name_in[-4:] == ".zip":
            f.write(readZIP(name_in)) # write to <>.show
            print("File {} is ready!".format(name_out + ".show"))
        else:
            print("Wrong input format!")
            exit()
else:
    print("Wrong command!")
    exit()

