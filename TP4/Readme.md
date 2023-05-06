
# Tokenizer

The goal of this homework is to tokenize a book into phrases, paragraphs, chapters.

## Page Breaks

First, we will try to deal with page breaks. Page breaks only make sense when the book is displayed in pages, since we want to process the text as one, they serve no purpose.
I'm considering multiple newlines in a row as a page break:

    (.*)\n\n+(.*)

This will be replace for only one newline between each group.


## Mark chapters

Chapters are a really common separator for main division within books.
They are hard to identify. If they have the reserved word indicating that it is a chapter Capítulo in Portuguese or Chapter in English.
These are related to the language of the book, so they are hard to generalize.
It's even harder, if the book was no reserved word.
Since, the book we are testing is portuguese, and has a reserved word for the chapters (Capítulo), the regex will deal with this case, but this will have to be more generalized.

    .*(CAP[ÍI]TULO +\w+).*\n(.*)

This regex catches on the first group the reserved word and the word next to it. The second group catches the description of the chapter.

After this, we will merge the chapter number and description in the same line.

## Save a poem 

This section dedicated to save a poem meaning, but this approach can be expanded to 