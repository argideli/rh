pygrep is a tool that can be used to to search one or two files for matches of
a regular expression. It has four modes of output, the colored [-c]  that paints
the matches with red color. The caret indicator mode that places the caret ^ symbol
under every character of a match. The combination of the caret and color mode [-cu],
which places a red colored caret under every match, and lastly the colon [:] delimited
machine output in the format: filename:line_number:start_position:matched_text.
Also there is a functionality testing script that can be used to evaluate possible
changes in the code, the script uses the avocado framework to run the testing suite
and also it can be used in conjunction with the tox automation tool to test in different
python versions.

usage: pygrep.py [-h] [-u] [-c] [-m] regex [files [files ...]]

positional arguments:

  regex             Search expression enclosed in single quotes ex.
                    'something.*[0-9]'

  files             One or two files to be searched for matches of [regex]

optional arguments:

  -h, --help        show this help message and exit

  -u, --underscore  Print '^' under the matching text

  -c, --color       Colorize matches

  -m, --machine     Generate machine readable output`


*Requirements*

Running:

* python >= 2.7

Testing:

* avocado framework https://avocado-framework.github.io/
* avocado-framework-plugin-loader-yaml
* avocado-framework-plugin-varianter-yaml-to-mux

*Example usage*


stdin:

  python pygrep.py -c  ':.\*con.* '  <  log_file2.txt

pipe:

  cat log_file2.txt | python pygrep.py -c  ':.\*con.* '

file read:

  python pygrep.py -c  ':.\*con.* ' log_file1 log_file2.txt
