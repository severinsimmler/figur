"""
Figurenerkennung for German literary texts.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

figur is very easy to use:

```
>>> import figur
>>> text = "Der Gärtner entfernte sich eilig, und Eduard folgte bald."
>>> figur.tag(text)
    SentenceId      Token      Tag
0            0        Der        _
1            0    Gärtner  AppTdfW
2            0  entfernte        _
3            0       sich     pron
4            0      eilig        _
5            0          ,        _
6            0        und        _
7            0     Eduard     Core
8            0     folgte        _
9            0       bald        _
10           0          .        _
```
"""

from .api import tag
