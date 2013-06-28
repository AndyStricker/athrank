Athrank - Athletics Ranking System Core
=======================================

Overview
--------

A very simple, cross platform ranking software. It stores all data in
a database and provides a RESTful API interface and some command line
tools.

It's intended to be used with Athinput, the simple input interface, or
be contolled by whatever you'll use as the interface.

The rankings calculations are exchangeable, but currently only the
SLV 94 ranking table are implemented.

Story
-----

For a athletics event with children I've had the duty to lead the
rankings office. The software intended to to help to create the ranking
table was a bit legacy and strongly depended on a platform of a hugh
software vendor. As I didn't wanted to support this vendor by buying
licences I decided to build an open source solution.

As usual I did a research first to check if there are already software
solutions available. After a bit research I found an open source
solution for large athletics competitions developted by members of
Swiss Athletics (http://www.swiss-athletics.ch/) called Athletica
(see [1]). I suggest you to check this out first, as it's a very
complete and feature full software suite.

Well that was exactly my problem: I didn't need a feature complete
software suite, just a simple tool to enter results calculate rankings
and print them as a ranking table ready to be included in a document
together with other ranking tables.

[1] http://www.swiss-athletics.ch/?Itemid=128&option=com_jumi&fileid=4&lang=de

Copyright and Licence
---------------------

Copyright © 2013 Andreas Stricker <andy@knitter.ch>

Athrank is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

