# SI 507 F17 - Final Project - Analysis of Campus-around Restaurants

### Intro ###
This project aims to make an analysis of restaurants around(i.e. within 2km) 5 different colleges on ratings, services, categories and prices. 

### How to run the code ###
First of all, please go to the file(config_example.py), and set your own "db_name"(database name, like "SI507_final_pj"), "db_user"(username, like "postgres") and "db_password"(password for your database). And then save it.

Secondly, please go to https://www.yelp.com/developers/documentation/v3/authentication, click the "Create App" on your right to create your own app, and get your "client id" and "client secret". Then go back to the file(yelp_credentials.py) to fill in the corresponding variables there.
If the way above doesn't work, please copy the file(yelp_credentials) which has been submitted to canvas to the current directory.

Thirdly, pip install -r requirements.txt

The main function is in the file(SI507F17_finalproject.py). To run the whole program, you are supposed to give an input command after the filename in the command line. Firstly, by "python SI507F17_finalproject.py setup", you can build up a database consisting of 4 different tables. And then by "python SI507F17_finalproject.py view", two new windows will be opened in your browser, and the processed data will be visualized by bar charts and pie charts.

To run testsuite, simply type "python SI507F17_finalproject_tests.py" in the command line.

Finally, the expected output figures can be seen by openning 2 html files, "BarChart.html" and "Pie_Chart.html" in a browser.

### Structure(Object-oriented Programming) ###
* **Cache_Class.py:** definition of class Cache. Partial codes from lectures have been bowrrowed here. Two main methods are get_from_cache() and set_in_cache(). The corresponding functionality are obvious from the name of the functions.

* **Session_Class.py:** definition of class Session. This is responsible for creating a new session using OAuth2 with 2 main methods get_new_token() and get_data_from_api(). In addition to the class definition, there are 2 other functions defined in this file. create_request_identifier() is for creating a unique identifier for caching. make_requests() is an important function for requesting and returning data from API. It takes two input arguments, one is the endpoint url and the other is the parameters dict of a request.

* **Classes_for_Data.py:** definition of 2 different classes Restaurant and School. These 2 classes are responsible for transporting each data record got from API to the database. Their member variables and functions are defined based on the needs of database. It is similar to project 3, where the NationalSite class is used to transport the scraped data to a csv file.

* **Database_Class.py:** definition of class Database. This class is for dealing with the whole process of building a database and input query. In the building process, setup_db() is for creating 4 tables needed including Restaurants(id, yelp_id, name, school_id, rating, distance, price), Schools(id, name, city, state), Transactions(id, restaurant_id, transaction) and Categories(id, restaurant_id, category). Besides, insert_One_Request() is an important function that takes in the data from each API request and inserts it into database. After that, other methods are for analyzing on built database, each has one or two SQL queries inside.

* **Drawing_Class.py:** definition of class Visual. This is for creating kinds of charts based on the data got from methods of Database class. The library plotly is used here.

* **SI507F17_finalproject.py:** main function lies here. See the above part "How to run the code" for more details.

* **SI507F17_finalproject_tests.py:** definition of a comlete testsuite. It has one test class for each module class mentioned above except "Visual" in "Drawing_Class.py". Note that for testing the Database Class, a data file(test_db.json) is used.

### Conclusion ###
In conclusion, among a list of colleges(i.e. ['umich', 'ucla', 'mit', 'columbia university', 'UT Austin']), "MIT" has the best quality of eating due to the highest average ratings and highest percentage of good restaurants. Besides, "American(New)", "Breakfast & Brunch" and "Italian" are top 3 popular categories of restaurants. And only 38.3% of hot restaurants has additional services such as delivery and reservation, this might be because those services may not be so important to restaurants close to campus. And for the prices, level of "$$" takes up the majority, since college students may not be rich.
