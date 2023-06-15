# File-Storage

This is a simple Flask-based web application that allows you to upload, download, delete, and retrieve metadata of files. The application is built using Python3, Flask and Postgresql.

## Features

- Upload files: You can upload any type of file.

- Customize extensions: You can choose which file extension is allowed to be uploaded.

- Download files: You can download any file you have uploaded before.

- Delete files: You can delete any file you have uploaded before.

- Retrieve metadata: You can retrieve the metadata of any file which includes the file name, extension, file path, and last modified date.


## QuickStart:

### - Using docker-compose:

Dependencies:

- `docker` and `docker-compose`

  ```bash
  # install
  $ git clone https://github.com/fatemeh-mgsdi/file-storage.git
  $ cd file-storage
  
  # configure (the defaults are fine for development)
  $ edit `.env.sample` and save as `.env`
  
  # run it
  $ docker-compose build
  $ docker-compose --env-file=.env up

  ```

  Once it's done building and everything has booted up:

  - Access the app at: [http://localhost:5000](http://localhost:5000)

### - Running locally

- Dependencies:

  - Linux system
  - Python 3.8+
  - virtualenv
  - PostgreSQL

- Installation

  ```bash
  # install
  $ git clone https://github.com/fatemeh-mgsdi/file-storage.git
  $ cd file-storage
  $ virtualenv -p /path/to/python3 venv
  $ source venv/bin/activate
  $ pip install -r requirements.txt
  
  # configure
  $ edit `.env.sample` and save as `.env`
  $ customize ALLOWED_EXTENSIONS in `configs.py`
    
  # backend dev server:
  $ flask run
  ```
