# Notes for the exam about the Search Engine

## Session 2 - Crawling

Currently the crawler doesn't have any content filtering. That is, the crawler
will look for any href tags it can find and then add that to the frontier. Due
to this, the crawler will find much more stuff but potentially it could find
links to stuff that shouldn't or cant be opened by the crawler. This leads to
the next problem. There is no error handling. So if the crawler encounters any
problems during its journey it has no way of handling this, and it would crash.

Also, efficiency wise, the crawler doesnt save any of its found pages locally in
storage. So next time the crawler is ran, it will check the same sites again.
This could be tweaked to save it to a CSV or JSON file, and have that file
passed when the crawler is started first to make sure we don't visit any of
these first unless its the seed url. And then load the CSV / JSON into the
`self.visited` set.

In terms of the crawling for relative links. Those where not accounted for, so
the crawler will in its current state (12/10/2024) also visit these, which will
inevitably course some troubles with duplicates.

## Session 3 - Indexing

In the previous session the crawling method was implemented which simply would
fetch the URL's and then check the html from the url for other urls and then
keep going.

For this part, the indexer was implemented which simultaniously also checks the
near duplicates. This near duplicates function is VERY slow. and can sometimes
take up for 12 seconds in my PC (Lenovo Yoga Slim 7 Pro with 16GB RAM and a
Ryzen 5600H).

Not much processing or normalization where performed on the terms in the content
of the pages. That is, it could be improved my using a Stemmer like
PorterStemmer to get the words down to their base, this would also make the
crawling more efficient.

## Session 4 - Ranking

Ranking was done by using the LNC-LTC method and works great. It was tested on
the example document from the slides during the lecture and yielded the same
results

## Session 5 - Ranking (link-based)
