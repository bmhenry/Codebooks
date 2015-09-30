###Codebooks
When I write code, it ends up in any one of a million different directories. Sure, I have folders that 'organize' my code, but these often end up pretty clustered anyways. When I write something clever (which happens far too rarely), I usually can't find it because it's in a module within a package within a folder within another folder... you've been there.

What Codebooks does is give you a good place to copy and paste your clever/useful/boilerplate code, in a way that's easily organized and (perhaps more importantly) searchable. Every code entry you make can be put into a 'codebook', which is whatever kind of general topic you choose, and each entry can be tagged. The way this differs from Evernote, though, is that every entry can have multiple files. No more searching for your commented breakpoints in a note page that are thousands of pages long, you can put your code into separate files.

####How it's organized:
- A codebook stores code entries, with each entry being a place to store your code as well as a description.
- Each entry contains a 'description.txt' file intended to contain a brief description of what the code does, as well as a tag line that is searchable. You can then add as many files as you like to the entry.

Say you've searched through your entries and you've found some code you'd like to use again. Hit the 'Get Code' button at the bottom right of the page, and you can resave that code anywhere you like without copying and pasting all of those files.

Speaking of copy & paste, what if you have some existing code in a folder, and want to add it as an entry to a codebook? Easy: just choose to import a new entry and it will make a copy of your code in the codebook, keeping the file structure intact.

###Runtime
To run the program, double-click codebooks.pyw or run it from the command line with 'python codebooks.pyw' .



Copyright (c) 2015 Brandon Henry
Licensed under the MIT License