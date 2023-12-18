# search_phrases_manager.py
# print("search_phrases_manager.py")



# # Early Documentation / Notes
# 	-We have a list of search terms - At first, this may only be a single sentence or single phrase
#	-This should also be wrapped in a class which lets us store things like, when this term was added, an id that results and reports can link back to, etc)

class SearchPhraseManager():
	def __init__(self):
		print("SearchPhraseManager: __init__");

		self.search_phrases = []

		# Defaults for these are dev and local_filesystem
		self.env 					= "dev" 					# Possibile Choices are: "dev", "stage", "prod"
		self.app_memory_location 	= "local_filesystem" 		# Possibile Choices are: "local_filesystem", "cloud_s3"

		pass

	def set_env(self, env):
		self.env = env

	def set_app_memory_location(self, app_memory_location):
		self.app_memory_location = app_memory_location

	def add_new_search_phrase(self, new_search_phrase):
		self.search_phrases.append(new_search_phrase)

	def get_search_phrases(self):
		return self.search_phrases

	def load_search_phrases(self):
		# We need to know the environment - for local, we load them from a local file, for cloud, we load them from an S3 bucket
		pass

	def save_search_phrases(self):
		# We need to know the environment - for local, we save them to a local file, for cloud, we save them to an S3 bucket
		pass

	# TODO - Functions which store the Search Phrases (or maybe we make a single class for managing the input and output of data?)