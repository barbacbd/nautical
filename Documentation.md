# Documentation

The `pages` branch will always contain all documentation. When creating new information on master

- rebase `pages` with `master`.
- Remove all old documentation. If you have an `artifacts` file, you can clean it up with `AutoDocExtClean`. Otherwise remove
`rst_docs` and `docs`.
- Run the `AutoDocExt` application again and readd the updated/new documents.
