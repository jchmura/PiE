from datetime import datetime
from xml.etree import ElementTree
import sys
from collections import namedtuple

import re

DATE_FORMAT = '%Y-%m-%d'

Book = namedtuple('Book', ['id', 'author', 'title', 'genre', 'price', 'publish_date', 'description'])


def main():
    filename = get_filename(sys.argv)
    tree = ElementTree.parse(filename)
    books = create_books(tree.getroot())

    for book in books:
        print(book)


def create_books(root):
    books = []

    for book_tag in root:
        try:
            attributes = {'id': book_tag.attrib['id']}
            for attribute in book_tag:
                attributes[attribute.tag] = attribute.text

            convert_attributes(attributes)

            book = Book(**attributes)
            books.append(book)
        except (KeyError, TypeError) as e:
            print(e, file=sys.stderr)

    return books


def convert_attributes(attributes):
    attributes['publish_date'] = datetime.strptime(attributes['publish_date'], DATE_FORMAT)

    # replace new lines with spaces with single space
    attributes['description'] = re.sub(r'[ \n]+', ' ', attributes['description'])


def get_filename(args):
    if len(args) != 2:
        print('You need to specify the xml file as sole argument')
        sys.exit(1)
    return args[1]


if __name__ == '__main__':
    main()
