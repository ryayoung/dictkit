# DictKit

A Python package that provides utility data structures with simple but powerful
features, with a focus on flexibility and user experience.

## UtilDict

A feature-enriched dictionary.

- Access items with dot notation.
- Flexible subscripting:
    - Get multiple items at once.
    - Set multiple items or the same value to multiple items at once.
- Add items without mutating - return an updated copy
- Drop items without mutating - return a filtered copy
- Accept a variety of positional argument types at creation, such as other dictionaries, 2-column dataframes, series, or other iterables

### Examples

```python
from dictkit import UtilDict

# Like a dictionary...
ud = UtilDict(a=1, b=2, c=3)
print(ud)  # {'a': 1, 'b': 2, 'c': 3}

# ... but can be initialized from a variety of types
ud = UtilDict({"a": 1}, [("b", 2)], c=3)
print(ud)  # {'a': 1, 'b': 2, 'c': 3}

# Supports dot notation access
print(ud['a'])  # 1
print(ud.a)  # 1

# Get multiple items at once
selected_items = ud[["a", "c"]]
print(selected_items)  # {'a': 1, 'c': 3}

# Set multiple items at once
ud[["a", "c"]] = 10, 30
print(ud)  # {'a': 10, 'b': 2, 'c': 30}

# Set the same value to multiple keys at once
ud[["a", "c"]] = 99
print(ud)  # {'a': 99, 'b': 2, 'c': 99}

# Add items from a variety of types
ud2 = ud.add({"c": 3}, ("d", 4), e=5)
print(ud2)  # {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}

# Add items from a 2-column dataframe
import pandas as pd
ud = UtilDict(a=1, b=2)
df = pd.DataFrame({"key": ["c", "d"], "value": [3, 4]})
ud2 = ud.add(df)
print(ud2)  # {'a': 1, 'b': 2, 'c': 3, 'd': 4}

# Drop multiple items at once
>>> ud3 = ud2.drop("a", "c")
>>> print(ud3)  # {'b': 2, 'd': 4}
```
