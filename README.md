# Movie Scraper
This script scrapes the Multikino website and retrieves a list of movie titles that are currently playing in a specified city on a specified showing date.

### Usage
1. Set the CHROMEDRIVER_PATH variable to the path of your ChromeDriver executable.
2. Set the city variable to the name of the city where the cinema is located.
3. Set the showing_date variable to the date in format DD-MM-YYYY for which movie titles are to be retrieved.
4. Run the script.

The script will output a list of movie titles.

### Dependencies
- contextlib
- selenium
- beautifulsoup4

### Good programming practices
- The script defines constants at the top of the file and uses them throughout the script. This makes it easier to change the values in the future.
- The script defines a context manager for the ChromeDriver instance to ensure that the driver is properly closed after use.
- The script defines a function with a clear and concise docstring that explains its purpose, arguments, and return value.
- The script uses a try-except block to handle exceptions that may occur during scraping.
- The script prints a descriptive error message when an exception occurs.
- The script uses descriptive variable names to make the code easier to read and understand.

### Further development
This script can be further developed and integrated into the MovieMate backend project available at https://github.com/UserMarekDrag/MovieMate-backend. 
For example, the script can be modified to scrape other websites for movie titles, and the retrieved data can be stored in a database to be used by the MovieMate backend. 
Additionally, the script can be integrated into a cron job to regularly update the movie titles available on the website.