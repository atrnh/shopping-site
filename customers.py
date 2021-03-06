"""Customers at Hackbright."""


class Customer(object):
    """Ubermelon customer."""

    def __init__(self,
                 first_name,
                 last_name,
                 email,
                 hashed_password
                 ):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.hashed_password = hashed_password

    def __repr__(self):
        """Convenience method to show information about melon in console."""

        return '<Customer: {} {}, {}>'.format(
            self.first_name, self.last_name, self.email
        )

    def is_hashed_password(self, password):
        """Check if 'password' is the correct password for this customer.

        Compares hashed 'password' against stored hash of original password.
        """

        return hash(password) == self.hashed_password


def read_customers_from_file(filepath):
    """Read customer data and populate dictionary of customers.

    Dictionary will be {email: Customer object}
    """

    customers = {}

    for line in open(filepath):
        (first_name,
         last_name,
         email,
         password) = line.strip().split('|')

        customers[email] = Customer(first_name,
                                    last_name,
                                    email,
                                    hash(password))

    return customers


def get_by_email(email):
    """Return a customer given an email"""

    # This relies on access to the global dictionary 'customers'
    return customers[email]


customers = read_customers_from_file('customers.txt')
