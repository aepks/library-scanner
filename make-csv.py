import argparse
import requests
import csv
import json

GOOGLE_API_KEY = ''

def dump_response(r):
	print(json.dumps(r.json(), indent=2, sort_keys=True))

def matches_isbn(isbn, volumeInfo):
	if 'industryIdentifiers' not in volumeInfo:
		print("     no identifiers for {}".format(isbn))
		return False
	for identifier in volumeInfo['industryIdentifiers']:
		try:
			if int(identifier['identifier']) == isbn:
				return True
			# print("id {} != isbn {}".format(identifier['identifier'], isbn))
		except ValueError as e:
			pass # ignore non-numeric ISBNs, since our scanner doesn't generate them anyway
			# print("Found a non-numeric identifier: {}".format(identifier['identifier']))
	return False



parser = argparse.ArgumentParser(description="Turn a list of ISBNs into a CSV")
parser.add_argument("isbns", help="A file with an ISBN on each line", type=argparse.FileType('r'))
parser.add_argument("output", help="A CSV file with the book details", type=argparse.FileType('w'), default='-')
args = parser.parse_args()

writer = csv.DictWriter(args.output,
	fieldnames=['Google Books ID', 'ISBN', 'Last Name', 'First Author', 'Title', 'Comment'],
	restval="")
writer.writeheader()

comment = ""

for isbn in args.isbns:
	isbn = isbn.strip("\n")
	try:
		isbn = int(isbn)
	except ValueError:
		print("Found comment: {}".format(isbn))
		comment = isbn
		continue


	print("Searching for {}".format(isbn))
	r = requests.get(
		'https://www.googleapis.com/books/v1/volumes', params={
			'q': 'isbn:{}'.format(isbn),
			'fields': 'items/volumeInfo/authors,items/volumeInfo/title,items/volumeInfo/industryIdentifiers,items/id',
			'maxResults': 1,
			'key': GOOGLE_API_KEY
			})
	if r.status_code == 403:
		print("Oop, we might be rate-limited. Stopping. Response:")
		dump_response(r)
		exit()
	if r.status_code != 200:
		print("Uh-oh, got a non-200 return. Continuing to the next one. Response:")
		dump_response(r)
		continue

	try:
		book = r.json()['items'][0]
	except KeyError as e:
		print("No results for {}!".format(isbn))
		dump_response(r)
		writer.writerow({
			'ISBN': isbn,
			'Comment': comment
			})
		continue

	try:
		if not matches_isbn(isbn, book['volumeInfo']):
			print("Matching ISBN not found for {}!".format(isbn))
			writer.writerow({
				'ISBN': isbn,
				'Comment': comment
			})
			dump_response(r)
			continue
		if 'subtitle' in book['volumeInfo']:
			title = "{title}: {subtitle}".format(**book['volumeInfo'])
		else:
			title = book['volumeInfo']['title']
		writer.writerow({
			'Title': title,
			'First Author': book['volumeInfo'].get('authors', [""])[0], # some books don't have authors listed :(
			'Last Name': book['volumeInfo'].get('authors', [""])[0].split(" ")[-1], # doesn't take into account multi-word last names
			'ISBN': isbn,
			'Google Books ID': book['id'],
			'Comment': comment
			})
	except KeyError as e:
		print("Couldn't find field {} in results for {}!".format(e, isbn))
		print(json.dumps(book, indent=4, sort_keys=True))
