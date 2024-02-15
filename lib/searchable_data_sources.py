# searchable_data_sources.py
# print("searchable_data_sources.py")

# Imports
# Dir 'data_sources' has the datasources manipulated by this class.

# Imports used by Scholarly Section
from scholarly import scholarly
import json
import time

# For creating Unique IDs from strings
import hashlib
import base64


# # Early Documentation / Notes
# 	-We have a list of data sources (enumerated list of strings), each string points to a different class that actually does the searching work
#	-Each of these class instances may have their own logic, but should also conform to expected input/output standards.

class SearchableDataSources():
	def __init__(self):
		print("SearchableDataSources: __init__");

		# Defaults for these are dev and local_filesystem
		self.env 					= "dev" 					# Possibile Choices are: "dev", "stage", "prod"
		self.app_memory_location 	= "local_filesystem" 		# Possibile Choices are: "local_filesystem", "cloud_s3"
		self.run_id 				= "unset" 					# The run_id should be set just after instanciating this object.
		

	def set_env(self, env):
		self.env = env

	def set_app_memory_location(self, app_memory_location):
		self.app_memory_location = app_memory_location

	def set_run_id(self, run_id):
		self.run_id = run_id
	
	@staticmethod
	def create_search_result_object(input_param_1, input_param_2, other_params):
		search_result_object = {}
		search_result_object['prop_1'] = input_param_1
		search_result_object['prop_2'] = input_param_2
		search_result_object['prop_3'] = other_params
		return search_result_object


	# TODO - Connect multiple methods of searching inside of this function.
	# 
	# use_local_example_search_results_data is being defaulted to True so we don't accidently hit the data source too often during testing unless we explicitly intend to
	def perform_searches(self, search_phrases, use_local_example_search_results_data=True):
		#print("SearchableDataSources.perform_searches: TODO - Convert this so that it creates instances of child classes for each API we are searching and call them.")

		# An object to hold a standard dictionary for each search result
		search_results = []

		# (1) Call our method to get results.
		search_results__from__scholarly = []
		if(use_local_example_search_results_data == False):
			# Do an actual live search
			search_results__from__scholarly = self._scholarly__perform_search(search_phrase=search_phrases[0])
		else:
			# Do not do an actual search query, just use the locally stored example data
			search_results__from__scholarly = self._scholarly__get_real_example_search_results_data()

		# (2) Collate/transform the results into a standard way
		search_results = self._scholarly__transform_pub_search_results(search_results__from__scholarly)

		# (3) Return the results
		print("SearchableDataSources.perform_searches: Reached the End.")
		return search_results


		# # Initial Version, with examples if we were using subclassing
		# #
		# # An object to hold a standard dictionary for each search result
		# search_results = []
		# #
		# # (1) Try and Call Each of the search methods to get results.
		# #
		# # (2) Collate the results into a standard way
		# search_result_obj_1 = SearchableDataSources.create_search_result_object("Property_1a", "Property_2a", "Property_3a")
		# search_result_obj_2 = SearchableDataSources.create_search_result_object("Property_1b", "Property_2b", "Property_3b")
		# search_results.append(search_result_obj_1)
		# search_results.append(search_result_obj_2)
		# #
		# # Just some in context notes.
		# print("SearchableDataSources.perform_searches: TODO - We will likely need to store search results (and possibly publications as well) - so we can identify what was previously found vs what might be new.")
		# print("SearchableDataSources.perform_searches: TODO - Future Version may even anaylyze the content of the publications")
		# #
		# # (3) Return the results
		# print("SearchableDataSources.perform_searches: Reached the End.")
		# return search_results
		

	# For now, we only have a single datasource - which is using the Scholarly library.  Adding a set of functions here that will conform to what 'perform_searches()' expects
	
	# Generate a hash using the year, publication title and list of authors.
	@staticmethod
	def get_hash_for_pub_search_result(pub_search_result):
		# Defaults are used, incase this search result does not have a bib and/or sub prop
		pub_year = "9999"
		try:
			pub_year 			= str(pub_search_result['bib']['pub_year'])
		except:
			pub_year 			= "9999"

		pub_author_list = ['default', 'error']
		try:
			pub_author_list 	= pub_search_result['bib']['author']
		except:
			pub_author_list 	= ['default', 'error']

		# Converts ['A Name', 'B Person'] to 'A Name B Person'
		pub_authors 	=' '.join(pub_author_list)

		pub_title 		= "Default Pub Title"
		try:
			pub_title 		= str(pub_search_result['bib']['title'])
		except:
			pub_title 		= "Default Pub Title"

		# Combining all 3 strings together now.
		combined_input = str(pub_year) + str(pub_authors) + str(pub_title)

		# Generate a SHA-1 hash of combined_input
		hash_obj = hashlib.sha1(combined_input.encode())

		# Create the unique string
		hex_digest_str = hash_obj.hexdigest()

		# Return it
		return hex_digest_str

	# This function is used to get a unique id for any given pub_search_result
	# First, we simply check to see if there is a publication url value present, if so, that IS the id.  If not, then we generate a hash using the year, publication title and list of authors and then that has becomes the id.
	# This process should be deterministic - meaning we can count on getting the same id out given the same input.
	def get_or_generate_id_from_search_result(self, pub_search_result):
		pub_id = ""
		pub_url = ""
		try:
			pub_url = str(pub_search_result['pub_url'])
		except:
			pub_url = ""

		# If the pub_url is still blank at this point, then we need to use the hash as the id, if not, use the UR
		if(pub_url == ""):
			pub_hash = self.get_hash_for_pub_search_result(pub_search_result=pub_search_result)
			pub_id = pub_hash
		else:
			pub_id = pub_url

		# Return the pub_id
		return pub_id


	# Example showing Properties being added by searchable_data_sources (AND the existing properties)
	#
	# 	// Properties Added During SearchableDataSources._scholarly__transform_pub_search_results()
	# 	'pub_search_result_source': 'scholarly_google_scholars',
	# 	'pub_id': 	'https://ieeexplore.ieee.org/abstract/document/9554702/',
	# 	'pub_url': 	'https://ieeexplore.ieee.org/abstract/document/9554702/',
	# 	'pub_hash': '9cbf802077d5bfc5e8429a91930f6cee49f0ee11',
	# 	'run_id': 	'2024_02_14__00_30_32'
	#
	# 	'pub_search_result':
	# 		// (SearchableDataSources._scholarly__transform_pub_search_results() actually wraps the entire search result into property: 'pub_search_result')
	# 		// Scholarly ONLY
	# 		{
	# 			'container_type': 'Publication',
	# 			'source': "<PublicationSource.PUBLICATION_SEARCH_SNIPPET: 'PUBLICATION_SEARCH_SNIPPET'>",
	# 			'bib':
	# 			{
	# 				'title': 'Commercial Smallsat Data Acquisition Program: Airbus US Synthetic Aperture Radar Quality Assessment Summary',
	# 				'author': ['B Osmanoglu', 'M Jo'],
	# 				'pub_year': '2023',
	# 				'venue': 'NA',
	# 				'abstract': 'Trade names and trademarks are used in this report for identification  the Commercial  Smallsat Data Acquisition (CSDA) program\\’s radar subject matter experts, following the Joint NASA'
	# 			},
	# 			'filled': False,
	# 			'gsrank': 3,
	# 			'pub_url': 'https://ntrs.nasa.gov/citations/20230013207',
	# 			'author_id': ['', '9ZkFo54AAAAJ'],
	# 			'url_scholarbib': '/scholar?hl=en&q=info:Au3uhC6dBJAJ:scholar.google.com/&output=cite&scirp=2&hl=en',
	# 			'url_add_sclib': '/citations?hl=en&xsrf=&continue=/scholar%3Fq%3DThis%2Bwork%2Butilized%2Bdata%2Bmade%2Bavailable%2Bthrough%2Bthe%2BNASA%2BCommercial%2BSmallsat%2BData%2BAcquisition%2B(CSDA)%2BProgram%26hl%3Den%26as_sdt%3D0,33&citilm=1&update_op=library_add&info=Au3uhC6dBJAJ&ei=S7e6ZZGZJoSC6rQPspmXgAw&json=',
	# 			'num_citations': 0,
	# 			'eprint_url': 'https://ntrs.nasa.gov/api/citations/20230013207/downloads/NASA%20TP%2020230013207.pdf'
	# 		}
	# 	Note: Property: 'source' has been transformed to be a string (for easy json storage):  'source': "<PublicationSource.PUBLICATION_SEARCH_SNIPPET: 'PUBLICATION_SEARCH_SNIPPET'>",

	
	# When we have more than one data source, we may need to make a transformer function which transforms the results into a standard form (common fields with defaults set for any fields with missing data)
	#
	# // This function simply tags the grouped search results so we know which run_id they are part of and which api_source
	def _scholarly__transform_pub_search_results(self, search_results=[]):
		# Tag each result with a run_id, and api_source.  Also determine uniqueness for each publication
		transformed_search_results = []
		for search_result in search_results:

			# Get/generate variables that we will need later (pub_id)
			pub_hash 	= self.get_hash_for_pub_search_result(pub_search_result=search_result)
			pub_id 		= self.get_or_generate_id_from_search_result(pub_search_result=search_result)
			pub_url 	= str(search_result['pub_url'])

			# Load up the object
			transformed_search_result = {}
			transformed_search_result['pub_search_result_source'] 	= "scholarly_google_scholars"
			transformed_search_result['pub_search_result'] 			= search_result
			transformed_search_result['pub_id'] 					= pub_id
			transformed_search_result['pub_url'] 					= pub_url
			transformed_search_result['pub_hash'] 					= pub_hash
			transformed_search_result['run_id'] 					= self.run_id

			# Append this transformed search result to the list
			transformed_search_results.append(transformed_search_result)

		# Return the list of transformed search results
		return transformed_search_results

	# Performs the search from the input phrase.  (runs the scholarly search_pubs function and collects all the results)
	def _scholarly__perform_search(self, search_phrase=""):
		ret_search_results_obj_list = [] #{}

		# A setting for adding a slight delay between server requests.
		seconds_of_wait_time_between_page_requests = 0.08 # 0.08 means 80 ms

		# A flag to tell us if we should even try the search
		can_search = True

		# Validation - Do not perform the search if the search phrase was blank.
		if(search_phrase==""):
			can_search = False 
			print("searchable_data_sources._scholarly__perform_search(): Cannot perform search.  search_phrase was blank. ")

		# Proceed with the search
		if(can_search == True):
			
			# Making a publication search query, using the input search_phrase.
			#search_pubs_query = scholarly.search_pubs('This work utilized data made available through the NASA Commercial Smallsat Data Acquisition (CSDA) Program')
			search_pubs_query = scholarly.search_pubs(search_phrase)

			# Store the search results into an object list
			# Iterating the whole list once by going 'forever' with a while loop until we 'catch' the end of the data using an except.
			raw_scholarly_results = []
			result_counter = 0
			has_result = True
			while (has_result == True):
				try:
					#print(next(search_pubs_query))
					next_result = next(search_pubs_query)
					raw_scholarly_results.append(next_result)
					time.sleep(seconds_of_wait_time_between_page_requests) # (0.08)
				except:
					len__raw_scholarly_results = len(raw_scholarly_results)
					print("searchable_data_sources._scholarly__perform_search(): End of results.  (result_counter): " + str(result_counter) + ", (len__raw_scholarly_results): " + str(len__raw_scholarly_results))
					has_result = False
				result_counter = result_counter + 1

			# Save the list into the return object.
			ret_search_results_obj_list = raw_scholarly_results

		return ret_search_results_obj_list

	# This function will get a set of real example search results as JSON in a very simillar form that scholarly would return for a "search_pubs()"" function call.
	def _scholarly__get_real_example_search_results_data(self):
		# Here we have a couple real search results with limitted manual formatting from the search string "This work utilized data made available through the NASA Commercial Smallsat Data Acquisition (CSDA) Program"
		ret_search_results_obj_list = [ {'container_type': 'Publication', 'source': '<PublicationSource.PUBLICATION_SEARCH_SNIPPET: \'PUBLICATION_SEARCH_SNIPPET\'>', 'bib': {'title': 'Commercial Smallsat Data Acquisition Program: Airbus US Synthetic Aperture Radar Quality Assessment Summary', 'author': ['B Osmanoglu', 'M Jo'], 'pub_year': '2023', 'venue': 'NA', 'abstract': 'Trade names and trademarks are used in this report for identification  the Commercial  Smallsat Data Acquisition (CSDA) program\’s radar subject matter experts, following the Joint NASA'}, 'filled': False, 'gsrank': 3, 'pub_url': 'https://ntrs.nasa.gov/citations/20230013207', 'author_id': ['', '9ZkFo54AAAAJ'], 'url_scholarbib': '/scholar?hl=en&q=info:Au3uhC6dBJAJ:scholar.google.com/&output=cite&scirp=2&hl=en', 'url_add_sclib': '/citations?hl=en&xsrf=&continue=/scholar%3Fq%3DThis%2Bwork%2Butilized%2Bdata%2Bmade%2Bavailable%2Bthrough%2Bthe%2BNASA%2BCommercial%2BSmallsat%2BData%2BAcquisition%2B(CSDA)%2BProgram%26hl%3Den%26as_sdt%3D0,33&citilm=1&update_op=library_add&info=Au3uhC6dBJAJ&ei=S7e6ZZGZJoSC6rQPspmXgAw&json=', 'num_citations': 0, 'eprint_url': 'https://ntrs.nasa.gov/api/citations/20230013207/downloads/NASA%20TP%2020230013207.pdf'}, {'container_type': 'Publication', 'source': '<PublicationSource.PUBLICATION_SEARCH_SNIPPET: \'PUBLICATION_SEARCH_SNIPPET\'>', 'bib': {'title': 'Commercial Smallsat Data Acquisition Program On-ramp# 2 Airbus US Synthetic Aperture Radar (SAR) Evaluation Report', 'author': ['B Osmanoglu', 'J Nickeson', 'A Hall'], 'pub_year': '2023', 'venue': 'NA', 'abstract': 'Trade names and trademarks are used in this report for identification only. Their usage does   In this report, CSDA evaluates the usefulness of imagery and data provided by Airbus US'}, 'filled': False, 'gsrank': 4, 'pub_url': 'https://ntrs.nasa.gov/citations/20230013218', 'author_id': ['', '', ''], 'url_scholarbib': '/scholar?hl=en&q=info:c50Cz0VJRx0J:scholar.google.com/&output=cite&scirp=3&hl=en', 'url_add_sclib': '/citations?hl=en&xsrf=&continue=/scholar%3Fq%3DThis%2Bwork%2Butilized%2Bdata%2Bmade%2Bavailable%2Bthrough%2Bthe%2BNASA%2BCommercial%2BSmallsat%2BData%2BAcquisition%2B(CSDA)%2BProgram%26hl%3Den%26as_sdt%3D0,33&citilm=1&update_op=library_add&info=c50Cz0VJRx0J&ei=S7e6ZZGZJoSC6rQPspmXgAw&json=', 'num_citations': 0, 'eprint_url': 'https://ntrs.nasa.gov/api/citations/20230013218/downloads/NASA%20TP%2020230013218.pdf'}, {'container_type': 'Publication', 'source': '<PublicationSource.PUBLICATION_SEARCH_SNIPPET: \'PUBLICATION_SEARCH_SNIPPET\'>', 'bib': {'title': 'Combining NASA Earth Observations and Commercial Smallsat Data to Inform Localized Decision Making', 'author': ['L Tanh', 'M Pazmino', 'L Childs-Gleason', 'KW Ross'], 'pub_year': '2023', 'venue': 'AGU23', 'abstract': "the program's use of CSDA data and its integration with NASA Earth  work utilized data  made available through the NASA Commercial Smallsat Data Acquisition (CSDA) program"}, 'filled': False, 'gsrank': 5, 'pub_url': 'https://ntrs.nasa.gov/citations/20230017240', 'author_id': ['', '', '', ''], 'url_scholarbib': '/scholar?hl=en&q=info:i-FhZ5APDnkJ:scholar.google.com/&output=cite&scirp=4&hl=en', 'url_add_sclib': '/citations?hl=en&xsrf=&continue=/scholar%3Fq%3DThis%2Bwork%2Butilized%2Bdata%2Bmade%2Bavailable%2Bthrough%2Bthe%2BNASA%2BCommercial%2BSmallsat%2BData%2BAcquisition%2B(CSDA)%2BProgram%26hl%3Den%26as_sdt%3D0,33&citilm=1&update_op=library_add&info=i-FhZ5APDnkJ&ei=S7e6ZZGZJoSC6rQPspmXgAw&json=', 'num_citations': 0, 'eprint_url': 'https://ntrs.nasa.gov/api/citations/20230017240/downloads/2023AGU_Poster_Tanh_CSDA-FDv2.pdf'}, {'container_type': 'Publication', 'source': '<PublicationSource.PUBLICATION_SEARCH_SNIPPET: \'PUBLICATION_SEARCH_SNIPPET\'>', 'bib': {'title': 'Data in Action Story: Sharing and Exploring Earth Science Data', 'author': ['D Pham'], 'pub_year': '2023', 'venue': 'NA', 'abstract': 'used for good data storytelling practice. Specifically, they  from a NASA internship supported  by the CSDA Program in the  of the Commercial Smallsat Data Acquisition (CSDA) review'}, 'filled': False, 'gsrank': 6, 'pub_url': 'https://search.proquest.com/openview/01b1bc68667a942808662719e8ed570b/1?pq-origsite=gscholar&cbl=18750&diss=y', 'author_id': [''], 'url_scholarbib': '/scholar?hl=en&q=info:0n0uwFkMkFcJ:scholar.google.com/&output=cite&scirp=5&hl=en', 'url_add_sclib': '/citations?hl=en&xsrf=&continue=/scholar%3Fq%3DThis%2Bwork%2Butilized%2Bdata%2Bmade%2Bavailable%2Bthrough%2Bthe%2BNASA%2BCommercial%2BSmallsat%2BData%2BAcquisition%2B(CSDA)%2BProgram%26hl%3Den%26as_sdt%3D0,33&citilm=1&update_op=library_add&info=0n0uwFkMkFcJ&ei=S7e6ZZGZJoSC6rQPspmXgAw&json=', 'num_citations': 0, 'url_related_articles': '/scholar?q=related:0n0uwFkMkFcJ:scholar.google.com/&scioq=This+work+utilized+data+made+available+through+the+NASA+Commercial+Smallsat+Data+Acquisition+(CSDA)+Program&hl=en&as_sdt=0,33', 'eprint_url': 'https://louis.uah.edu/cgi/viewcontent.cgi?article=1451&context=uah-theses'}, {'container_type': 'Publication', 'source': '<PublicationSource.PUBLICATION_SEARCH_SNIPPET: \'PUBLICATION_SEARCH_SNIPPET\'>', 'bib': {'title': 'Commercial Smallsat Data Acquisition: Program Update', 'author': ['M Maskey', 'A Hall', 'K Murphy', 'C Tucker'], 'pub_year': '2021', 'venue': '… and Remote Sensing …', 'abstract': 'CSDA will utilize Cumulus to publish data from commercial sources such that the data are  available next to the NASA’s  CSDA program has enabled access to commercial data allowing'}, 'filled': False, 'gsrank': 7, 'pub_url': 'https://ieeexplore.ieee.org/abstract/document/9554702/', 'author_id': ['k4T40hoAAAAJ', '', '', 'IBvX950AAAAJ'], 'url_scholarbib': '/scholar?hl=en&q=info:T3p8qChMC6IJ:scholar.google.com/&output=cite&scirp=6&hl=en', 'url_add_sclib': '/citations?hl=en&xsrf=&continue=/scholar%3Fq%3DThis%2Bwork%2Butilized%2Bdata%2Bmade%2Bavailable%2Bthrough%2Bthe%2BNASA%2BCommercial%2BSmallsat%2BData%2BAcquisition%2B(CSDA)%2BProgram%26hl%3Den%26as_sdt%3D0,33&citilm=1&update_op=library_add&info=T3p8qChMC6IJ&ei=S7e6ZZGZJoSC6rQPspmXgAw&json=', 'num_citations': 2, 'citedby_url': '/scholar?cites=11676510196397275727&as_sdt=5,33&sciodt=0,33&hl=en', 'url_related_articles': '/scholar?q=related:T3p8qChMC6IJ:scholar.google.com/&scioq=This+work+utilized+data+made+available+through+the+NASA+Commercial+Smallsat+Data+Acquisition+(CSDA)+Program&hl=en&as_sdt=0,33', 'eprint_url': 'https://ieeexplore.ieee.org/iel7/9553015/9553016/09554702.pdf'} ]
		return ret_search_results_obj_list



