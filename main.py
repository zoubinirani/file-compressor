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

def decompressFileWindow(path):
    layout = [[sg.Text('Decompressing...' + path)]]
    window = sg.Window('Decompressing File', layout)
    while True:
        event, values = window(timeout=0)
        decompress_path = decompressFile(path)
        break
    window.close()
    decompressResultsWindow(path, decompress_path)

def resultsWindow(original_path, compress_path):
    new_size = round(os.stat(original_path).st_size / 1000000, 2)
    savings = 1 - os.stat(compress_path).st_size / os.stat(original_path).st_size
    layout = [[sg.Text('Success!')],
             [sg.Text('Your compressed file is ' + str(new_size) + "MB and is " + 
              str("{:.1%}".format(savings)) + " smaller than the original.")],
             [sg.Submit(button_text = "Compress/Decompress Another File", key="Submit"),
              sg.Cancel(button_text = "Close", key="Close")]]
    window = sg.Window('Summary', layout)
    while True:
        event, values = window.read()
        if event in ('Close', None):
            break
        window.close()
        selectFileWindow()
    window.close()
    
def decompressResultsWindow(original_path, decompress_path):
    new_size = round(os.stat(original_path).st_size / 1000000, 2)
    savings = 1 - os.stat(original_path).st_size/os.stat(decompress_path).st_size
    layout = [[sg.Text('Success!')],
             [sg.Text('Your decompressed file is ' + str(new_size) + "MB and is " + 
              str("{:.1%}".format(savings)) + " larger than the original.")],
             [sg.Submit(button_text = "Compress/Decompress Another File", key="Submit"),
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
    layout = [[sg.Text('Select your file to compress or decompress.')],
         [sg.Input(key="Input"), sg.FileBrowse(key="Browse")],
         [sg.Submit(button_text = "Compress", key="Compress"),
          sg.Submit(button_text = "Decompress", key="Decompress"), 
          sg.Cancel(button_text = "Close", key="Close")]]
    window = sg.Window('File Compressor', layout)
    
    while True:
        event, values = window.read()
        if event in ('Close', None):
            break
        elif event in ('Compress'):
            if not values['Browse']:
                selectFileWindow()
            else:
                compressFileWindow(path=values['Browse'])
        elif event in ('Decompress'):
            if not values['Browse'] or ".gz" not in values['Browse']:
                selectFileWindow()
            else:
                decompressFileWindow(path=values['Browse'])
        window.close()
    window.close()
    
def compressFile(path):
    with open(path, 'rb') as f_in:
        folder_path, file_name = extractFolderPath(path)
        compress_path = folder_path + file_name + '.gz'
        with gzip.open(compress_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        return compress_path

def decompressFile(path):
    with open(path, 'rb') as f_in:
        decompress_path = path[:-3]
        with gzip.open(decompress_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        return decompress_path

def main():
    sg.theme('Default1')
    selectFileWindow()
    return 0

if __name__ == "__main__":
    main()