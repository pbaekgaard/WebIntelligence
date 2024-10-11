# Notes for the exam about the Search Engine

## Session 1 - Crawling

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

## Session 2 - Indexing

## Session 3 - Ranking

## Session 4 - Ranking (link-based)
