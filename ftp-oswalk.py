# Import Module
import ftplib
import os
import glob
import sys


# Fill Required Information
HOSTNAME = "192.168.0.136"
USERNAME = "test"
PASSWORD = ""
# Connect FTP Server
ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)
# force UTF-8 encoding
ftp_server.encoding = "utf-8"


ftp_server.dir()


########   upload to server   ########## 

# Function to recursively create directory structure
def create_directory_structure(ftp, path):
    parts = path.split('/')
    for part in parts:
        if part:
            part = part.replace('\\', '/')
            try:
                ftp.mkd(part)
                print("Creating directory", part)
            except Exception as e:
                pass#print(f"{part}: {e}")

# Function to upload files to FTP using os.walk()
def upload_files_to_ftp(ftp_server):
    for root, dirs, files in os.walk('.'): 
        print(root)
        print(dirs)
        print(dirs)
        
        for file in files:
            try:
                item = os.path.join(root, file)
                directory_path = os.path.dirname(item)
                
                
                with open(item, 'rb') as file:
                   
                    file_name = os.path.basename(item)
                    directory_path = directory_path.replace('\\', '/')
                   
                    create_directory_structure(ftp_server,os.path.dirname(item))
                    
                    ftp_server.cwd(directory_path)
                  
                    ftp_server.storbinary(f"STOR {file_name}", file)
                    
                    print(f"Uploading {item}\n")
                    
                ftp_server.cwd('/')    
                    
            except Exception as e:
                print(f"Error uploading {item}: {e}")
                
        
        for directory in dirs:
            try:
                create_directory_structure(ftp_server, os.path.join(root, directory))
            except Exception as e:
                print(f"Error creating directory {directory}: {e}")
                
 
# Assuming ftp_server is your FTP connection object
upload_files_to_ftp(ftp_server)



########   Download from server   ##########  


try:

    print(ftp_server.pwd())
    print("Files on server")
    ftp_server.dir()
    
    
           
    files = ftp_server.nlst()
    print(":/n",files)
    

    if files:
        
        print("Enter comma-separated filenames to download or type 'all' to download all files:")
        selection = input("Selection: ").strip()

        if selection.lower() == "all":
        # Download all files
            for filename_to_download in files:
                if not os.path.isdir(filename_to_download):  # Check if it's not a directory
                    with open(filename_to_download, "wb") as file:
                        ftp_server.retrbinary(f"RETR {filename_to_download}", file.write)
                    print("File", filename_to_download, "downloaded successfully.")
                else:
                    print("Skipping directory1", filename_to_download)
                    
        
                    
        else:
        
            selected_files = [f.strip() for f in selection.split(",")]
            for filename_to_download in selected_files:
                if filename_to_download in files:
                    with open(filename_to_download, "wb") as file:
                        ftp_server.retrbinary(f"RETR {filename_to_download}", file.write)
                        print("File", filename_to_download, "downloaded successfully.")
                else:
                        print("File", filename_to_download, "does not exist on the server.")




except ftplib.error_perm as e:
    print("FTP error:", e)

except ftplib.error_reply as e:
    print("FTP reply error:", e)

except ftplib.error_temp as e:
    print("FTP temporary error:", e)

except ftplib.all_errors as e:
    print("Other FTP errors:", e)

finally:
    # Close the FTP connection
    ftp_server.quit()
