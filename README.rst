
==========
Assingment
==========

1) Basic Task: Design of a distributed multimedia database environment
   with the metadata in the meta-level system is shown and
   discussed. The database schema for multimedia database structuring
   is also shown and discussed.

2) Advanced Task-1 (Optional-1): Actual implementation of a
   distributed multimedia database environment with the metadata in
   the meta-level system is shown.

3) Advanced Task-2 (Optional-2): Some original functions defined as
   UDFs (User-Defined Functions)) that realize multimedia & semantic
   database processing are shown.


Design and Implementation of a Psychometric Test
================================================

My task for this assignment is to build psychometric test which first
asks to match impressions for 20 images. Then subject is queried how
well the psychometric table fits to 5 random image.

All images are fetched from flicker's interesting images.


Database schema
---------------

The assignment did not restrict to use only relational database. I
chosen to select RDF database instead. The schema and vocabulary is
shown and discussed. 

Vocabulary is following::

  class Vocab:
    Img = 'http://vocab/Image'
    impression_ = 'http://vocab/impression/'
    color_ = 'http://vocab/color'
    answer = 'http://vocab/answer'
    yes = 'http://vocab/correct#yes'
    no = 'http://vocab/correct#no'

Each new picture url is marked as Image by adding::

  img_url rdf:type Img

Addition to this url's color histogram is read and pushed into::

  img_url color_+colorIndex count

colorIndex is numbered array of colors of Munsell's color system. The
particular index table is shown in /munsell.html

Each selected impression is bound to color count::

  color_+colorIndex impression_+impression count

Also when correct match is requested, one of the following triples is added::

  img_url answer yes
  img_url answer no


Implementation
==============

The implementation is done by html5 web application. It has been
tested only with Google's Chrome. Support for other browsers is not
subject of the assignment and thus bugless working can't be
guaranteed.

Web app is implemented on top of bottle framework.
jQuery and imageloader libraries are used on JavaScript.
Database access uses simple flat file.
Image palette conversion to Munsell's table is done with PIL.
Communication between server and client is done with simplejson library.

Journey notes
-------------

Munsell's color system was the hardest to get right. First I used
simple web colors but I got quite bad results, e.g. everything was
just warm impression (see simple_colors.html).

After two hour googling of how to get this Munsell's color system. Now
I found conversion table for rgb values.
http://www.cis.rit.edu/mcsl/online/munsell.php and that had a link to
http://www.cis.rit.edu/research/mcsl2/online/real_sRGB.xls
I filtered it to less than 256 colors needed by PIL.


Matching of psychometric table and query
========================================

Simple algorithm of matching impression is used. First the color with
greatest pixel count is calculated. Then, the impression of that color
with greatest pixel count is queried from user. User answer yes or no,
if he feels the impression fits.

