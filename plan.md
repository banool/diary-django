1. Write a script that reads markdown into the database.
2. In the database, store the entries as Entry objects from the markdown.
3. Generate the html using `views.py` from this database-held markdown entry. Each time you go to generate the html check that the last-updated date of the entry in the database is newer than the markdown, otherwise reload the markdown into the database.

This isn't perfect, the entry in its markdown form is stored twice. Storing the generated html in the database seems inelegant too, so maybe the django db needs to be avoided entirely. Still, generating the HTML has the benefit of being able to use the templating system. I guess you could use it statically (generate html just once using the template for each entry) but this seems alright.