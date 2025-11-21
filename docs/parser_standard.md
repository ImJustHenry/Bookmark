# Parser standard

A parser must have the functions with the following signatures:

```{python}
    parse(int isbn) -> Book
    get_test_isbn() -> int
```

parse function should raise a BookError exception if the book is not found.

get_test_isbn function should output an isbn that exists on the target site.

Note that not all parameters of the Book object are required to be filled for the input.
