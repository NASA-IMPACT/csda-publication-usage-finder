# reports_generator.py
# print("reports_generator.py")


# # Early Documentation / Notes
# 	-Here we can generate raw reports (lists of data we have or are storing)
# 	-We should also be able to generate more complex outputs (slides, pdfs, customized, formatted lists (HTML, etc))

class ReportsGenerator():
	def __init__(self):
		print("ReportsGenerator: __init__");

		# Defaults for these are dev and local_filesystem
		self.env 					= "dev" 					# Possibile Choices are: "dev", "stage", "prod"
		self.app_memory_location 	= "local_filesystem" 		# Possibile Choices are: "local_filesystem", "cloud_s3"
		

	def set_env(self, env):
		self.env = env

	def set_app_memory_location(self, app_memory_location):
		self.app_memory_location = app_memory_location
	
	# Generate a simple text report
	def generate_report__simple_text(self, processed_search_results_object):
		report_text = ""

		# Create the report text in a logical way and read properties as we go through what needs to be in the report.
		report_text += "Search Results Report\n"
		report_text += "The number of search results found: " + str(processed_search_results_object['num_of_results']) + "\n"
		report_text += " - Put more info in the report here.\n"
		report_text += "END OF REPORT"

		# Return the report
		print("ReportsGenerator.generate_report__simple_text: Reached the End.")
		return report_text

	# Future: Generate Report Email
	# Future: Generate Report PDF and/or PowerPoint and/or Spreadsheet.  -- Depends on requirements and needs
