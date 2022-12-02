# Github Documentation Generation

The document provides instructions for generating the python documentation for the `Nautical` package.
The documentation can be found [here](https://barbacbd.github.io/nautical/build/html/index.html). 

# Location

The `pages` branch will always contain all of the [documentation](https://barbacbd.github.io/nautical/build/html/index.html).
As new code is added to the repository (on `master`), the `pages` branch must be rebased off of `master` and the
documents should be regenerated based on the new source.

# Process

The following should be executed from the base of the project:

```bash
wget https://raw.githubusercontent.com/barbacbd/auto_doc/master/auto_doc.sh;
chmod 777 auto_doc.sh;
./auto_doc.sh
```
