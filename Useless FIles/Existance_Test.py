import os

# Constructing path using os.path
downloads_path = 'Downloads'

# Checking if the directory exists
if os.path.exists(downloads_path):
    print('Directory')
else:
    print("Downloads directory does not exist.")
