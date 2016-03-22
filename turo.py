import sys


# Establish attributes and methods for the db class
class SimpleDB(object):
    """A simple, in-memory database."""

    def __init__(self):
        """Initialize an instance of the SimpleDB class."""

        # Creates two dbs -- one for committed changes, and one for keeping track
            # of additions, edits, and deletions in a transaction
        self.real_db = {}
        self.working_db = {}

        # Creates two count_dicts -- one to track of value counts of all COMMITTED values,
            # and one to track of counts that have been added/edited/deleted in a transaction
        self.real_counts = {}
        self.working_counts = {}

        self.num_transactions = 1

    def begin(self):
        """Start a new transaction."""

        for name in self.working_db:
            self.working_db[name].append(self.working_db[name][-1])

        for value in self.working_counts:
            self.working_counts[value].append(self.working_counts[value][-1])

        self.num_transactions += 1

    def set(self, name, value):
        """Create a name in the working_db and set it equal to a value.

        For each pair, key = name of variable,
        value = list of the key's value in each transaction, will function as a stack

        Ex. {'a': ['NULL', 1, 2]."""

        if self.num_transactions > 1:
            # Look up name in working db, if it exists, set the value of the name in the
                # most recent transaction to the input value
            # Subtract the value count of the old value
            if name in self.working_db:
                old_value = self.working_db[name][-1]

                self.working_db[name][-1] = value

                # Look up old value in working counts, if not there, add to working counts from real counts
                # Subtract working count at the old value by 1
                if old_value not in self.working_counts and old_value in self.real_counts:
                    self.working_counts[old_value] = [self.real_counts[old_value] for x in range(self.num_transactions)]

                if old_value in self.working_counts:
                    self.working_counts[old_value][-1] -= 1

            # Look up name in real db, if it's there - create in working_db and specify
                # the old value in previous transactions
            # Subtract the value count of the old value from the working counts dict
            elif name in self.real_db:
                self.working_db[name] = [self.real_db[name] for x in range(self.num_transactions-1)]

                old_value = self.real_db[name]

                # Look up old value in working counts, if not there, add to working counts from real counts
                # Subtract working count at the old value by 1
                if old_value not in self.working_counts and old_value in self.real_counts:
                    self.working_counts[old_value] = [self.real_counts[old_value] for x in range(self.num_transactions)]

                if old_value in self.working_counts:
                    self.working_counts[old_value][-1] -= 1

                self.working_db[name].append(value)

            # If name doesn't exist in the real db or working db, add to the working db
                # and specify that the value was equal to NULL in previous transactions
            else:
                self.working_db[name] = ['NULL' for x in range(self.num_transactions-1)]
                self.working_db[name].append(value)

            # If value already in working counts, add one to the final value in the counts list
            if value not in self.working_counts and value in self.real_counts:
                self.working_counts[value] = [self.real_counts[value] for x in range(self.num_transactions)]

            if value in self.working_counts:
                self.working_counts[value][-1] += 1

            # If the value isn't in counts, create a key: value pair
                # Set all values to the list to 0 except the last one, which is one
            else:
                self.working_counts[value] = [0 for x in range(self.num_transactions-1)]
                self.working_counts[value].append(1)

        # If not in a transaction, set name: value pair and counts right away in realdb
        elif self.num_transactions == 1:
            self.real_db[name] = value
            self.real_counts[value] = self.real_counts.get(value, 0) + 1

    def get(self, name):
        """See if name exists in DB. If yes, get its value."""

        if name in self.working_db:
            print self.working_db[name][-1]

        elif name in self.real_db:
            print self.real_db[name]

        else:
            print 'NULL'

    def unset(self, name):
        """See if name exists in DB. If yes, set value equal to 'NULL"""

        if self.num_transactions > 1:
            # Add name to workingdb if not in there already
            if name not in self.working_db and name in self.real_db:
                self.working_db[name] = [self.real_db[name] for x in range(self.num_transactions)]

            # If old value is in working counts, decrease by 1
            # If old value is only in real counts, duplicate in working counts and decrease by 1
            # Set newest value equal to 'NULL' in working db
            if name in self.working_db:
                old_value = self.working_db[name][-1]

                if old_value not in self.working_counts and old_value in self.real_counts:
                    self.working_counts[old_value] = [self.real_counts[old_value] for x in range(self.num_transactions)]

                if old_value in self.working_counts:
                    self.working_counts[old_value][-1] -= 1

                self.working_db[name][-1] = 'NULL'

        # If not in a transaction, unset in realdb and realcounts right away
        elif self.num_transactions == 1:

            if name in self.real_db:
                old_value = self.real_db[name]

                self.real_db[name] == 'NULL'
                self.real_counts[old_value] -= 1

    def numequalto(self, value):
        """Given an integer input, return the number of names with a value equal to the input."""

        if value in self.working_counts:
            print self.working_counts[value][-1]

        elif value in self.real_counts:
            print self.real_counts[value]

        else:
            print 0

    def commit(self):
        """Commit changes to the db."""

        if self.num_transactions > 1:
            # Add/Replace the value of each name in the real DB with the most recent
                # value from the working db
            for name in self.working_db:
                    self.real_db[name] = self.working_db[name].pop()

            #Add/Replace the counts of each value in the real_counts with the most
                # recent value from working counts
            for value in self.working_counts:
                self.real_counts[value] = self.working_counts[value].pop()

            # Reset working_db, working counts, and number of transactions
            self.working_db = {}

            self.working_counts = {}

            self.num_transactions = 1

        else:
            print "NO TRANSACTION"

    def rollback(self):
        """Delete changes from the most recent transaction."""

        # Delete the last entries in workingdb and working counts
        # Decrease transaction count
        if self.num_transactions > 1:

            for name in self.working_db:
                self.working_db[name].pop()

            for value in self.working_counts:
                self.working_counts[value].pop()

            self.num_transactions -= 1
        else:
            print "NO TRANSACTION"

    def end(self):
        """End the db session."""

        sys.tracebacklimit = 0
        sys.exit()

################################################################################

# Create the db for the session
db = SimpleDB()

# Dictionary of Commands
commands_dict = {'SET': (lambda name, value: db.set(name, value)),
                 'GET': (lambda name: db.get(name)),
                 'UNSET': (lambda name: db.unset(name)),
                 'NUMEQUALTO': (lambda value: db.numequalto(str(value))),
                 'BEGIN': db.begin,
                 'COMMIT': db.commit,
                 'ROLLBACK': db.rollback,
                 'END': db.end}


# Allow user to imput commands
def lets_get_started():
    """Take command as raw_input, look up command in the commands dict,
        and run the corresponding function with the remaining raw_input as
        the function parameter(s)."""

    r = raw_input().split()

    command = r[0].upper()
    arg_list = r[1:]

    if command in commands_dict:
        return commands_dict[command](*arg_list)
    else:
        print "Not a valid command."


# Keep prompting for raw_input commands until user ends the session
while True:
    lets_get_started()
