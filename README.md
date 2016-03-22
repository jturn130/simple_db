# Challenge to Build a Simple Database

## Instructions to Run Code:

To get started, run this file in interactive mode (python -i db.py).

## Thought Process Behind Code:

When I saw that the database challenge was about storing "names" and "values", it
sounded an awful lot like key: value pairs in Python dictionaries. Dictionaries
are a pretty awesome data structure since most common operations are O(1) time.

Once I decided that a dictionary was the best data structure for the project,
I realized that I would need multiple dictionaries to be successful. Dictionary #1
would be the real, actual database that stores all the committed name: value pairs.
Dictionary #2 would be a working database that stores ONLY the uncommitted pairs 
that have been added, edited, or deleted in order to keep memory costs low 
(typically only a few items are changed in a transaction, so the size of the
working database would be minor).

Because the challenge requires that the NUMEQUALTO command run in O(logn) time or
better, I decided to keep a pair of "real" and "working" dictionaries that keep
track of the number of times a certain value is stored in the dictionary. That way the
command will run in O(1) time. Similar to the previous dictionaries, the real 
dictionary stores all the values, and the working dictionary stores only the values
that have been changed in some way.

The next major challenge was to tackle the issue of transactions. A stack-like (LIFO)
structure seemed like the best call for this one--if you kept a list of transactions,
you could pop() off the last value on every rollback, or just keep the popped
value for the real database on every commit. Pop operations are also O(1) time. So, in the working
database and working counts dict, the key would be the variable name or value count,
and the value would be the stack of changes made to that key.

The final task at hand: how to get the user to interact with the functions and
structures I created. My solution: I created yet another dictionary, in which the
keys were commands, and the values lambda functions. The user would enter in a command
as raw input, which I would convert into a list. The first item of the list would be
matched to the appropriate key command in the dictionary, and the rest of the 
raw input would be passed as parameters to the lambda functions in the values.

And there you have it!

