# publication_usage_finder.py
# print("publication_usage_finder.py")

# Imports
from lib.search_phrases_manager 	import SearchPhraseManager
from lib.searchable_data_sources 	import SearchableDataSources
from lib.results_processor 			import ResultsProcessor
from lib.reports_generator 			import ReportsGenerator
from lib.reports_outputter 			import ReportsOutputter

import os
import json
import datetime

# # Early Documentation / Notes
# 	-Overall controller object which has interface functions for executing a search based on a configuration
#	-We should store things like, when a search was initited, a JSON object representing the configuration, etc

# Environments
# dev 		# Uses local file system
# stage 	# Lives in the cloud
# prod 		# Lives in the cloud

# App Memory Location
# local_filesystem 		# Configuration to run this app and saved data lives in the local filesystem
# cloud_s3 				# Configuration to run this app and saved data lives in the AWS cloud

class PublicationUsageFinder():
	def __init__(self):
		print("PublicationUsageFinder: __init__");

		# Defaults for these are dev and local_filesystem
		self.env 					= "dev" 					# Possibile Choices are: "dev", "stage", "prod"
		self.app_memory_location 	= "local_filesystem" 		# Possibile Choices are: "local_filesystem", "cloud_s3"
		
		# # Default Config - In the future, maybe load these from a file.
		# searchable_data_sources_config = {}
		# searchable_data_sources_config['use_test_results']
		# self.searchable_data_sources_config = searchable_data_sources_config
		

	def set_env(self, env):
		self.env = env

	def set_app_memory_location(self, app_memory_location):
		self.app_memory_location = app_memory_location

	# Generates a new run id based on the current UTC datetime
	def generate_new_run_id(self):
		new_run_id = datetime.datetime.utcnow().strftime('%Y_%m_%d__%H_%M_%S') 		# Example Output: '2024_02_13__17_41_38'
		return new_run_id


	# Perform a run from within airflow (assuming different settings are needed for this)
	def run__from_airflow(self):
		print("PublicationUsageFinder: run__from_airflow");

	# Perform a run from within airflow (assuming different settings are needed for this)
	def run__from_local_dev_terminal(self):
		print("PublicationUsageFinder: run__from_local_dev_terminal");


	# Rename this to the actual function that calls all the other classes and properly manages the data transport
	# Note: Production Version of this code will have the default be the production environment settings so that the deployed version works out of the box.  Dev Settings will need to be explicity set.
	def run__DRAFT(self, current__env="dev", current__app_memory_location="local_filesystem"):
		print("PublicationUsageFinder: run__DRAFT");

		# This is where the ENV and App Memory Locations are set - these are then propogated to the rest of the child classes just after their inits
		# self.set_env("dev")
		# self.set_app_memory_location("local_filesystem")
		self.set_env(current__env)
		self.set_app_memory_location(current__app_memory_location)

		# Generate a new run_id for this run
		current_run_id = self.generate_new_run_id()
		print("Current Run Id (current_run_id): " + str(current_run_id))

		# Search Phrases for this run
		search_phrase_1 = "This work utilized data made available through the NASA Commercial Smallsat Data Acquisition (CSDA) Program"

		# Create an Instance of each of the child classes, configure them and then call their functions which perform each step in the pipeline.

		# Search Phrase Manager - Keeping track of anything related to our search phrases
		searchPhraseManager 	= SearchPhraseManager();
		searchPhraseManager.set_env(self.env)
		searchPhraseManager.set_app_memory_location(self.app_memory_location)
		#
		# Add the Search Phrases
		searchPhraseManager.add_new_search_phrase(search_phrase_1)
		#
		# Get the Search Phrases
		search_phrases = searchPhraseManager.get_search_phrases()

		# Searchable Datasources - Actually performs the searches by various plugin-able child classes (or just sub-methods)
		print("TODO - Connect up SearchableDataSources - Sub Datasources (in that file 'SearchableDataSources') -- See inside of class SearchableDataSources")
		searchableDataSources 	= SearchableDataSources();
		searchableDataSources.set_env(self.env)
		searchableDataSources.set_app_memory_location(self.app_memory_location)
		searchableDataSources.set_run_id(run_id=current_run_id)
		#
		# Perform the Searches and get the Search Results
		#search_results = searchableDataSources.perform_searches(search_phrases, config=self.searchable_data_sources_config)
		#search_results = searchableDataSources.perform_searches(search_phrases)
		# # Note: setting use_local_example_search_results_data to True, so we don't hit the server unless we intend to - this prevents us from getting blocked or ip banned from doing these kinds of searches.
		search_results = searchableDataSources.perform_searches(search_phrases=search_phrases, use_local_example_search_results_data=True)

		# Results Processor - Read through the array of search_results and create a single results object as a dictionary
		resultsProcessor 		= ResultsProcessor();
		resultsProcessor.set_env(self.env)
		resultsProcessor.set_app_memory_location(self.app_memory_location)
		resultsProcessor.set_run_id(run_id=current_run_id)
		#
		# Process the results into a python dictionary
		processed_search_results_object = resultsProcessor.process_search_results(search_results)

		# Read the Processed Search Results dictionary and generate 1 or more reports
		reportsGenerator 		= ReportsGenerator();
		reportsGenerator.set_env(self.env)
		reportsGenerator.set_app_memory_location(self.app_memory_location)
		reportsGenerator.set_run_id(run_id=current_run_id)
		#
		# Generate a simple text report
		report__text = reportsGenerator.generate_report__simple_text(processed_search_results_object)
		# Note - We could have other methods like, generate_report__pdf, or slide_show, or email or spreadsheet, etc

		reportsOutputter 		= ReportsOutputter();
		reportsOutputter.set_env(self.env)
		reportsOutputter.set_app_memory_location(self.app_memory_location)
		#
		# TODO - Perform some kind of set of output functions with the report (Print to the console, Email results, Send results to a slack channel, etc?)
		


		# Debug - Local Outputs - To prove that the communication between classes is working properly
		print("PublicationUsageFinder: (search_phrases):                  " + str(search_phrases))
		print("PublicationUsageFinder: (search_results):                  " + str(search_results))
		print("PublicationUsageFinder: (processed_search_results_object): " + str(processed_search_results_object))
		#print("PublicationUsageFinder: (report__text):                    " + str(report__text))
		print("PublicationUsageFinder: (report__text):                    " + "Next Lines")
		#
		print("")
		print("")
		print(str(report__text))
		print("")

		print("")
		print("PublicationUsageFinder.run__DRAFT: Reached the End.")



# # REMOVE ME 		START
# #
# 	def create_directory(self, directory_path):
# 		"""Ensure the directory exists."""
# 		os.makedirs(directory_path, exist_ok=True)

# 	def save_json(self, data, file_path):
# 		"""Save data to a JSON file."""
# 		with open(file_path, 'w') as file:
# 			json.dump(data, file, indent=4)



# 	"""Append the new search result to 'all_runs.json', avoiding duplicates."""

# 	def append_to_all_runs(self, data, directory_path):
# 		if not isinstance(data, dict) or 'unique_identifier' not in data:
# 			print("Error: 'data' is not structured correctly.")
# 			return

# 		all_runs_path = os.path.join(directory_path, 'all_runs.json')
# 		if os.path.exists(all_runs_path):
# 			with open(all_runs_path, 'r+') as file:
# 				try:
# 					all_runs_data = json.load(file)
# 					if 'results' not in all_runs_data or not isinstance(all_runs_data['results'], list):
# 						print("Error: 'all_runs_data' does not contain a 'results' list.")
# 						return
# 				except json.JSONDecodeError:
# 					print("Error decoding JSON from 'all_runs.json'.")
# 					return

# 				# Ensure every item in 'results' is a dict before calling .get()
# 				existing_identifiers = [result['unique_identifier'] for result in all_runs_data['results'] if
# 										isinstance(result, dict) and 'unique_identifier' in result]

# 				if data['unique_identifier'] not in existing_identifiers:
# 					all_runs_data['results'].append(data)
# 					file.seek(0)
# 					file.truncate()
# 					json.dump(all_runs_data, file, indent=4)
# 		else:
# 			self.save_json({'results': [data]}, all_runs_path)

# 	def manage_search_results(self, results, directory_path='pub_finder_runs'):
# 		"""Handle the entire process of saving and managing search results."""
# 		self.create_directory(directory_path)
# 		run_id = self.generate_new_run_id()
# 		run_specific_file_path = os.path.join(directory_path, f'{run_id}.json')
# 		latest_file_path = os.path.join(directory_path, 'latest.json')

# 		# Assume `results` is a list of dictionaries, each representing a search result
# 		for result in results:
# 			# Extract necessary information from each result
# 			data_to_save = {
# 				# "unique_identifier": result["pub_hash"],  # Use 'pub_hash' as unique identifier
# 				"unique_identifier": result["pub_url"], # use this for formatted report
# 				"data": result  # Save the entire result under 'data' key
# 			}

# 			# Append the search result to 'all_runs.json', avoiding duplicates
# 			self.append_to_all_runs(data_to_save, directory_path)

# 		# Optionally, save the whole set of results to run-specific and latest files
# 		self.save_json(results, run_specific_file_path)
# 		self.save_json(results, latest_file_path)
# #
# self.manage_search_results(search_results, 'pub_finder_runs') #deatiled results
# self.manage_search_results(processed_search_results_object['search_results_to_present_in_report'],'pub_finder_runs')


# # REMOVE ME 		END

# END OF FILE