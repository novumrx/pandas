""" support numpy compatiblitiy across versions """

import numpy as np
from distutils.version import LooseVersion
from pandas.compat import string_types, string_and_binary_types

# TODO: HACK for NumPy 1.5.1 to suppress warnings
# is this necessary?
try:
    np.seterr(all='ignore')
except Exception:  # pragma: no cover
    pass

# numpy versioning
_np_version = np.version.short_version
_np_version_under1p8 = LooseVersion(_np_version) < '1.8'
_np_version_under1p9 = LooseVersion(_np_version) < '1.9'
_np_version_under1p10 = LooseVersion(_np_version) < '1.10'
_np_version_under1p11 = LooseVersion(_np_version) < '1.11'

if LooseVersion(_np_version) < '1.7.0':
    raise ImportError('this version of pandas is incompatible with numpy < 1.7.0\n'
                      'your numpy version is {0}.\n'
                      'Please upgrade numpy to >= 1.7.0 to use '
                      'this pandas version'.format(_np_version))


def tz_replacer(s):
    if isinstance(s, string_types):
        if s.endswith('Z'):
            s = s[:-1]
        elif s.endswith('-0000'):
            s = s[:-5]
    return s


def np_datetime64_compat(s, *args, **kwargs):
    """
    provide compat for construction of strings to numpy datetime64's with
    tz-changes in 1.11 that make '2015-01-01 09:00:00Z' show a deprecation
    warning, when need to pass '2015-01-01 09:00:00'
    """

    if not _np_version_under1p11:
        s = tz_replacer(s)
    return np.datetime64(s, *args, **kwargs)


def np_array_datetime64_compat(arr, *args, **kwargs):
    """
    provide compat for construction of an array of strings to a
    np.array(..., dtype=np.datetime64(..))
    tz-changes in 1.11 that make '2015-01-01 09:00:00Z' show a deprecation
    warning, when need to pass '2015-01-01 09:00:00'
    """

    if not _np_version_under1p11:

        # is_list_like
        if hasattr(arr, '__iter__') and not \
           isinstance(arr, string_and_binary_types):
            arr = [tz_replacer(s) for s in arr]
        else:
            arr = tz_replacer(s)

    return np.array(arr, *args, **kwargs)

__all__ = ['_np_version',
           '_np_version_under1p8',
           '_np_version_under1p9',
           '_np_version_under1p10',
           '_np_version_under1p11',
           ]
