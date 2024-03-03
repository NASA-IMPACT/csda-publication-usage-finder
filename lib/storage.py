# storage.py
# Handles storage for local and cloud based runs

# Imports
import os
import json
#import boto3

# Handles storage for local filesystem based runs
class StorageLocal():
	def __init__(self):
		pass 

	# Create a local directory if it does not already exist
	@staticmethod
	def create_directory_if_not_exists(directory_path=""):
		# Check if the directory path is not blank
		if directory_path:
			# Check if the directory does not already exist
			if not os.path.exists(directory_path):
				# Create the directory
				os.makedirs(directory_path)
				print(f"Directory created at: {directory_path}")
			else:
				print("Directory already exists.")
		else:
			print("No directory path provided.")
		
	@staticmethod
	def save_dict_to_json_file(data_dict, directory_path, file_name):
		# Create the save directory if it does not exist.
		StorageLocal.create_directory_if_not_exists(directory_path=directory_path)
		
		# Generate the full file path
		full_file_path = os.path.join(directory_path, file_name)

		# Save a dictionary to a JSON file.
		with open(full_file_path, 'w') as file:
			json.dump(data_dict, file, indent=4)
		print(f"Dictionary Saved to {full_file_path}")

	# This is just loading the data and sending to the function who called it.
	@staticmethod
	def load_dict_from_json_file(directory_path, file_name):
		# Object to return
		ret_dict_obj = {}

		# Generate the full file path
		full_file_path = os.path.join(directory_path, file_name)

		# If the file does not already exist, there is nothing to load.
		if os.path.exists(full_file_path):
			try:
				with open(full_file_path, 'r') as file:
					ret_dict_obj = json.load(file)
				print(f"Dictionary Loaded from {full_file_path}")
			except:
				print("There was an error when trying to load the json file: " + str(full_file_path))
		else: 
			print("There was no file found at: " + str(full_file_path) + "  Does the file and/or path exist?")

		return ret_dict_obj

	@staticmethod
	def save_string_to_file(string_to_save, directory_path, file_name):
		# Create the save directory if it does not exist.
		StorageLocal.create_directory_if_not_exists(directory_path=directory_path)
		
		# Generate the full file path
		full_file_path = os.path.join(directory_path, file_name)

		# Save a dictionary to a JSON file.
		with open(full_file_path, 'w') as file:
			file.write(string_to_save)
		print(f"String Saved to {full_file_path}")

# Handles storage for cloud based runs using S3 as the storage location
#
# Prerequisites
# # Create an S3 bucket where we will store all these runs (in the same or simillar structure to how local filesystem files are stored)
# # Create a iam role (or an assumed role) which has read/write access to this S3 bucket.
class StorageS3():
	def __init__(self):
		pass

	# PLACEHOLDER # Create S3 bucket if not exists

	# PLACEHOLDER # Create IAM Role/Assumed Role if not exists


# Abstraction which handles which class to use (so we can call a single function like load_json or save_json, and based on the environment is which other Storage class gets used (StorageLocal, or StorageS3))
class Storage():
	def __init__(self):
		self.app_memory_location 	= "local_filesystem" 		# Possibile Choices are: "local_filesystem", "cloud_s3"
		
	def set_app_memory_location(self, app_memory_location):
		self.app_memory_location = app_memory_location

	def save_dict_to_json_file(self, data_dict, directory_path, file_name):
		# TODO - Check ENV variable, call the correct save function based on the env variable.
		# # if(self.app_memory_location == "local_filesystem"):
		#
		# Placeholder - just call the save local function
		StorageLocal.save_dict_to_json_file(data_dict=data_dict, directory_path=directory_path, file_name=file_name)

	def load_dict_from_json_file(self, directory_path, file_name):
		# The object to be returned.
		ret_dict_obj = {}
		#
		# TODO - Check ENV variable, call the correct save function based on the env variable.
		#
		# Placeholder - just call the save local function
		ret_dict_obj = StorageLocal.load_dict_from_json_file(directory_path=directory_path, file_name=file_name)
		#
		return ret_dict_obj

	def save_string_to_file(self, string_to_save, directory_path, file_name):
		# TODO - Check ENV variable, call the correct save function based on the env variable.
		# # if(self.app_memory_location == "local_filesystem"):
		#
		# Placeholder - just call the save local function
		StorageLocal.save_string_to_file(string_to_save=string_to_save, directory_path=directory_path, file_name=file_name)





# END OF FILE