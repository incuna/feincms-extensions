# feincms-extensions [![Build Status](https://travis-ci.org/incuna/feincms-extensions.png?branch=master)](https://travis-ci.org/incuna/feincms-extensions)

Extensions for FeinCMS.

## Prepared date

Add a prepared date value to the FeinCMS `page.Page` model.
If the page has no value set then the value is taken from nearest ancestor
page (based on `_cached_url` path) that has a value.


## Render regions

Render the feincms regions into a dictionary.


## Page Menu Navigation (template)

Render the page navigation. To enable the `feincms_extensions/navigation.html`
template in this project add feincms_extensions` to `INSTALLED_APPS`.

The template needs to be included in your template and it accepts two optional
parameters:

  - `nav_id` (default: `top-level`): css id to be used for the menu;
  - `depth` (default: 1): the depth of sub navigation to include.

### Usage

```python
{% include "feincms_extensions/navigation.html" with nav_id="new-id" depth=2 %}
```
