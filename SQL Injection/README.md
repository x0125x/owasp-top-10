SQL Injection is unarguably one of the most common types of injections.

The program is a simple login mechanism implemented in an incorrect way to demonstrate how easily the unwanted unauthorised access can be obtained.

To try it for yourself, try to use:
' OR '1'='1
as your login credentials.

With this method of accessing the database:
"SELECT * FROM user WHERE username='" + username + "' AND password='" + password + "'" ,
any provided input can result in modifying the inquiry. This can be dangerous, especially when modifying the inquiry to "A or B" statement, of which only one part has to return True.

Notice that when using the ' OR '1'='1 as your login and password, you gain the access even without such user being previously added to the database. That is because as soon as the statement passes one 'True' (like 1=1), the further validation is skipped and data is pulled out from the database. No further validation, to check whether the credentials provided by the user and those existing in the database are identical, is implemented in the code.

To eliminate the vulnerability, the line should be replaced by:
"SELECT * FROM user WHERE username=? AND password=?", (username, password) ,
which compares the values without the potential risk of inquiry modifications through the usage of ' or " characters.

Important: the code does not check data provided by user during the registration process (that is for instance not allowing for using certain characters) as its purpose is only to demonstrate the great risk resulting from this common implementation.
