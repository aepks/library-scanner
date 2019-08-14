import argparse
import requests
import csv
import json

GOOGLE_API_KEY = ''

parser = argparse.ArgumentParser(description="Turn a list of ISBNs into a CSV")
parser.add_argument("isbns", help="A file with an ISBN on each line", type=argparse.FileType('r'))
parser.add_argument("output", help="A CSV file with the book details", type=argparse.FileType('w'), default='-')
args = parser.parse_args()

writer = csv.DictWriter(args.output,
	fieldnames=['Google Books ID', 'ISBN', 'Last Name', 'First Author', 'Title'],
	restval="")
writer.writeheader()

for isbn in args.isbns:
	isbn = isbn.strip("\n")
	print("Searching for {}".format(isbn))
	r = requests.get(
		'https://www.googleapis.com/books/v1/volumes', params={
			'q': 'isbn={}'.format(isbn),
			'key': GOOGLE_API_KEY
			})
	if r.status_code == 403:
		print("Oop, we might be rate-limited. Stopping. Response:")
		print(json.dumps(r.json(), indent=2, sort_keys=True))
		exit()
	if r.status_code != 200:
		print("Uh-oh, got a non-200 return. Continuing to the next one. Response:")
		print(json.dumps(r.json(), indent=2, sort_keys=True))
		continue
	try:
		book = r.json()['items'][0]
	except KeyError as e:
		print("No results for {}!".format(isbn))
		print(json.dumps(r.json(), indent=2, sort_keys=True))
		continue

	try:
		if 'subtitle' in book['volumeInfo']:
			title = "{title}: {subtitle}".format(**book['volumeInfo'])
		else:
			title = book['volumeInfo']['title']
		writer.writerow({
			'Title': title,
			'First Author': book['volumeInfo'].get('authors', [""])[0], # some books don't have authors listed :(
			'Last Name': book['volumeInfo'].get('authors', [""])[0].split(" ")[-1], # doesn't take into account multi-word last names
			'ISBN': int(isbn), # int() avoids quotes
			'Google Books ID': book['id']
			})
	except KeyError as e:
		print("Couldn't find field {} in results for {}!".format(e, isbn))
		print(json.dumps(book, indent=4, sort_keys=True))
