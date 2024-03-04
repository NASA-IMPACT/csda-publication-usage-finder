# results_processor.py
# print("results_processor.py")

# Abstraction for storing the search results
from lib.storage import Storage

# # Early Documentation / Notes
# 	-We have a class which expects an input of a certain structure, and this class then processes results into a more streamlined output
#	-Mini_ETL work here
#	-Storage of searches, results, and publications should happen here.
#	-Consolidation of 'same' results should also happen here
#	 	-IMPORTANT, We need to know the datastructure of each of our [searchable_data_sources] outputs
#			-We may only be able to get a small number of fields out of EVERY datasource, and then we can store the rest as (JSON) data_source_specific_meta_data or data_source_specific_extra_data

class ResultsProcessor():
	def __init__(self):
		print("ResultsProcessor: __init__");

		# Defaults for these are dev and local_filesystem
		self.env 					= "dev" 					# Possibile Choices are: "dev", "stage", "prod"
		self.app_memory_location 	= "local_filesystem" 		# Possibile Choices are: "local_filesystem", "cloud_s3"
		self.run_id 				= "unset" 					# The run_id should be set just after instanciating this object.
		
		# Settings for where the search results are saved and loaded
		self.results_processor_dir_path = "pub_finder_runs/results_processor"
		self.results_processor_file_name_all_results = "all_runs.json"

	def set_env(self, env):
		self.env = env

	def set_app_memory_location(self, app_memory_location):
		self.app_memory_location = app_memory_location

	def set_run_id(self, run_id):
		self.run_id = run_id

	# Load from JSON, a unique list of ALL search results that were previously encountered from all runs
	# Output is an array of processed search results (dictionary objects).  This function decodes
	def load_running_list_of_all_previous_search_results(self):
		# Default is to return a blank array.
		ret__all_previous_search_results = []

		# Instancate the storage class and pass on the app memory location variable to it (so it knows if we are working with local or cloud version)
		storage_instance = Storage()
		storage_instance.set_app_memory_location(app_memory_location=self.app_memory_location)
		
		# Call the Function to save the latest search results
		dict_obj = storage_instance.load_dict_from_json_file(directory_path=self.results_processor_dir_path, file_name=self.results_processor_file_name_all_results) # all_runs.json

		# Get the array from the JSON object
		if "all_runs" in dict_obj.keys():
			ret__all_previous_search_results = dict_obj["all_runs"]
		else:
			# Could not find the key 'all_runs', maybe the file didn't exist or we have a blank object.
			print("Could not find the key 'all_runs', maybe the file didn't exist or we are trying to load results from a blank dictionary object.")

		# Return the list
		return ret__all_previous_search_results

	# Save to JSON, a unique list of ALL search results that were previously encountered from all runs (including the current run)
	# Input is an array of processed search results (dictionary objects).  This function than wraps that into a dictionary under the key 'all_runs'
	def save_running_list_of_all_previous_search_results(self, all_runs_processed_search_results):
		# Convert the search_results_list into an object, add the results as a property of that object, also add the run_id to the object
		obj_to_save = {}
		obj_to_save['all_runs'] 	= all_runs_processed_search_results
		
		# Instancate the storage class and pass on the app memory location variable to it (so it knows if we are working with local or cloud version)
		storage_instance = Storage()
		storage_instance.set_app_memory_location(app_memory_location=self.app_memory_location)
		
		# Call the Function to save the latest search results
		storage_instance.save_dict_to_json_file(data_dict=obj_to_save, directory_path=self.results_processor_dir_path, file_name=self.results_processor_file_name_all_results) # latest.json


	# Possible to deprecate - we may not need this function after all
	#
	# # Compare the current_run_id with the run_id found in the search result.  If they are the same, then this is a new result, if they are different, then this is NOT a new result.
	# def is_search_result_new(self, current_run_id, search_result):
	# 	search_result__run_id = ""
	# 	try:
	# 		search_result__run_id = search_result['run_id']
	# 	except:
	# 		search_result__run_id = ""
	#
	# 	is_result_new = False
	# 	if(search_result__run_id == current_run_id):
	# 		is_result_new = True
	#
	# 	return is_result_new

	# Properties the results_processor adds to the object being sent to reports_generator
	# 	{
	# 		'num_of_results__from_previous_saved_searches': 0,
	# 		'num_of_results__from_current_run_search': 5,
	# 		'num_of_results__presented_in_report': 5,
	# 		'search_results_to_present_in_report':
	# 		[
	# 			// One Eample here
	# 			{
	# 				'api_source': 'Scholarly (GS)',
	# 				'authors_list': ['B Osmanoglu', 'M Jo'],
	#
	# 				'pub_title': 'Commercial Smallsat Data Acquisition: Program Update',
	# 				'pub_year': '2021',
	# 				'pub_url': 'https://ieeexplore.ieee.org/abstract/document/9554702/',
	# 				'search_string': 'TODO_FINISH_HOOKING_THIS_UP',
	#
	# 				'run_id': '2024_02_14__23_07_34',
	# 				'is_new_result': True
	# 			}
	# 		]
	# 	}

	# -Look inside the 'search_result' object,
	# -determine which type of result this is,
	# -then parse the fields and keep only what is needed
	# -Ensure this is done to a constant standard that the report_generator can later process.
	# -Return the object {...} result
	def get_result_processor__search_result_object(self, search_result):
		result_processor__search_result_object = {}

		# Get the strig for the result source
		pub_search_result_source = search_result['pub_search_result_source']

		# Store the original Search Result object here as well.
		result_processor__search_result_object['original_search_result_object'] = search_result

		# Store the ID for ALL pub types
		result_processor__search_result_object['pub_id'] = search_result['pub_id']

		# SCHOLARLY LIB - Via Google Scholars
		if(pub_search_result_source == "scholarly_google_scholars"):
			result_processor__search_result_object['api_source'] 	= "Scholarly (GS)"
			result_processor__search_result_object['authors_list'] 	= search_result['pub_search_result']['bib']['author']
			result_processor__search_result_object['pub_title'] 	= search_result['pub_search_result']['bib']['title']
			result_processor__search_result_object['pub_year'] 	    = search_result['pub_search_result']['bib']['pub_year']
			result_processor__search_result_object['pub_url'] 	 	= search_result['pub_url']
			result_processor__search_result_object['search_string'] = "TODO_FINISH_HOOKING_THIS_UP" #search_result['pub_search_result']['bib']['title']
			result_processor__search_result_object['run_id'] 		= search_result['run_id']

		# OTHER API DATA SOURCE EXAMPLE
		elif(pub_search_result_source == "SOME_OTHER_SOURCE"):
			result_processor__search_result_object['api_source'] 	= "OTHER_HUMAN_READABLE_DATA_SOURCE_NAME_HERE"
			result_processor__search_result_object['authors_list'] 	= ['a1', 'a2']
			result_processor__search_result_object['pub_title'] 	= "Key_Path_to: pub_title"
			result_processor__search_result_object['pub_year'] 	    = "Key_Path_to: pub_year"
			result_processor__search_result_object['pub_url'] 	 	= search_result['pub_url']
			result_processor__search_result_object['search_string'] = "TODO_FINISH_HOOKING_THIS_UP"
			result_processor__search_result_object['run_id'] 		= search_result['run_id']

		# Default Case (just some defaults)
		else:
			result_processor__search_result_object['api_source'] 	= "UNKNOWN"
			result_processor__search_result_object['authors_list'] 	= ['person_1', 'person_2']
			result_processor__search_result_object['pub_title'] 	= "UNKNOWN"
			result_processor__search_result_object['pub_year'] 	    = "UNKNOWN"
			result_processor__search_result_object['pub_url'] 	 	= "UNKNOWN"
			result_processor__search_result_object['search_string'] = "UNKNOWN"
			result_processor__search_result_object['run_id'] 		= "UNKNOWN"

		# TODO - Remember to check the type, the type is what determines which fields that may or may not exist
		#result_processor__search_result_object['TODO'] = "Map certain fields that we need for the report_generator!"

		return result_processor__search_result_object

	def process_search_results(self, search_results):
		processed_search_results_object = {}

		# Create a set of properties from the search results - this will likely require iterating - For now, a simple example property is the length of the search results.

		# This section was replaced with: 'num_of_results__from_current_run_search'
		#
		# Get the number of search results.
		#len__search_results = len(search_results)
		#
		# Load up the Processed Search Results object
		#processed_search_results_object['num_of_results'] = len__search_results

		# An array to hold the search results that need to be placed into the report.
		search_results_to_present_in_report = []


		# TODO - Examine all the results and collate them with any previously saved search results.
		# # Note, if we only have one datasource, this may be as simple as mapping the fields from one type of result into another

		# # Items to send to the report generator:
		# How many new results,
		# How many results were previously saved
		# Sorted List of search results to present (perhaps with some kidn of tag that says "NEW_RESULT" or "PREVIOUS_RESULT")
		print("___TODO - process_search_results: SEE COMMENT ABOVE THIS LINE AND DO THOSE THINGS")

		# Load previous results, get the ids and create objects for handling specific search results.
		#previously_saved_search_results = []  # Until this gets integrated, this will be an empty list
		previously_saved_search_results = self.load_running_list_of_all_previous_search_results()
		previously_saved_search_results__pub_ids = []
		previously_saved_search_results__counter = 0
		#
		# previously_saved_search_results = <function_to_load_most_recent_saved_JSON> ### TODO - Integrate Storage RIGHT HERE - Where we load saved results from previous runs and compare their ids to see if we have seen these results before or not.  -- Save the loaded JSON into an array of dictionaries ('previously_saved_search_results')
		#
		for previously_saved_search_result in previously_saved_search_results:
			#previously_saved_search_result__run_id = previously_saved_search_result['run_id']
			#previously_saved_search_results__ids.append(result_processor__search_result_object)

			
			# We are going to need the pub_id from each of these previously saved search results in order to later compare them to our most recent search.
			previously_saved_search_result__pub_id = previously_saved_search_result['pub_id']
			previously_saved_search_results__pub_ids.append(previously_saved_search_result__pub_id)

			# Refactor - We are already savinvg these previously processed search results in the same object format.
			# # So, removing the parts where we make an object.  All we are doing here is storing the pub IDs for comparing to the new results and setting the is_new_result to false, 
			#
			# Set the is_new_result key to False (since this IS a previously seen object)
			previously_saved_search_result['is_new_result'] = False
			#
			# Make an object
			#result_processor__search_result_object = self.get_result_processor__search_result_object(search_result=previously_saved_search_result)
			#result_processor__search_result_object['is_new_result'] = False
			#
			# Append this result to the search_results_to_present_in_report array
			#search_results_to_present_in_report.append(result_processor__search_result_object)
			search_results_to_present_in_report.append(previously_saved_search_result)

			previously_saved_search_results__counter = previously_saved_search_results__counter + 1


		# Iterating to get the list of search results from the current search
		#current_search__pub_ids = []
		current_search__counter = 0
		current_search_new_results__counter = 0
		for current_search_result in search_results:
			#current_search_result__run_id = search_result['run_id']
			#current_search__pub_ids.append(current_search_result__pub_id)


			# Get the search_result_object
			result_processor__search_result_object = self.get_result_processor__search_result_object(search_result=current_search_result)
			result_processor__search_result_object['is_new_result'] = True

			# Compare the current_search_result__pub_id with the list of previously_saved_search_results__ids to see if it exists in there.  If the result previously exists, then do not save it.
			current_search_result__pub_id = current_search_result['pub_id']

			does_result_already_exist = False
			if( (current_search_result__pub_id in previously_saved_search_results__pub_ids) == True ):
				does_result_already_exist = True

			# We only want to append results that do NOT already exist (meaning only keep the new results)
			if(does_result_already_exist == False):
				# Append this result to the search_results_to_present_in_report array
				search_results_to_present_in_report.append(result_processor__search_result_object)

				# A brand new result was just added.  Incrementing the counter that keeps track of how many of those new results from the current run were found.
				current_search_new_results__counter = current_search_new_results__counter + 1

			current_search__counter = current_search__counter + 1

		# Save 'search_results_to_present_in_report' as an overwrite of the 'all_runs.json'
		self.save_running_list_of_all_previous_search_results(all_runs_processed_search_results=search_results_to_present_in_report)

		# How many results are we presenting
		len__search_results_to_present_in_report = len(search_results_to_present_in_report)

		# Load up the object for the reports_generator
		processed_search_results_object['num_of_results__from_previous_saved_searches'] = previously_saved_search_results__counter
		processed_search_results_object['num_of_results__from_current_run_search'] 		= current_search__counter
		processed_search_results_object['num_of_new_results__from_current_run_search'] 	= current_search_new_results__counter
		processed_search_results_object['num_of_results__presented_in_report'] 		    = len__search_results_to_present_in_report
		processed_search_results_object['search_results_to_present_in_report'] 			= search_results_to_present_in_report


		# Return the processed search results object
		print("ResultsProcessor.process_search_results: Reached the End.")
		return processed_search_results_object


# Comments to delete on next pass
#
# Somewhere in here, do the compare to see if this ID was seen before or not

	