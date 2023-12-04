# app.py
# print("app.py")

# Imports
from lib.publication_usage_finder import PublicationUsageFinder


# Console Entry Point
# Usage: python app.py
if __name__ == '__main__':
    # Create an instance of the PublicationUsageFinder
	pubUsageFinder = PublicationUsageFinder();

	# Run the Publication Usage Finder
	#pubUsageFinder.run__from_airflow()
	#pubUsageFinder.run__from_local_dev_terminal()
	#pubUsageFinder.run__DRAFT()

	# Call the Draft without any params to use the defaults
	#pubUsageFinder.run__DRAFT()

	# Or set the Env and App Memory Location in the function call.
	# run__DRAFT(self, current__env="dev", current__app_memory_location="local_filesystem")
	pubUsageFinder.run__DRAFT("dev", "local_filesystem")
	
# END OF FILE