from __future__ import with_statement
from enum import Enum
import csv
import numpy as np
import pandas as pd
import math
import cv2

class NAME(Enum):
	index = 0,
	palm = 1,
	fist = 2,
	grap = 3,
	hand = 4
	
image = None
title = ""
##### Windows : 
path = '../images/round 2/index(0)'
path_where_to_save = '../datasets'
images_paths = []
images = []
nb_repeated = 1
name_csv = 'not_mixed_database.csv'

# WRITING VARIABLES
nb_images_to_write = 200
label_write = NAME.palm.value

# MIXING ELEMENTS
times_of_mixing = 1

def progressBar(current, total, barLength = 20):
    percent = float(current) * 100 / total
    arrow   = '-' * int(percent/100 * barLength - 1) + '>'
    spaces  = ' ' * (barLength - len(arrow))

    print('\t > Progress: [%s%s] %d %%' % (arrow, spaces, percent), end='\r')

	#''' --------------------------------------- presentation ---------------------------------------'''
print("----------------------------------- PRESENTATION -----------------------------------")
print("- \t This program allows you to:                                               -")
print("- \t\t 1) Read csv files and convert each row to an image                -")
print("- \t\t 2) Read csv files mix elements inside and write another one       -")
print("------------------------------------------------------------------------------------")

choise = input("-> What do you want to do? \n\t >  Tape 'r' if you want to read \n\t >  Type 'w' if you want to write \n\t >  Type 'm' if you want to mix elements \n\t >  Type 'q' if you want to quit\n-> Your answer is: ")

if choise == 'w':
	''' --------------------------------------- Writing file ---------------------------------------'''
	#       ------ Change names of files
	print("The default name of the csv file is : " + name_csv)
	answer_change_csv_name = input("If you want to keep it type 'y', otherwise type 'n' : ")
	if answer_change_csv_name == 'n' or answer_change_csv_name == "'n'":
		n_name_csv = input("-> Type the new name for the csv file WITH THE EXTENSION  (Type '/' if don't want to change) : \n\t > ")
		if n_name_csv != "/" and n_name_csv != "'/'":
			name_csv = n_name_csv
			print("The new name of the csv file is : " + name_csv)
		else:
			print("You've chosen to keep the default one !")
	elif answer_change_csv_name == 'q':
		print("You've decided to quit the program. Have a good day and God bless you !")
		quit()

	#       ------ Change paths
	print("The default path for saving the csv file is : \n\t > " + path_where_to_save)
	print("The default path from where the images are situated is  : \n\t > " + path)
	answer_change_path = input("-> If you want to keep the default settings type 'y', otherwise type 'n' : ")
	if answer_change_path == 'n' or answer_change_path == "'n'":
		n_path_where_to_save = input("-> Type the new path where to save the csv file (Type '/' if don't want to change) : \n\t > Your answer : ")
		n_path = input("-> Type the new path leading to the images (Type '/' if don't want to change) : \n\t > Your answer : ")
		if n_path != "/" and n_path != "'/'":
			path = n_path
			print("The new path leading to the images is :" + path)
		else:
			print("You've chosen the default path leading to the images !\n")

		if n_path_where_to_save != "/" and n_path_where_to_save != "'/'":
			path_where_to_save = n_path_where_to_save
			print("The new path for the csv file is :" + path_where_to_save)
		else:
			print("You've chosen the default path to save the csv file !\n")
	elif answer_change_path == 'q':
		print("You've decided to quit the program. Have a good day and God bless you !")
		quit()

	#       ------ Changes nb images to write
	print("The number of images you want to convert into csv is actualy = "+ str(nb_images_to_write)+ ". Keep in mind that if in your file you have less than "+ str(nb_images_to_write)+ " images, you will have an overflow!")
	answer_change_nb_images = input("-> If you want to keep it type 'y', otherwise type 'n' : ")
	if answer_change_nb_images == 'n' or answer_change_nb_images == "'n'":
		nb_images_to_write = int(input("-> Tape the new number of images you want to convert : "))

	elif answer_change_nb_images == 'q':
		print("You've decided to quit the program. Have a good day and God bless you !")
		quit()
	else:
		print("You've chosen the default settings!\n")
	
	print("You will convert "+str(nb_images_to_write)+" * 2 * "+str(nb_repeated)+" (times we repete an image) images, so "+str(nb_images_to_write*2*nb_repeated)+" images.")


	#       ------ Change the label of the images
	print("The default label we are saving images with is : "+ str(label_write))
	answer_change_label_write = input("-> If you want to keep it type 'y', otherwise type 'n' : ")
	if answer_change_label_write == 'n' or answer_change_label_write == "'n'":
		print("Your options are : ")
		for x in NAME:
				print("\t > id : {}, value : {} ".format(x.value, x.name))
		label_write = int(input("-> Tape the id you want to used : "))

	elif answer_change_label_write == 'q':
		print("You've decided to quit the program. Have a good day and God bless you !")
		quit()
	else:
		print("You've chosen the default settings!\n")

	#       ------ Reading images, resizing them and writing the csv file
	print("Loading and resizing images (it could take a while)...")
	i = 0
	dim = (100, 100)
	# print("\t > Images already read : ", end=" ")
	while(i < nb_images_to_write):
		img = cv2.resize(cv2.imread(path + '/' + str(i+1) + '.jpg', 0), dim, interpolation = cv2.INTER_AREA)  # 0 to read grayscale mode
		images.append(img)
		inv = np.flip(img, 1)
		images.append(inv)
		progressBar(i+1, nb_images_to_write)
		i += 1
	print("")
	print("-> " + str(i) + " images were read!")
	print("Images resized.")

	print("Saving images into csv to path : " + path_where_to_save)
	print("> We have to do the loop : " + str(len(images)))
	
	with open(path_where_to_save + '/'+name_csv, 'a', newline='') as out3:
		csv_writer = csv.writer(out3, delimiter=',')
		for index, img in enumerate(images):
			progressBar(index+1, len(images))
			data = [label_write]
			data = np.append(data, img.flatten())
			csv_writer.writerow(data)

	print("")
	print("CSV file writen!")


elif choise == 'r':
	''' --------------------------------------- Reading file ---------------------------------------'''

	#       ------ Change names of files
	print("The default name of the csv file is : " + name_csv)
	answer_change_csv_name = input("-> If you want to keep it type 'y', otherwise type 'n' : ")
	if answer_change_csv_name == 'n' or answer_change_csv_name == "'n'":
		n_name_csv = input("-> Type the new name for the csv file WITH THE EXTENSION  (Type '/' if don't want to change) : \n\t > ")
		if n_name_csv != "/" and n_name_csv != "'/'":
			name_csv = n_name_csv
			print("The new name of the csv file is : " + name_csv)
		else:
			print("You've chosen to keep the default one !")
	elif answer_change_csv_name == 'q':
		print("You've decided to quit the program. Have a good day and God bless you !")
		quit()

	#       ------ Change paths
	print("The default path for the csv file is : " + path_where_to_save)
	answer_change_path = input("-> If you want to keep the default one type 'y', otherwise type 'n' : ")
	if answer_change_path == 'n' or answer_change_path == "'n'":
		n_path_where_to_save = input("-> Type the new path for the csv file (Type '/' if don't want to change) : \n\t > ")
		if n_path_where_to_save != "/" and n_path_where_to_save != "'/'":
			path_where_to_save = n_path_where_to_save
			print("The new path for the csv file is :" + path_where_to_save)
		else:
			print("You've chosen the default path to save the csv file !")
		print("Change done!")
	elif answer_change_path == 'q':
		print("You've decided to quit the program. Have a good day and God bless you !")
		quit()

	#       ------ Reading and processing the csv file
	print("Reading the csv file...")

	#       ------ Read the csv file
	df = []
	with open(path_where_to_save + '/'+name_csv) as f:
		reader = csv.reader(f)
		for  l in reader:
			df.append(l)

	nb_images = len(df)
	df = pd.DataFrame(df) # Convert the list into pandas DataFrame

	print("There are "+ str(nb_images)+ " images.")
	print("Please enter the number of images you want to show as following : ex : From 5 to 10!")
	print("If you want to quit the program and to show no image, just enter a negative number for FROM of for TO !")

	FROM = input("-> From : ")
	FROM = int(FROM)
	if FROM < 0:
		print("You decided to show no image and quit the program. Have a good day and God bless you !")
		quit()

	TO = input("-> to : ")
	TO = int(TO)
	if FROM < 0 or TO < 0:
		print("You decided to show no image and quit the program. Have a good day and God bless you !")
		quit()

	print("We are showing you images from "+ str(FROM)+ " to "+ str(TO)+ ". Please wait a few seconds! ")

	for i in range(FROM, TO+1):
		title = df.values[i][0] # Take the label
		im_buffer = df.values[i][1:] # create dlat array of only the pixels of the given image
		axis_len = int(math.sqrt(im_buffer.shape[0])) # take the dimensions of the image
		im_array = np.uint8(np.reshape(im_buffer, (axis_len, axis_len))) # Reshape the image from 1D to 2D

		cv2.imshow(str(i)+": "+str(title), im_array)

	print("Here you are!")
	print("Tape 'q' in order to quit the program !")
	cv2.waitKey(0)
	cv2.destroyAllWindows()

elif choise == 'm':
	''' --------------------------------------- Mixing the elements in the csv file ---------------------------------------'''
	#       @@@@@@ Reading the file

	#       ------ Change names of files
	print("The default name of the csv file you want to mix is : " + name_csv)
	answer_change_csv_name = input("-> If you want to keep it type 'y', otherwise type 'n' : ")
	if answer_change_csv_name == 'n' or answer_change_csv_name == "'n'":
		n_name_csv = input("-> Type the new name for the csv file WITH THE EXTENSION  (Type '/' if don't want to change) : \n\t > ")
		if n_name_csv != "/" and n_name_csv != "'/'":
			name_csv = n_name_csv
			print("The new name of the csv file is : " + name_csv)
		else:
			print("You've chosen to keep the default one !")
	elif answer_change_csv_name == 'q':
		print("You've decided to quit the program. Have a good day and God bless you !")
		quit()

	#       ------ Change paths
	print("The default path from where to get the csv file is : " + path_where_to_save)
	answer_change_path = input("-> If you want to keep the default one type 'y', otherwise type 'n' : ")
	if answer_change_path == 'n' or answer_change_path == "'n'":
		n_path_where_to_save = input("-> Type the new path for the csv file (Type '/' if don't want to change) : \n\t > ")
		if n_path_where_to_save != "/" and n_path_where_to_save != "'/'":
			path_where_to_save = n_path_where_to_save
			print("The new path for the csv file is :" + path_where_to_save)
		else:
			print("You've chosen the default path to save the csv file !")
		print("Change done!")
	elif answer_change_path == 'q':
		print("You've decided to quit the program. Have a good day and God bless you !")
		quit()

	 #       ------ Change times_of_mixing
	print("By default the elements wil be mixed "+ str(times_of_mixing) + " times.")
	answer_change_time_of_mixing = input("-> If you want to keep the default number type 'y', otherwise type 'n' : ")
	if answer_change_time_of_mixing == 'n' or answer_change_time_of_mixing == "'n'":
		times_of_mixing = int(input("-> Type the number of times you want to mix elements : "))
		print("The elements will be mixed " + str(times_of_mixing) + " times.")
		
	elif answer_change_time_of_mixing == 'q':
		print("You've decided to quit the program. Have a good day and God bless you !")
		quit()
	else:
		print("You've chosen to keep the default one !")

	#       ------ Reading and processing the csv file
	df = []
   
	with open(path_where_to_save + '/' +name_csv) as f:
		reader = csv.reader(f)
		for l in reader:
			df.append(l)
			

			

	nb_images = len(df)
	df = pd.DataFrame(df) # Convert the list into pandas DataFrame
	print("> Before dropping the NA there are "+ str(len(df))+ " images.")
	elem = df.sample(frac=1).reset_index(drop=True)
	elem = elem.dropna() # DataFrame adds NA elements, so we need to take them out ( we delete all rows containing a NA)
	nb_images = len(elem)
	elements = elem.values.tolist()
	print("> After dropping the NA there are "+ str(len(df))+ " images.")

	#       @@@@@@ Writing the new file
	name_of_new_file = "mixed_file.csv"

	print("\nNow you have to create a new csv file containing the new mixed elements.")
	print("The default settings are : ")
	print("\tName of file : "+ name_of_new_file)
	print("\tThe path where to save the file is : "+ path_where_to_save)

	answer_change_new_csv_settings = input("-> If you want to keep the default settings type 'y', otherwise type 'n' : ")
	if answer_change_new_csv_settings == 'n' or answer_change_new_csv_settings == "'n'":
		
		n_name_csv = input("\t -> Type the new name for the csv file WITH THE EXTENSION (Type '/' if don't want to change) : \n\t > ")
		
		if n_name_csv != "/" and n_name_csv != "'/'":
			name_of_new_file = n_name_csv
			print("The new name of the csv file is : " + name_of_new_file)
		else:
			print("You've chosen to keep the default name !")

		n_path_csv = input("\t -> Type the new path where save the file to (Type '/' if don't want to change) : \n\t > ")
		
		if n_path_csv != "/" and n_path_csv != "'/'":
			path_where_to_save = n_path_csv
			print("The new name of the csv file is : " + path_where_to_save)
		else:
			print("You've chosen to keep the default path !")
	elif answer_change_new_csv_settings == 'q':
		print("You've decided to quit the program. Have a good day and God bless you !")
		quit()
	#       ------ Writting
	print("Writting the new file...")

	with open(path_where_to_save + '/'+name_of_new_file, 'a', newline='') as out_new_csv:
		csv_writer = csv.writer(out_new_csv, delimiter=',')
		for index, element in enumerate(elements):
			csv_writer.writerow(element)
			progressBar(index+1,len(elements))

	print("")
	print("The new file was created succesfully!")
	print("Execution ended succesfully. Have a good day and God bless you !")

	
elif choise == 'q':
	print("You've decided to quit the program. Have a good day and God bless you !")
	quit()
else:
	print("We don't understand your choise, so by default we chose to quit the program. Have a good day and God bless you !")