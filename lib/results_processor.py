# results_processor.py
# print("results_processor.py")


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
		

	def set_env(self, env):
		self.env = env

	def set_app_memory_location(self, app_memory_location):
		self.app_memory_location = app_memory_location

	def process_search_results(self, search_results):
		processed_search_results_object = {}

		# Create a set of properties from the search results - this will likely require iterating - For now, a simple example property is the length of the search results.

		# Get the number of search results.
		len__search_results = len(search_results)

		# Load up the Processed Search Results object
		processed_search_results_object['num_of_results'] = len__search_results

		# TODO - Examine all the results and collate them with any previously saved search results.
		# # Note, if we only have one datasource, this may be as simple as mapping the fields from one type of result into another

		# Return the processed search results object
		print("ResultsProcessor.process_search_results: Reached the End.")
		return processed_search_results_object
	