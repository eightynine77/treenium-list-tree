# treenium list tree
list directories and files in tree with advanced features<br>
<img width="538" height="366" alt="image" src="https://github.com/user-attachments/assets/454c8439-bba9-43fd-acf8-55b29a9fa0dc" />

## how to use
### commands
<hr>
[ef | --exclude-files] exclude files in the tree listing
NOTE: --exclude-files argument is case sensitive. so if a file is in upper case LIKE-THIS.jpeg or have a mix of upper and lower case characters Like-This.jpeg then you should type it exactly like the filename

[-ee | --exclude-extensions] exclude files by their file extension in the tree listing

[-ed | --exclude-directories] exclude folders/directories in the tree listing
NOTE: just like --exclude-files argument, this one is also case sensitive

[-h | --help] show the help message

### example usage
<hr>
just running treenium without arguments will list all directories and files.

treenium "C:\path\to\your\folder"
this will list all files and folders in a specified directory.

```batchfile
treenium --exclude-files example-file.txt "example picture.png" example-doc.docx
```
```batchfile
treenium --exclude-extensions exe txt jpeg png
```
```batchfile
treenium --exclude-directories folder1 "second folder" folder3
```
```batchfile
treenium "C:\path\to\your\folder" --exclude-files "1st text file.txt" picture.png
```
```batchfile
treenium "C:\path\to\your\folder" --exclude-extensions jpeg png
```
```batchfile
treenium "C:\path\to\your\folder" --exclude-directories "3rd folder"
```
