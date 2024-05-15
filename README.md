# UEFI-FTP
Python-based FTP client to upload and download recursive

# FTP File Uploader and download

This Python script automates downloading/uploading files to/from a local directory to an FTP server. One is based on the "glob library" and the other is "oswalk" library. To begin testing either module, Python support must first be added to the EFI shell, as both modules are native to Python.

## Description

The FTP File script traverses a local directory, uploads files to the specified FTP server, and creates directory structures as needed.

## Features

- Recursively uploads files from a local directory to an FTP server.
- Automatically creates directory structures on the FTP server to mirror the local directory structure.
- Supports handling of errors during the upload process.

## Installation

1. Clone the repository:

  

2. Navigate to the project directory:

   

3. Install the required dependencies (if any):

    ```bash
    Does not require any external library
    ```

## Usage

1. Make sure you have Python installed on your system.
2. Configure the FTP connection parameters in the script.
3. Run the script:

    ```bash
    python3 ftp-glob.py
    python3 ftp-oswalk.py
    
    ```

4. Follow the on-screen instructions to monitor the upload process.

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).





