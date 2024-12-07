Description of the program startup process.

To start the program, create a stylizations directory in the directory where the program is located and add all the necessary images to it.

|  ATTENTION:                                                                                                |
|  Stylized images should be called 'content_<content_id>_...', this is important due to shuffeling process  |

Then run the code using the 'python app.py' command.

In the directory from which you run the program, two directories output and index_file will be created. 
- output contains all the user's answers in the form of csv files.
- index_file contains the order in which the mixed files will be shown to the user.

If there are nested directories in stylizations, the program will recursively collect all files with jpg extension from them.

Launch parameters:
--data DATA    Stylizations directory name (Default is 'stylizations')
--out OUT      Output scores directory name (will be created if not present) (Default is 'output')
--index INDEX  Shuffeling index for directory name (will be created if not present) (Default is 'index_file')
