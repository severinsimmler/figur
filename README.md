# Figurenerkennung for German literary texts

[![Build Status](https://travis-ci.com/severinsimmler/figur.svg?branch=master)](https://travis-ci.com/severinsimmler/figur)

An important step in the quantitative analysis of narrative texts is the automatic recognition of references to figures, a special case of the generic NLP problem of Named Entity Recognition (NER).

Usually NER models are not designed for literary texts resulting in poor recall. This easy-to-use package is the continuation of the work of [Jannidis et al.](https://opus.bibliothek.uni-wuerzburg.de/opus4-wuerzburg/frontdoor/deliver/index/docId/14333/file/Jannidis_Figurenerkennung_Roman.pdf), using state-of-the-art techniques from the field of Deep Learning reaching a Micro F1-Score of **95.89** and a Macro F1-Score of **67.74**.

<table>
  <thead>
    <tr>
      <th></th>
      <th>TP</th>
      <th>FP</th>
      <th>FN</th>
      <th>TN</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>AppA</th>
      <td>2</td>
      <td>2</td>
      <td>288</td>
      <td>2</td>
    </tr>
    <tr>
      <th>AppTdfW</th>
      <td>418</td>
      <td>131</td>
      <td>383</td>
      <td>418</td>
    </tr>
    <tr>
      <th>Core</th>
      <td>626</td>
      <td>114</td>
      <td>211</td>
      <td>626</td>
    </tr>
    <tr>
      <th>pron</th>
      <td>2284</td>
      <td>604</td>
      <td>766</td>
      <td>2284</td>
    </tr>
    <tr>
      <th>_</th>
      <td>52538</td>
      <td>1546</td>
      <td>749</td>
      <td>52538</td>
    </tr>
  </tbody>
</table>


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
