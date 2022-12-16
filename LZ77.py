#explaining the code
#1. find_in_dict function is used to find the longest substring in the dictionary that matches the buffer
import os
from tkinter import Tk
from tkinter import filedialog
from art import tprint
#1. find_in_dict function is used to find the longest substring in the dictionary that matches the buffer   

def find_in_dict(buffer, dictionary):
    shift = len(dictionary)
    substring = ""
    #while the substring is in the dictionary
    
    for character in buffer:
        #add the character to the substring
        substring_tmp = substring + character
        #find the shift of the substring in the dictionary
        shift_tmp = dictionary.rfind(substring_tmp)
        #if the shift is negative, break the loop
        if shift_tmp < 0:
            break
        #if the shift is smaller than the current shift, update the shift and the substring
        substring = substring_tmp
        shift = shift_tmp
    # return the length of the substring and the shift
    return len(substring), len(dictionary) - shift

#2. compress function is used to compress the message in the LZ77 algorithm
def compress(message, buffer_size, dictionary_size):
    dictionary = ""#dictionary is empty
    buffer = message[:buffer_size]#buffer is the first 4 characters of the message

    output = []
    #while the buffer is not empty
    while len(buffer) != 0:
      #find the longest substring in the dictionary that matches the buffer
        size, shift = find_in_dict(buffer, dictionary)
        #add the substring to the dictionary
        dictionary += message[:size + 1]
        #if the dictionary is bigger than the dictionary size, remove the first characters
        dictionary = dictionary[-dictionary_size:]
        #remove the substring from the buffer
        message = message[size:]
        #if the buffer is not empty, add the first character to the output
        last_character = message[:1]
          #remove the first character from the buffer
        message = message[1:]
        #add the shift, size and last character to the output
        buffer = message[:buffer_size]
        if shift != 0 or size != 0:
            output.append((shift, size, last_character))
        else:
            output.append(last_character)
    return output

#3. decompress function is used to decompress the message in the LZ77 algorithm
def decompress(compressed_message):
    message = ""
    for part in compressed_message:
        if len(part)!=1:
            shift, size, character = part
            message = message + message[-shift:][:size] + character
        else:
            message += part
    return message
#function that opens file manager top select a file with multi selection desabled
def open_file():
    root = Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    file=filedialog.askopenfilename( title="Choose the file you want to Compress", filetypes =(("Text", "*.txt"),("All Files","*.*"),("Text", "*.txt")))
    root.update()
    root.destroy()
    return open(file, "r").read()
#function that saves the compressed file
def save_file(compressed_message):
    root = Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    file=filedialog.asksaveasfilename( title="Choose where you want to save the compressed text", filetypes =(("Text", "*.txt"),("All Files","*.*"),("Text", "*.txt")))
    root.update()
    root.destroy()
    open(file, "w").write(str(compressed_message))
#4. main function is used to test the code
if __name__ == "__main__":
    tprint("LZ77", font="block", chr_ignore=True)
    choice=input("Do you want to compress a file or decompress a file or both? (c/d/b) ")
    if choice=="b":
        #open the file
        message = open_file()
        #compress the file
        try:
            buffer, dictionary = input("Enter the buffer size and the dictionary size respectively seperated by space: ").split()
            print("buffer size: " + buffer + " dictionary size: " + dictionary)
            compressed_message = compress(message, int(buffer), int(dictionary))
        except:
            print("Invalid input, using default values")
            compressed_message = compress(message, 4, 8)
        #save the compressed file
        save_file(compressed_message)
        #decompress the file
        decompressed_message = decompress(compressed_message)
        #print the results
        print("Original message: " + message)
        print("Compressed message: " + str(compressed_message))
        print("Decompressed message: " + decompressed_message)
        print("Are the messages equal? " + str(message == decompressed_message))
    elif choice=="c":
        #open the file
        message = open_file()
        #compress the file
        try: 
            buffer, dictionary = input("Enter the buffer size and the dictionary size respectively seperated by space: ").split()
            compressed_message = compress(message, int(buffer), int(dictionary))
        except:
            print("Invalid input, using default values")
            compressed_message = compress(message, 4, 8)
        save_file(compressed_message)
    elif choice=="d":
        #open the file
        message = open_file()
        #decompress the file
        decompressed_message = decompress(message)
        #print the results
        print("Original message: " + message)
        print("Decompressed message: " + decompressed_message)
        print("Are the messages equal? " + str(message == decompressed_message))