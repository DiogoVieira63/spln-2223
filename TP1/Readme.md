# TPC 1

The goal of this homework was to extract the info of a pdf file (**medicina.pdf**) to an organized structure, eg. json.

### Part 1 - Pdf conversion

First, we need to covert the pdf to a more managable file type.
There are two options: **txt** or **xml**.
With txt, we lose a lot of information about types of fonts, bold, italics, etc..
So, it will be converted to a xml file.
The command used for this conversion was:

        pdftohtml -f 20 -l 543 -xml medicina.pdf medicina.xml

This will convert the file **medicina.pdf** from pages 20-543 to **medicina.xml**.

### Part 2 - XML clean up

If we explore the xml file, we can see that there is a lot of irrelevant information.
First, the headers and footers of each page are removed.

Each text tag of xml has this information: 

    <text top="154" left="114" width="40" height="18" font="3"><b>1  á    f</b></text>

The only info that can be useful from these tag's attributes is the **font**. The others are related to the position at the file, and there is not much we can do with that information.

So, we will preserve the font and the text of each tag. The result:

    #3#<b>1  á    f</b>

That's much cleaner. After this, we can see that because we have the information about the font, the bold tag will problaly not be useful.
And there is a big chunk of spaces between each word, that we can reduce to one space.
We remove these two things and the result is:

    #3#1 á f

Now, we have only the information that is necessary.

### Part 3 - Markers

In this part, it will be added markers to be easier to parse the information afterwards.

To do this, we have to study the xml file to see what each font represents.

Here's an example of an entry:

    #3#7 abdución f
    #6#Fisioloxía Anatomía
    #5# SIN.- separación
    #0# es 
    #7#abducción
    #0#; 
    #7#separación
    #0# en 
    #7#abduction
    #0# pt 
    #7#abdução
    #0#; 
    #7#separação
    #0# la 
    #7#abductio
    #9#Nota.- Evítese “abducción”.
    #3# aberración cromosómica 
    #5#Vid.- anomalía cromosómica


The definition of each complete and remissive entry has the font 3.
So we will replace these, with the marker **"###"**.

The font 7 represents the value of each translation, we will replace with **"-"**. And the line prior represents the language that it's referring to, so we will replace that with **"@@@"**.

For the category,**SIN**,**Vid** and **Nota**, we will just remove the font and replace with nothing.

In this process, before the replacement with the marker, we make sure that if two consecutive lines have the same font, their content will be merge into one line.

After this process, this is the result:

    ###7 abdución f
    Fisioloxía Anatomía
    SIN.- separación
    @@@ es 
    -abducción
    -separación
    @@@ en 
    -abduction
    @@@ pt 
    -abdução
    -separação
    @@@ la 
    -abductio
    Nota.- Evítese “abducción”.
    ### aberración cromosómica 
    Vid.- anomalía cromosómica

### Part 4 - Build Json

At this stage, we will make a split of **###**, so each element of a resulting list will either be a complete entry or a remissive entry.

Now, we will iterate trough the list, and parsing each entry accordingly.

The final result:

    {
            "nome": "abdución",
            "género": "f",
            "plural": "no",
            "indíce": "7",
            "categoria": [
                "Fisioloxía",
                "Anatomía"
            ],
            "sinonimos": [
                "separación"
            ],
            "nota": "Evítese “abducción”.",
            "traducoes": {
                " es ": [
                    "abducción",
                    "separación"
                ],
                " en ": [
                    "abduction"
                ],
                " pt ": [
                    "abdução",
                    "separação"
                ],
                " la ": [
                    "abductio"
                ]
            }
        }