"""
TODO:
    UtilDict add methods for working with keys and values recursively
    - Make functions inspired by pandas functions, but add a `level: int` parameter. So `level=2` means
      do this operation on the first two tree levels. `level=-2` means do it on the LAST two tree levels.
    - It would be nice to control how keys and values are displayed in the `render()` output.
      for instance, you might have a nested dict of pandas dataframes. For a large structure, it can be annoying to
      print out the entirety of each dataframe. So instead, pass a lambda function to determine how *values* are printed.
      If value is dict, pass. If value is dataframe, print value.head(5), etc. That kind of thing.
    - Allow easier renaming of keys using a dictionary, like `df.rename()`.
    - Convert all sub-dictionaries nested inside self to Self's type.
"""
from dictkit import utildict

from dictkit.utildict import UtilDict
