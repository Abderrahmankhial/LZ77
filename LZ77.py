#explaining the code
#1. find_in_dict function is used to find the longest substring in the dictionary that matches the buffer
import os
from tkinter import Tk
from tkinter import filedialog
import art
import text2art
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
            #add the shift, size and last character to the output
            output.append((shift, size, last_character))
        else:
            #add the last character to the output if the shift and size are 0
            output.append(last_character)
    return output

#3. decompress function is used to decompress the message in the LZ77 algorithm
def decompress(compressed_message):
    message = ""
    
    for part in compressed_message:
        #if the part is a tuple, add the substring to the message
        if len(part)!=1:
            shift, size, character = part
            message = message + message[-shift:][:size] + character
        else:
            #if the part is not a tuple, add the character to the message
            message += part
    return message
#function that opens file manager top select a file with multi selection desabled
def open_file(title):
    root = Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    file=filedialog.askopenfilename(title=title,filetypes=[("Text Files", "*.txt")])
    if file=="":
        return "no file selected.error"
    root.update()
    root.destroy()
    return open(file, "r").read()
#function that saves the compressed file
def save_file(compressed_message, Title ,):
    root = Tk()#create a window
    root.withdraw()
    root.wm_attributes('-topmost', 1)#make the window appear on top of all other windows
    file=filedialog.asksaveasfilename(title=Title,filetypes=[("Text Files", "*.txt")])#save the file as a text file
    if file=="":#if the user didn't select a file, save the file in the same directory as the program under the name output.txt
        file="output.txt"
    root.update()
    root.destroy()
    open(file, "w").write(str(compressed_message))#write the compressed message to the file
#function that selects a file and checks if the file is empty or too big or if the user didn't select a file
def select_file(title):
    is_selected=False
    while is_selected!= True:
            message = open_file(title)
            if message=="":#if the file is empty
                print("The file is empty, select another file")
                pass
            elif len(message)>1000000:#if the file is too big
                print("The file is too big, choose another file")
                pass
            elif message=="no file selected.error":#if the user didn't select a file
                print("No file selected, Select a file")
                pass
            elif message!="":#if the file is valid exit the loop and return the message
                is_selected=True
                return message
#4. main function is used to run the code
if __name__ == "__main__":
    try:
        print("\033[1;32m")#set the color of the text to green
        art.tprint("LZ77", font="block", chr_ignore=True)#print the title
        choice=input("Do you want to compress a file or decompress a file or both? (c/d/b) ")#get the choice from the user
        if choice=="b":
            #open the file
            message = select_file("Choose the file you want to compress")
            #compress the file
            try:
                #get the buffer size and the dictionary size from the user
                buffer, dictionary = input("Enter the buffer size and the dictionary size respectively seperated by space: ").split()
                print("buffer size: " + buffer + " dictionary size: " + dictionary)
                compressed_message = compress(message, int(buffer), int(dictionary))#compress the file
            except:
                #if the user enters invalid input, use the default values
                print("Invalid input, using default values")
                compressed_message = compress(message, 4, 8)
            #save the compressed file
            save_file(compressed_message, "Choose the file you want to save the compressed file to")
            #decompress the file
            decompressed_message = decompress(compressed_message)
            #print the results
            print("Original message: " + message)
            print("Compressed message: " + str(compressed_message))
            print("Decompressed message: " + decompressed_message)
            print("Are the messages equal? " + str(message == decompressed_message))
        elif choice=="c":
            #open the file
            message = select_file("Choose the file you want to compress")
            #compress the file
            try: 
                buffer, dictionary = input("Enter the buffer size and the dictionary size respectively seperated by space: ").split()
                print("buffer size: " + buffer + " dictionary size: " + dictionary)
                compressed_message = compress(message, int(buffer), int(dictionary))
            except:
                print("Invalid input, using default values")
                compressed_message = compress(message, 4, 8)
            save_file(compressed_message, "Save the compressed file")
        elif choice=="d":
            #open the file
            message = select_file("Choose the file you want to decompress")
            #convert the string to a list
            x=eval(message)
            #decompress the file
            decompressed_message = decompress(x)
            #print the results
            print("Decompressed message: " + decompressed_message)
            save= input("Do you want to save the decompressed message? (y/n) ")
            if save=="y":
                save_file(decompressed_message, "Save the decompressed file")
            else:
                exit()
        else:
            print("Invalid input")
    except KeyboardInterrupt:
        x=input("\nDo you want to exit? (y/n) ")
        if x=="y":
            out=art.text2art("Goodbye",font="rnd-small")
            print(out)
            exit()
        else:
            pass
        
