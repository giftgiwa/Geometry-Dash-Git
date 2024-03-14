import os
import platform
import base64
import zlib
import gzip
from os.path import expanduser


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

        # use these to include either a forward or a backwards slash in the directory
        op_sys_index = 0 
        slashes = ["/", "\\"]

        if "Windows" in current_platform: # windows
            # print("in Windows")
            home = expanduser("~")
            home += "\\AppData\\Local\\GeometryDash"
            local_levels_query = 'GeometryDash\\CCLocalLevels.dat'
            op_sys_index = 1
        elif "microsoft-standard-WSL" in current_platform: # WSL
            non_users = ['All Users', 'Default', 'Default User', 'desktop.ini', 'Public']

            user_directory = os.listdir("/mnt/c/Users")
            for user in user_directory:
                if user not in non_users:
                    home = "/mnt/c/Users/" + user + "/AppData/Local/GeometryDash"
                    break
            op_sys_index = 0

        CCLocalLevels_path = ""
        for root, dirs, files in os.walk(home):
            for file in files: 
                if (file.endswith("CCLocalLevels.dat") and root.endswith("GeometryDash")):
                    # forward slash for Windows, backwards for WSL
                    CCLocalLevels_path = root + slashes[op_sys_index] + file
                    break
        
        f = open(CCLocalLevels_path, "r")
        self.CCLocalLevels_encrypted = (f.read()) # encrypted version of CCLocalLevels
        return

    # decrypt CCLocalLevels
    # source: https://wyliemaster.github.io/gddocs/#/topics/localfiles_encrypt_decrypt?id=windows-1
    def decrypt(self, s: str):

        def xor(string: str, key: int) -> str:
            return ("").join(chr(ord(char) ^ key) for char in string)
        
        base64_decoded = base64.urlsafe_b64decode(xor(s, key=11).encode())
        decompressed = gzip.decompress(base64_decoded)
        return decompressed.decode()

    # encrypt CCLocalLevels
    # source: https://wyliemaster.github.io/gddocs/#/topics/localfiles_encrypt_decrypt?id=windows-1
    def encrypt(self, s: str):

        def xor(string: str, key: int) -> str:
            return ("").join(chr(ord(char) ^ key) for char in string)

        gzipped = gzip.compress(s.encode())
        base64_encoded = base64.urlsafe_b64encode(gzipped)
        return xor(base64_encoded.decode(), key=11)


# if __name__ == '__main__':
    # level = CCLocalLevels()
    # print(level.CCLocalLevels_encrypted)
