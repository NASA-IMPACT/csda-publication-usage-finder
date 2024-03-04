# reports_generator.py
# print("reports_generator.py")

# Abstraction for storing the search results
from lib.storage import Storage

# # Early Documentation / Notes
# 	-Here we can generate raw reports (lists of data we have or are storing)
# 	-We should also be able to generate more complex outputs (slides, pdfs, customized, formatted lists (HTML, etc))

class ReportsGenerator():
	def __init__(self):
		print("ReportsGenerator: __init__");

		# Defaults for these are dev and local_filesystem
		self.env 					= "dev" 					# Possibile Choices are: "dev", "stage", "prod"
		self.app_memory_location 	= "local_filesystem" 		# Possibile Choices are: "local_filesystem", "cloud_s3"
		self.run_id 				= "unset" 					# The run_id should be set just after instanciating this object.
		
		# Settings for where the search results are saved and loaded
		self.reports_generator_dir_path 		= "pub_finder_runs/reports_generator"
		self.reports_generator_file_name_latest = "latest.txt"
		

	def set_env(self, env):
		self.env = env

	def set_app_memory_location(self, app_memory_location):
		self.app_memory_location = app_memory_location

	def set_run_id(self, run_id):
		self.run_id = run_id

	# Save Over the 'latest.txt' report generator output string and save a txt file which contains the run_id as the base part of the filename
	def save__generated_report_text(self, string_to_save):
		# Convert the search_results_list into an object, add the results as a property of that object, also add the run_id to the object
		
		
		# Instancate the storage class and pass on the app memory location variable to it (so it knows if we are working with local or cloud version)
		storage_instance = Storage()
		storage_instance.set_app_memory_location(app_memory_location=self.app_memory_location)
		
		# Call the Function to save the latest search results
		storage_instance.save_string_to_file(string_to_save=string_to_save, directory_path=self.reports_generator_dir_path, file_name=self.reports_generator_file_name_latest) # latest.txt

		# Create the filename for the current run_id and save that one as well.
		current_run_id__txt_file_name = str(self.run_id) + ".txt"
		storage_instance.save_string_to_file(string_to_save=string_to_save, directory_path=self.reports_generator_dir_path, file_name=current_run_id__txt_file_name) # <yyyy_mm_dd__hh_mm_ss>.txt


	
	# Generate a simple text report
	def generate_report__simple_text(self, processed_search_results_object):
		report_text = ""


		# TODO - Also pull in info about older results and integrate them in the report here.

		# Iterate the `processed_search_results_object` list and create a presentable report from that info
		search_results_to_present_in_report = processed_search_results_object['search_results_to_present_in_report']
		report_text__section__search_results = "\n"
		report_text__section__search_results += "    ------------------------------\n"
		for current_report_result in search_results_to_present_in_report:
			#report_text__section__search_results += "      TODO__REPLACE_THIS_LINE_WITH_INFO_FROM_current_report_result.\n"

			report_text__section__search_results += "\n"

			is_new_result = current_report_result['is_new_result']
			if(is_new_result == True):
				report_text__section__search_results += "      ***(NEW RESULT FOR THIS RUN)***\n"

			report_text__section__search_results += "      PubTitle:           "+str(current_report_result['pub_title'])+"\n"
			report_text__section__search_results += "      Year:               "+str(current_report_result['pub_year'])+"\n"
			report_text__section__search_results += "      Authors:            "+str(current_report_result['authors_list'])+"\n"
			report_text__section__search_results += "      URL:                "+str(current_report_result['pub_url'])+"\n"
			report_text__section__search_results += "      Datasource:         "+str(current_report_result['api_source'])+"\n"
			report_text__section__search_results += "      Search String:      (TODO__Finish_hooking_this_up)\n"
			report_text__section__search_results += "      Search Result Date: "+str(current_report_result['run_id'])+"\n" 		# TODO - Convert this to an actual date time and then present it as a better string
			report_text__section__search_results += "\n"
			report_text__section__search_results += "    ------------------------------\n"

		#report_text__section__search_results += "    ------------------------------\n"
		report_text__section__search_results += "\n"

		# Note: This should be as easy as just pulling in properties from objects that were loaded up / created by the 'results_processor'
		#
		# Report generator should process the run_id back into a date time and have a line that says,
		# # "This result was most recently seen on "DATE STRING" (NEW_RESULT)"
		print("___TODO - generate_report__simple_text: SEE COMMENT ABOVE THIS LINE AND DO THOSE THINGS")

		# Create the report text in a logical way and read properties as we go through what needs to be in the report.
		report_text += "START OF REPORT\n"
		report_text += "\n"
		report_text += "Search Results Report\n"
		#report_text += "The number of search results found: " + str(processed_search_results_object['num_of_results']) + "\n"
		report_text += "The number of search results in the current search found:             " + str(processed_search_results_object['num_of_results__from_current_run_search']) + "\n"
		report_text += "The number of search results loaded from previously saved searches:   " + str(processed_search_results_object['num_of_results__from_previous_saved_searches']) + "\n"
		report_text += "The number of NEW search results found in this run:                   " + str(processed_search_results_object['num_of_new_results__from_current_run_search']) + "\n"
		report_text += "The total number of search results presented in this report:          " + str(processed_search_results_object['num_of_results__presented_in_report']) + "\n"
		report_text += "\n"
		report_text += "\n"
		report_text += "  Publications List\n"
		report_text += "\n"
		report_text += report_text__section__search_results
		report_text += "\n"
		report_text += "\n"
		report_text += "END OF REPORT\n"

		# Save the current Report
		self.save__generated_report_text(string_to_save=report_text)

		# Return the report
		print("ReportsGenerator.generate_report__simple_text: Reached the End.")
		return report_text

	# Future: Generate Report Email
	# Future: Generate Report PDF and/or PowerPoint and/or Spreadsheet.  -- Depends on requirements and needs


# Garbage
# TODO - Remove on next pass
# report_text += " - Put more info in the report here.\n"