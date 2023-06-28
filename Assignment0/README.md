In that assignment, I read in some text files containing movie reviews and indexed them to perform boolean AND/OR queries.

The directory "data" had one file per review. Each file's name acted as the document ID, such as "Dog4.txt" having the Document ID Dog4. The file contained the review text.

The query operators were:

queried(term) -- where term is a string, returned a set of the IDs of all documents that contained it.
andQueried(arg1, arg2) -- where the arguments were either strings or sets of document IDs, returned a set of the IDs of the documents at the intersection of the two arguments.
orQueried(arg1, arg2) -- where the arguments were either strings or sets of document IDs, returned a set of the IDs of the documents at the union of the two arguments.
The definition of andQueried and orQueried was more complicated because they could be nested. For example, both of these needed to work:

orQueried('hello', 'world')
orQueried('hello', orQueried('world', 'earth'))
Here are three more examples (output below):

queried('movie')
andQueried('yellow', 'lab')
andQueried(andQueried('salome', orQueried('good', 'excellent')), 'opera')
The solution was implemented in two phases:

The indexing phase involved processing the documents in the directory and building the inverted index.
The query phase involved using the inverted index to compute the document IDs that satisfied a query.
