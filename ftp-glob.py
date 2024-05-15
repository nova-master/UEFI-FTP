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



# Function to recursively create directory structure

def create_directory_structure(ftp, path):    
    parts = path.split('/')  # Split the path into parts if needed
    for part in parts:
        if part:
            part = part.replace('\\', '/')  # Replace backslashes with forward slashes for uniformity
            print("Creating directory", part)  # Print a message indicating the directory being created
            ftp.mkd(part)
            


# Assuming ftp_server is your FTP connection object

# Assuming ftp_server is your FTP connection object
def upload_files_to_ftp(ftp_server):
    for item in glob.iglob('**/*', recursive=True):
        if not os.path.isdir(item):  # Check if it's a file
            try:
                directory_path = os.path.dirname(item)
               
                
                with open(item, 'rb') as file:
                    file_name = os.path.basename(item)
                    directory_path = directory_path.replace('\\', '/')
                    ftp_server.cwd(directory_path)
                    ftp_server.storbinary(f"STOR {file_name}", file)
                    print(f"Uploading {item}")
                    
                    
                    # Check files in current directory against ftp_files
                    ftp_files = os.listdir(directory_path)
                    print(ftp_files)
                    
                    for file_ftp in ftp_files:
                        if file_ftp not in glob.iglob(f"{directory_path}/**/*", recursive=True):
                            try:
                                # Perform the logic for storing the file here
                                file_path = os.path.join(directory_path, file_ftp)
                                with open(file_path, 'rb') as file1:
                                    print(f"Storing {file_path} which is present in ftp_files but not found locally.")
                                    ftp_server.storbinary(f"STOR {file_ftp}", file1)
                                ftp_server.cwd('/')
                            except Exception as e:
                                print(f"Error storing file {file_path}: {e}")
            except Exception as e:
               pass# print(f"Error uploading {item}: {e}")
        elif not os.path.isfile(item):  # Check if it's a directory and not found in items
            try:
                # Create the directory structure on the FTP server if it doesn't exist
                
                create_directory_structure(ftp_server, item)
            except Exception as e:
                print(f"Error creating directory {item}: {e}")
            
                
            
    

upload_files_to_ftp(ftp_server)

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