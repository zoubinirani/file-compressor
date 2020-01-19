#!/usr/bin/env python

import PySimpleGUI as sg
import gzip
import os
import shutil

def extractFolderPath(path):
    path = path.split("/")
    file_name = path[-1]
    path = path[0:-1]
    folder_path = ""
    for folder in path:
        folder_path += folder + "/"
    return folder_path, file_name
    
def compressFileWindow(path):
    layout = [[sg.Text('Compressing...' + path)]]
    window = sg.Window('Compressing File', layout)
    while True:
        event, values = window(timeout=0)
        compress_path = compressFile(path)
        break
    window.close()
    resultsWindow(path, compress_path)

def resultsWindow(original_path, compress_path):
    new_size = round(os.stat(original_path).st_size / 1000000, 2)
    savings = 1 - os.stat(compress_path).st_size / os.stat(original_path).st_size
    layout = [[sg.Text('Success!')],
             [sg.Text('Your compressed file is ' + str(new_size) + "MB and is " + 
              str("{:.1%}".format(savings)) + " smaller than the original.")],
             [sg.Submit(button_text = "Compress Another File", key="Submit"),
              sg.Cancel(button_text = "Close", key="Close")]]
    window = sg.Window('Summary', layout)
    while True:
        event, values = window.read()
        if event in ('Close', None):
            break
        window.close()
        selectFileWindow()
    window.close()
    
def selectFileWindow():
    layout = [[sg.Text('Select your file to compress.')],
         [sg.Input(key="Input"), sg.FileBrowse(key="Browse")],
         [sg.Submit(key="Submit"), sg.Cancel(key="Cancel")]]
    window = sg.Window('File Compressor', layout)
    
    while True:
        event, values = window.read()
        if event in ('Cancel', None):
            break
        window.close()
        compressFileWindow(path=values['Browse'])
    window.close()
    
def compressFile(path):
    with open(path, 'rb') as f_in:
        folder_path, file_name = extractFolderPath(path)
        compress_path = folder_path + file_name + '.gz'
        with gzip.open(compress_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        return compress_path
    
def main():
    sg.theme('Default1')
    selectFileWindow()
    return 0

if __name__ == "__main__":
    main()