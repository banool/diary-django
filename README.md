# Django Diary
This is an exact replica of the diary from my ftp webspace using Django. The link format is the same, the markdown is rendered into HTML in the exact same way, and the index looks exactly the same.

## To do
- Tests, my previous diary was sorely lacking this.
    - Make sure that the HTML renders properly.
    - Make sure that the secret tags are respected (**important**).
    - More Django'y tests.
- Put the old diary and the new diary together. This will remove the need for symlinks into the other diary and hopefully reduce the cruft around having a hardcoded absolute path to the entry directory.
- Productionise the code.
- Consider password protecting some / all of the diary.
- Consider where to store the entries and how to let Django know of their location. Where is the best place to store this piece of config information? What about in production? 