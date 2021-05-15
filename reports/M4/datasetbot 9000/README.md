Instructions to use dataset collection bot
Just fill in your search query line by line in classes.txt file
Bot will create subfolders in "download" folder for each query

For increasing the limit of download, change the range of 'for loop' at line 64 (By default : 100 images)

# Webdriver should be installed as the same version as your chrome browser
# Requires Selenium Library : 
>> pip install selenium

# Use Image resize.py to change all file extension to .jpg and resize it to 100x100