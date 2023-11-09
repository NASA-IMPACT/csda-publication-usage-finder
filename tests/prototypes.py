# Some early prototype tests 


# Imports are with their respective functions.



# Use Selenium to do a simple search and output the result URLs
#
# Using Selenium might be a bust - Already running into configuration problems.
# Also, after researching a bit, it looks like Google Scholar would block this sort of usage
def prototype_test_01__simple_g_scholar_search():
	print("prototype_test_01__simple_g_scholar_search:  Started")

	# IMPORTS
	from selenium import webdriver
	from selenium.webdriver.common.keys 	import Keys
	from selenium.webdriver.common.by 		import By
	from selenium.webdriver.common.service 	import Service
	from webdriver_manager.chrome 			import ChromeDriverManager


	# Setup the Selenium WebDriver
	service = Service(ChromeDriverManager().install())
	driver = webdriver.Chrome(service=service)

	# Navigate to Google Scholar
	driver.get("https://scholar.google.com/")

	# Locate the search input, enter the search term and submit
	search_input = driver.find_element(By.NAME, "q")
	search_term = "This work utilized data made available through the NASA Commercial Smallsat Data Acquisition (CSDA) Program"
	search_input.send_keys(search_term)
	search_input.send_keys(Keys.RETURN)

	# Wait for search results to load
	driver.implicity_wait(5) # 5 seconds

	# Collect all search result links 
	search_results = driver.find_elements(By.CSS_SELECTOR, 'h3.gs_rt a')
	urls = [result.get_attribute('href') for result in search_results]

	url_counter = 0
	for url in urls:
		print(str(url_counter) + ": URL: " + str(url))
		url_counter = url_counter + 1

	driver.quit() 

	print("prototype_test_01__simple_g_scholar_search:  Reached the End")


# API based Search of Google Scholars using `scholarly` (https://github.com/scholarly-python-package/scholarly)
def prototype_test_02__basic_use_of_scholarly_api_for_g_scholar_search():
	print("prototype_test_02__basic_use_of_scholarly_api_for_g_scholar_search:  Started")
	
	print("prototype_test_02__basic_use_of_scholarly_api_for_g_scholar_search:  Reached the End")


#prototype_test_01__simple_g_scholar_search()
prototype_test_02__basic_use_of_scholarly_api_for_g_scholar_search()
