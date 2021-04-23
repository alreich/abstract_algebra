# Abstract Algebra

#### Experimental implementation of finite groups--for now--and (maybe) later rings, fields, etc.


```python
import algebras as alg
import json
import os
```


```python
# Path to this repo
aa_path = os.path.join(os.getenv('PYPROJ'), 'abstract_algebra')

# Path to a directory containing Algebra definitions in JSON
alg_dir = os.path.join(aa_path, "Algebras")
```

## Store Group in JSON format

* The <b>addition_table</b> <u>must</u> reference group elements according to their index (position) in the <b>element_names</b> list.
* <b>0</b> <u>must</u> always refer to the <b>identity element</b>.


```python
# Path to a JSON file that defines the group V4
v4_json = os.path.join(alg_dir, "v4_klein_4_group.json")

!cat {v4_json}
```

    {"type": "Group",
     "name": "V4",
     "description": "Klein-4 group",
     "element_names": ["e", "h", "v", "hv"],
     "addition_table": [[0, 1, 2, 3],
                      [1, 0, 3, 2],
                      [2, 3, 0, 1],
                      [3, 2, 1, 0]]
    }


## Read JSON Definition to Instantiate a Group Object


```python
v4 = alg.Group(v4_json)
v4
```




    Group('V4', 'Klein-4 group', ['e', 'h', 'v', 'hv'], [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]])



#### The group can also be created at the Command Line:


```python
alg.Group('V4',
          'Another way to construct V4',
          ['e',  'h',  'v', 'hv'],
          [[0, 1, 2, 3],
           [1, 0, 3, 2],
           [2, 3, 0, 1],
           [3, 2, 1, 0]]
         )
```




    Group('V4', 'Another way to construct V4', ['e', 'h', 'v', 'hv'], [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]])



#### And the group can be created from a Python dictionary:


```python
v4_dict = {'type': 'Group',
           'name': 'V4',
           'description': 'Yet another way to define V4',
           'element_names': ['e', 'h', 'v', 'hv'],
           'addition_table': [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]]}

alg.Group(v4_dict)
```




    Group('V4', 'Yet another way to define V4', ['e', 'h', 'v', 'hv'], [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]])



## Add Elements


```python
v4.add('h','v')
```




    'hv'



## Get Inverse Element


```python
v4.inverse('h')
```




    'h'



## View Addition Table using Element Names

The addition table is known as a [Cayley Table](https://en.wikipedia.org/wiki/Cayley_table).

The group operation is referred to here as <i>addition</i> to distinguish it from ring or field <i>multiplication</i> operations.


```python
v4.addition_table_with_names()
```




    [['e', 'h', 'v', 'hv'],
     ['h', 'e', 'hv', 'v'],
     ['v', 'hv', 'e', 'h'],
     ['hv', 'v', 'h', 'e']]



## Check if Abelian


```python
v4.abelian()
```




    True




```python
v4.associative()
```




    True



## Derive Direct Product


```python
v4_x_v4 = v4 * v4
v4_x_v4
```




    Group('V4_x_V4', 'Direct product of V4 & V4', ['e,e', 'e,h', 'e,v', 'e,hv', 'h,e', 'h,h', 'h,v', 'h,hv', 'v,e', 'v,h', 'v,v', 'v,hv', 'hv,e', 'hv,h', 'hv,v', 'hv,hv'], [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], [1, 0, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10, 13, 12, 15, 14], [2, 3, 0, 1, 6, 7, 4, 5, 10, 11, 8, 9, 14, 15, 12, 13], [3, 2, 1, 0, 7, 6, 5, 4, 11, 10, 9, 8, 15, 14, 13, 12], [4, 5, 6, 7, 0, 1, 2, 3, 12, 13, 14, 15, 8, 9, 10, 11], [5, 4, 7, 6, 1, 0, 3, 2, 13, 12, 15, 14, 9, 8, 11, 10], [6, 7, 4, 5, 2, 3, 0, 1, 14, 15, 12, 13, 10, 11, 8, 9], [7, 6, 5, 4, 3, 2, 1, 0, 15, 14, 13, 12, 11, 10, 9, 8], [8, 9, 10, 11, 12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 6, 7], [9, 8, 11, 10, 13, 12, 15, 14, 1, 0, 3, 2, 5, 4, 7, 6], [10, 11, 8, 9, 14, 15, 12, 13, 2, 3, 0, 1, 6, 7, 4, 5], [11, 10, 9, 8, 15, 14, 13, 12, 3, 2, 1, 0, 7, 6, 5, 4], [12, 13, 14, 15, 8, 9, 10, 11, 4, 5, 6, 7, 0, 1, 2, 3], [13, 12, 15, 14, 9, 8, 11, 10, 5, 4, 7, 6, 1, 0, 3, 2], [14, 15, 12, 13, 10, 11, 8, 9, 6, 7, 4, 5, 2, 3, 0, 1], [15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]])



## Convert to Dictionary or JSON


```python
v4.to_dict()
```




    {'type': 'Group',
     'name': 'V4',
     'description': 'Klein-4 group',
     'element_names': ['e', 'h', 'v', 'hv'],
     'addition_table': [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]]}




```python
v4.dumps()
```




    '{"type": "Group", "name": "V4", "description": "Klein-4 group", "element_names": ["e", "h", "v", "hv"], "addition_table": [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]]}'


