To run the file clone the repository into a directory
I used python 3.8 so at least that version will need to be instaled.  The only external package I used was falsk so you will need to install that

pip install flask

then

cd to <clone_directory>/CategoryManager

invoke "python flask_routines.py"

In a browser got to localhost port 8000 http://127.0.0.1:8000/
The interface is very primitive (reasons later).  Enter an item by giving the category and label (both strings).  If successful the page will display the new state of the database.  To enter another you have to press the back button.  At any time you can display the state of the db on the page.

Notes
=====
I have to admit that I really struggled with this.  Not because of any technical difficulties but more trying to understand the scope of the test.
The instructions were for a full stack solution but it was clear that only a small amount of time was available so the solution needed to be very limited.  An added complcation for me was that I was primarily intereted in the back end whereas the test seemed more weighted to the front end.  So I decided to spend my two hours on the back end then add the front end afterwards.
For the back end I simply created a simple storage for the items arranged by category.  I then provided a few basic queries for manipulating the data.  There is a "row" per category with each row containing a list of items.  The data is volatile so only remains active as long as the process is running but I used class members so the process could create multiple instances using the same data.  There is a skeleton commit and a null load function to allow for persistence at a future time.  The requirement wasn't clear so I made category and label effectively a composite key (so it is possible to have items with the same label in different categories).  It would be trivial to make the label unique across categories.
I did allow room for some expansion but if the scope was extended any more then I would abandon this approach and use a real database instead.  I only tried to implement my own to give some functionality to the back end.
Having done the back end I then added the front-end almost as an afterthought.  I chose flask as the simplest method but I have only a very limited knowledge of flask from a brief scouringof the internet so the interface is a) very clunky - I couldn't work out how to get the return from the add to not overwrite the page - and b) only supports two of the back end functions.
There is a unit test file which can be run.
There are only a smallnumber of source files but initially I nonetheless separated them out into packages.  This gave me a few problems running from the command line.  This could be solved by adding directories to path, but I do not have access to a Linux account so was not 100% sure that would work there so put everything at the top level.

Extra features
==============

I did not have enough time to implement the extra features requested but here is how I would do them.  For multiple users it would be necessary to add an extra table to the "database" for the users.  Tere would be a login method which would update the users status in the table, and each of the other methods would pass in a user id and only be performed if the user had logged in.
For updating another user of a change the mechanism is there in the back end.  When the db is locked the token is assigned and when it is committed the token is incremented.  I amnot sure if this is possible but I would expect the front end to be polling using the read_token function and when it sees it change, perform a read_all (which should be changed to read from the persistent source) and update the page accordingly.
If the database was to be seriously implemented the commit would be passed the token and would only be performed if it matches the current token value.  The lock would have a timeout and would be released after a certain time, the change would be rolled back and the token incremented.
Adding extra features to an item is trivial in the back end as it is defined as an object so just need to add extra members to it which would be intialised.  It would make sense to introduce an update function where an item could be updated in the db without changing its label or category.  The fornt-nd would need to support the extra fields.  The creation of items should be factored out on the page (not necessary in my version as I only supported one operation, but if it were more then that would be required).

Summary
=======
If I were to do it again I would pay more attention to how the front end would work and create a proper interface first.  If I were developing a project in real life then the interface would be the first thing to be agreed.  As I said before I was trying to spend as much of the limited time available on the back end.  Even then it does not highlight much of my python knowledge.  Hopefully from these notes you can see how I thought that the code could be expanded at least and it is simple and easily maintainable.  Note also in a real project I would use docstrings rather than simple comments. 