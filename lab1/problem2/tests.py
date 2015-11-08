import unittest
from datetime import datetime
from xml.etree import ElementTree

import parser


class TestParser(unittest.TestCase):
    def test_convert_description(self):
        before = 'Lorem ipsum dolor sit amet, \n     consectetur adipiscing elit,\n     sed do eiusmod tempor\n   incididunt ut labore et dolore magna aliqua.'
        attributes = {
            'description': before,
            'price': '0',
            'publish_date': datetime.now().strftime(parser.DATE_FORMAT)
        }
        parser.convert_attributes(attributes)
        self.assertEqual(
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
            attributes['description'])

    def test_convert_date(self):
        attributes = {
            'description': '',
            'price': '0',
            'publish_date': '2015-04-03'
        }
        parser.convert_attributes(attributes)
        date = datetime(2015, 4, 3)
        self.assertEqual(date, attributes['publish_date'])

    def test_convert_price(self):
        attributes = {
            'description': '',
            'price': '6.28',
            'publish_date': datetime.now().strftime(parser.DATE_FORMAT)
        }
        parser.convert_attributes(attributes)
        self.assertEqual(6.28, attributes['price'])

    def test_single_book(self):
        xml = '''<?xml version="1.0"?>
<catalog>
    <book id="book101">
      <author>Chmura, Jakub</author>
      <title>This is a title</title>
      <genre>Adventure</genre>
      <price>3.14</price>
      <publish_date>2015-05-28</publish_date>
      <description>Lorem ipsum dolor sit amet,
      consectetur adipiscing elit</description>
   </book>
</catalog>
'''
        book = parser.Book(id='book101', author='Chmura, Jakub', title='This is a title', genre='Adventure',
                           price=3.14, publish_date=datetime(2015, 5, 28),
                           description='Lorem ipsum dolor sit amet, consectetur adipiscing elit')
        root = ElementTree.fromstring(xml)
        books = parser.create_books(root)
        self.assertEqual(1, len(books))
        self.assertEqual(book, books[0])

    def test_missing_attribute(self):
        xml = '''<?xml version="1.0"?>
<catalog>
    <book id="book101">
      <author>Chmura, Jakub</author>
      <title>This is a title</title>
      <genre>Adventure</genre>
      <publish_date>2015-05-28</publish_date>
      <description>Lorem ipsum dolor sit amet,
      consectetur adipiscing elit</description>
   </book>
</catalog>
'''
        root = ElementTree.fromstring(xml)
        books = parser.create_books(root)
        self.assertEqual(0, len(books))  # the book is not created


if __name__ == '__main__':
    unittest.main()
