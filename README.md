<div align="center">
  <img width="250" src ="https://github.com/OscarDogar/MetaDataRenamer/assets/60854050/5c157e98-daea-47cc-88fc-791b1f222074"/>
  <h1>Meta Data Renamer</h1>
</div>

<h3>A metadata renamer to remove or replace titles and metadata names of audio tracks, subtitles and images.</h3>

## Requirements 
- Install [MKVToolNix](https://mkvtoolnix.download/downloads.html)
- Install requirements.txt
- Add MKVToolNix path to windows. 

## Example

Using VLC to view available subtitles. In this case we will change the name of this subtitles by changing the string *test* to *new name*.

![image](https://github.com/OscarDogar/MetaDataRenamer/assets/60854050/3ad36852-c737-44c9-9b77-52b6c5fcab43)

1. We need to change the .env KEYWORDS to the keywords we want to change.

    ```KEYWORDS = "test"```
   
2. When we run the program, it will ask for the path where the files are located, and then the name we want to replace the KEYWORDS with.
   
   2.1. The path will look something like this: ```C:\Users\myuser\Videos\```
   
   2.2. After that, the replace string in this case will be: *new name*
   
3. Then the program will start and change all matches to the *new name*.
   
![image](https://github.com/OscarDogar/MetaDataRenamer/assets/60854050/6a2b417b-162d-47da-a108-b375258d6067)

4. This works for audio, titles, subtitles and attachments.
