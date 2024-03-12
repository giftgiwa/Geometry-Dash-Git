import os
from os.path import expanduser
import platform

home = ""

'''
Handle search for CCLocalLevels.dat differently depending on operating system by
picking a different starter directory.
'''

current_platform = platform.platform() # get operating system name

# use these to include either a forward or a backwards slash in the directory
op_sys_index = 0 
slashes = ["/", "\\"]

if "Windows" in current_platform: # windows
    print("in Windows")
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

CCLocalLevels = ""
for root, dirs, files in os.walk(home):
    for file in files: 
        if (file.endswith("CCLocalLevels.dat") and root.endswith("GeometryDash")):
            # print("CCLocalLevels found")
            local_levels = root + slashes[op_sys_index] + file
            # print(root + slashes[op_sys_index] + file)
            break

f = open(CCLocalLevels, "r")
encrypted = (f.read()) # encrypted version of CCLocalLevels