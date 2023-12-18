#reports_outputter.py
# print("reports_outputter.py")

# # Early Documentation / Notes
# 	-This module is where the report is sent to someone or some entity that is interested in it.
# 	-Here is where we have code that could do the following
# 	-Send an email, send to slack, save to a static S3 html page, etc

class ReportsOutputter():
	def __init__(self):
		print("ReportsOutputter: __init__");

		# Defaults for these are dev and local_filesystem
		self.env 					= "dev" 					# Possibile Choices are: "dev", "stage", "prod"
		self.app_memory_location 	= "local_filesystem" 		# Possibile Choices are: "local_filesystem", "cloud_s3"

	def set_env(self, env):
		self.env = env

	def set_app_memory_location(self, app_memory_location):
		self.app_memory_location = app_memory_location

	def output_report__DRAFT(self, report_text):
		print("ReportsOutputter.output_report__DRAFT: This is a placeholder for actually outputing the report. ")
		print("  In the future, this function might send an email, or send something to slack, or publish to a public S3 webpage, etc")
		print("  Right now here is the text that was passed in: " + str(report_text))