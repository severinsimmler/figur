# Figurenerkennung for German literary texts

[![Build Status](https://travis-ci.com/severinsimmler/figur.svg?branch=master)](https://travis-ci.com/severinsimmler/figur)

An important starting point for the quantitative analysis of narrative texts is the automatic recognition of references to figures, a special case of the generic NLP problem of Named Entity Recognition (NER).

Usually NER models are not designed for literary texts resulting in poor recall. This easy-to-use package is the continuation of the work of [Jannidis et al.](https://opus.bibliothek.uni-wuerzburg.de/opus4-wuerzburg/frontdoor/deliver/index/docId/14333/file/Jannidis_Figurenerkennung_Roman.pdf), using state-of-the-art techniques from the field of Deep Learning.

| Micro F1-Score | 95.89 |
|----------------|-------|
| Macro F1-Score | 67.74 |


## Installation

```
$ pip install figur
```

## Example

```python
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
