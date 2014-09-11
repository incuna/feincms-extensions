# feincms-extensions [![Build Status](https://travis-ci.org/incuna/feincms-extensions.png?branch=master)](https://travis-ci.org/incuna/feincms-extensions)

Extensions for FeinCMS.

## Prepared date

Add a prepared date value to the FeinCMS `page.Page` model.
If the page has no value set then the value is taken from nearest ancestor
page (based on `_cached_url` path) that has a value.


## Render regions

Render the feincms regions into a dictionary.
