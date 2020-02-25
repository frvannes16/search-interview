# Location Search

We are deploying a new web page, `index.html`, that contains a simple search bar. When a user types into the search bar, after waiting one second, the page makes a request to `http://localhost:5000/businesses?search={SearchVal}`. The web page expects to recieve a list of Business results that match the search. These results are then displayed on the web page.

The web page will be user facing and is expected to recieve lots of traffic.

Your task is to build the backend for this search tool.

## Provided Files

`index.html`		The webpage with the search interface.
`search.js`		Javascript employed by `index.html`.
`generate_locations.py`	A program with a command line interface for generating locations. Do not modify this file unless asked.
`requirements.txt`	The pip packages used to run generate_locations.py
`brief.md`		This file.

