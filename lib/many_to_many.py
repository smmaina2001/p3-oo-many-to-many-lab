# many_to_many.py
from datetime import datetime

class Author:
    all = []
    
    def __init__(self, name):
        if not isinstance(name, str):
            raise Exception("Name must be a string")
        self.name = name
        self.contracts_list = []
        Author.all.append(self)

    def add_contract(self, contract):
        if not isinstance(contract, Contract):
            raise Exception("Contract must be an instance of Contract")
        self.contracts_list.append(contract)

    def contracts(self):
        return self.contracts_list

    def books(self):
        return [contract.book for contract in self.contracts_list]

    def sign_contract(self, book, date, royalties):
        contract = Contract(self, book, date, royalties)
        self.add_contract(contract)
        return contract

    def total_royalties(self):
        return sum([contract.royalties for contract in self.contracts_list])

class Book:
    all = []
    
    def __init__(self, title):
        if not isinstance(title, str):
            raise Exception("Title must be a string")
        self.title = title
        self.contracts_list = []
        Book.all.append(self)

    def add_contract(self, contract):
        if not isinstance(contract, Contract):
            raise Exception("Contract must be an instance of Contract")
        self.contracts_list.append(contract)

    def contracts(self):
        return self.contracts_list

    def authors(self):
        return [contract.author for contract in self.contracts_list]

class Contract:
    all = []
    
    def __init__(self, author, book, date, royalties):
        if not isinstance(author, Author):
            raise Exception("Author must be an instance of Author")
        if not isinstance(book, Book):
            raise Exception("Book must be an instance of Book")
        if not isinstance(date, str):
            raise Exception("Date must be a string")
        if not isinstance(royalties, int):
            raise Exception("Royalties must be an integer")
        
        self.author = author
        self.book = book
        self.date = date
        self.royalties = royalties

        Contract.all.append(self)
        book.add_contract(self)
        author.add_contract(self)

    @classmethod
    def contracts_by_date(cls, date=None):
        if date:
            # Filter contracts by the provided date
            contracts_by_date = [contract for contract in cls.all if contract.date == date]
        else:
            # Sort contracts by date if no specific date is passed
            contracts_by_date = cls.all
        
        return sorted(contracts_by_date, key=lambda contract: datetime.strptime(contract.date, "%d/%m/%Y"))

# Testing Code
import pytest

def test_contract_contracts_by_date():
    """Test Contract class has method contracts_by_date() that sorts all contracts by date"""
    Contract.all = []
    author1 = Author("Name 1")
    book1 = Book("Title 1")
    book2 = Book("Title 2")
    book3 = Book("Title 3")
    author2 = Author("Name 2")
    book4 = Book("Title 4")
    
    contract1 = Contract(author1, book1, "02/01/2001", 10)
    contract2 = Contract(author1, book2, "01/01/2001", 20)
    contract3 = Contract(author1, book3, "03/01/2001", 30)
    contract4 = Contract(author2, book4, "01/01/2001", 40)

    # Test filtering by date
    assert Contract.contracts_by_date('01/01/2001') == [contract2, contract4]
    
    # Test sorting all contracts by date
    assert Contract.contracts_by_date() == [contract2, contract1, contract3, contract4]
