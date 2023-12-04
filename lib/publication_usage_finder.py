# publication_usage_finder.py
# print("publication_usage_finder.py")

# Imports
from lib.search_phrases_manager 	import SearchPhraseManager
from lib.searchable_data_sources 	import SearchableDataSources
from lib.results_processor 			import ResultsProcessor
from lib.reports_generator 			import ReportsGenerator
from lib.reports_outputter 			import ReportsOutputter

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
		
		

	def set_env(self, env):
		self.env = env

	def set_app_memory_location(self, app_memory_location):
		self.app_memory_location = app_memory_location
		

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
		#
		# Perform the Searches and get the Search Results
		search_results = searchableDataSources.perform_searches(search_phrases)

		# Results Processor - Read through the array of search_results and create a single results object as a dictionary
		resultsProcessor 		= ResultsProcessor();
		resultsProcessor.set_env(self.env)
		resultsProcessor.set_app_memory_location(self.app_memory_location)
		#
		# Process the results into a python dictionary
		processed_search_results_object = resultsProcessor.process_search_results(search_results)

		# Read the Processed Search Results dictionary and generate 1 or more reports
		reportsGenerator 		= ReportsGenerator();
		reportsGenerator.set_env(self.env)
		reportsGenerator.set_app_memory_location(self.app_memory_location)
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
		print("PublicationUsageFinder: (report__text):                    " + str(report__text))
		
		print("")
		print("PublicationUsageFinder.run__DRAFT: Reached the End.")





# END OF FILE