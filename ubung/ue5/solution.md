# Task 5.1.1

There’s a method align() in sequitur\_.py – however it doesn’t actually perform the computation (but is a SWIG binding to python_align() in EditDistance.cc. The relevant loops are in EditDistance.cc:57 (initialization), 63 (outer loop), 70 (inner loop).

The interaction between C++ and Python is quite interesting to see, isn’t it? It turns out, it’s automatically generated via SWIG. (For more on this, see <https://www.swig.org/Doc1.3/SWIG.html> ). There’s a definition in sequitur.i which defines the interaction between sequitur\_.py’s align and EditDistance.cc’s python_align in lines 94-100 .

If you take a look at sequitur*.py, most of the magic occurs in \_sequitur*.py (more underscores!) which calls the library file _sequitur_.cpython-38-x86_64-linux-gnu.so (in my case. In your case it could be something else instead of “38” (if you’re not on Python 3.8) and instead of “x86_64” (e.g. on Mach1 chips), “linux-gnu” (duh) and “.so” (likely “.dll” on Windows).) Now, investigating the library file is a bit tedious. Your friends could be strings or readelf -a, maybe filter for “align” with grep.

# Task 5.1.2 & 5.1.3

from sequitur\_ import align

print(align(list("meilenstein"),list("levenshtein")))

ref = ["r", "e:", "g", "e", "n", "s", "b", "U", "r", "k"]
hyp = ["r", "e:", "g", "N", "s", "b", "U", "6", "k"]
print(align(ref, hyp))
print("PER: {}".format(align[ref, hyp](1)/len(ref)))
In case your Python can’t find the “sequitur\_ import”: There’s the (very useful!) environment variable PYTHONPATH which tells Python where to look for modules (in addition to the default places). export PYTHONPATH=./install/lib/python3.8/site-packages/ tells Python to look in the right place (on my computer). You may want to use pwd instead of . in the command so that it also works when you’re changing working directories. Ask around for people who know how to do this on Windows.

# Task 5.2

TBD (will be done interactively during the exercise session)
