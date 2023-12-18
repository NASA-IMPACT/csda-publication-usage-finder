# searchable_data_sources.py
# print("searchable_data_sources.py")

# Imports
# Dir 'data_sources' has the datasources manipulated by this class.

# # Early Documentation / Notes
# 	-We have a list of data sources (enumerated list of strings), each string points to a different class that actually does the searching work
#	-Each of these class instances may have their own logic, but should also conform to expected input/output standards.

class SearchableDataSources():
	def __init__(self):
		print("SearchableDataSources: __init__");

		# Defaults for these are dev and local_filesystem
		self.env 					= "dev" 					# Possibile Choices are: "dev", "stage", "prod"
		self.app_memory_location 	= "local_filesystem" 		# Possibile Choices are: "local_filesystem", "cloud_s3"

		

	def set_env(self, env):
		self.env = env

	def set_app_memory_location(self, app_memory_location):
		self.app_memory_location = app_memory_location

	
	@staticmethod
	def create_search_result_object(input_param_1, input_param_2, other_params):
		search_result_object = {}
		search_result_object['prop_1'] = input_param_1
		search_result_object['prop_2'] = input_param_2
		search_result_object['prop_3'] = other_params
		return search_result_object


	# TODO - Connect multiple methods of searching inside of this function.
	def perform_searches(self, search_phrases):
		print("SearchableDataSources.perform_searches: TODO - Convert this so that it creates instances of child classes for each API we are searching and call them.")

		# An object to hold a standard dictionary for each search result
		search_results = []

		# (1) Try and Call Each of the search methods to get results.

		# (2) Collate the results into a standard way
		search_result_obj_1 = SearchableDataSources.create_search_result_object("Property_1a", "Property_2a", "Property_3a")
		search_result_obj_2 = SearchableDataSources.create_search_result_object("Property_1b", "Property_2b", "Property_3b")
		search_results.append(search_result_obj_1)
		search_results.append(search_result_obj_2)

		# Just some in context notes.
		print("SearchableDataSources.perform_searches: TODO - We will likely need to store search results (and possibly publications as well) - so we can identify what was previously found vs what might be new.")
		print("SearchableDataSources.perform_searches: TODO - Future Version may even anaylyze the content of the publications")

		# (3) Return the results
		print("SearchableDataSources.perform_searches: Reached the End.")
		return search_results
		