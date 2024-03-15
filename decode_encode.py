import os
import platform
import base64
import zlib
import gzip
from os.path import expanduser
from Crypto.Cipher import AES

class CCLocalLevels:

    # initialize CCLocalLevels object
    def __init__(self):
        self.CCLocalLevels_encrypted = ""
        self.CCLocalLevels_decrypted = ""

        self.get_CCLocalLevels()
        self.CCLocalLevels_decrypted = self.decrypt(self.CCLocalLevels_encrypted)

        # (for testing purposes) write the decrypted CCLocalLevels to a text file
        f = open("CCLocalLevels.txt", "w")
        f.write(self.CCLocalLevels_decrypted)
        f.close()

        # decrypting then encrypting CCLocalLevels indefinitely leaves the decrypted version intact
        assert(self.decrypt(self.encrypt(self.CCLocalLevels_decrypted))[0:200] == self.CCLocalLevels_decrypted[0:200])


    # locate CCLocalLevels on the user's computer
    def get_CCLocalLevels(self):
        '''
        Handle search for CCLocalLevels.dat differently depending on operating system by
        picking a different starter directory.
        '''
        home = ""
        current_platform = platform.platform() # get operating system name

        # print(current_platform) # for testing purposes

        # use these to include either a forward or a backwards slash in the directory
        op_sys_index = 0 
        slashes = ["/", "\\"]

        if "Windows" in current_platform: # windows
            home = expanduser("~")
            home += "\\AppData\\Local\\GeometryDash"
            op_sys_index = 1
        elif "microsoft-standard-WSL" in current_platform: # WSL
            non_users = ['All Users', 'Default', 'Default User', 'desktop.ini', 'Public']

            user_directory = os.listdir("/mnt/c/Users")
            for user in user_directory:
                if user not in non_users:
                    home = "/mnt/c/Users/" + user + "/AppData/Local/GeometryDash"
                    break
            op_sys_index = 0
        elif "macOS" in current_platform: # MacOS
            home = expanduser("~")
            home += "/Library/Application Support/GeometryDash"
            op_sys_index = 0

        CCLocalLevels_path = ""
        for root, dirs, files in os.walk(home):

            print(root)
            # print("Files in this directory: " + files)
            for file in files: 
                if (file.endswith("CCLocalLevels.dat") and root.endswith("GeometryDash")):
                    # forward slash for Windows, backwards for WSL
                    CCLocalLevels_path = root + slashes[op_sys_index] + file
                    break
        
        # print("CCLocalLevels path: " + CCLocalLevels_path)
        f = open(CCLocalLevels_path, "r")
        self.CCLocalLevels_encrypted = f.read() # encrypted version of CCLocalLevels
        return

    # decrypt CCLocalLevels
    # source: https://wyliemaster.github.io/gddocs/#/topics/localfiles_encrypt_decrypt?id=windows-1
    def decrypt(self, s: str) -> str:

        if "macOS" in platform.platform(): # MacOS decryption scheme
            def remove_pad(data: bytes) -> bytes:
                last = data[-1]
                if last < 16:
                    data = data[:-last]
                return data
            
            KEY = (  # python will automatically concatenate two parts
                    b"\x69\x70\x75\x39\x54\x55\x76\x35\x34\x79\x76\x5d\x69\x73\x46\x4d"
                    b"\x68\x35\x40\x3b\x74\x2e\x35\x77\x33\x34\x45\x32\x52\x79\x40\x7b"
            )

            cipher = AES.new(KEY, AES.MODE_ECB)
            return remove_pad(cipher.decrypt(s)).decode()
        
        else : # Windows decryption scheme

            def xor(string: str, key: int) -> str:
                return ("").join(chr(ord(char) ^ key) for char in string)
            
            base64_decoded = base64.urlsafe_b64decode(xor(s, key=11).encode())
            decompressed = gzip.decompress(base64_decoded)
            return decompressed.decode()

    # encrypt CCLocalLevels
    # source: https://wyliemaster.github.io/gddocs/#/topics/localfiles_encrypt_decrypt?id=windows-1
    def encrypt(self, s: str):

        if "macOS" in platform.platform(): # MacOS encryption scheme
            def add_pad(data: bytes) -> bytes:
                len_r = len(data) % 16
                if len_r:
                    to_add = 16 - len_r
                    data += to_add.to_bytes(1, "little") * to_add
                return data
            
            KEY = (  # python will automatically concatenate two parts
                    b"\x69\x70\x75\x39\x54\x55\x76\x35\x34\x79\x76\x5d\x69\x73\x46\x4d"
                    b"\x68\x35\x40\x3b\x74\x2e\x35\x77\x33\x34\x45\x32\x52\x79\x40\x7b"
            )
            
            cipher = AES.new(KEY, AES.MODE_ECB)
            return cipher.encrypt(add_pad(s.encode()))

        else: # Window encryption scheme

            def xor(string: str, key: int) -> str:
                return ("").join(chr(ord(char) ^ key) for char in string)

            gzipped = gzip.compress(s.encode())
            base64_encoded = base64.urlsafe_b64encode(gzipped)
            return xor(base64_encoded.decode(), key=11)


# if __name__ == '__main__':
    # level = CCLocalLevels()
    # print(level.CCLocalLevels_encrypted)
