# renamerrr

[![Build Status](https://travis-ci.org/inktrap/renamerrr.svg?branch=master)](https://travis-ci.org/inktrap/renamerrr)

## What does renamerrr do?

renamerrr is a simple script that recursively renames your files and folders.

(Means: If you want to break things, you are welcome. But I am not responsible.
You have been warned!)

Think of it as a list for `rename`, but with excludes (regex and/or list-based). So
it will turn:

 - `Filename in caps with Spaces--and-[something].doc` into `filename-in-caps-with-spaces-and-something.doc`
 - but not in a dir like .git/ or .hg/ and also not if the file is named f.e. TODO.md or README.md
 - and also not if the file is a symlink (and it won't follow symlinks)


## Fork me, edit me, …

There might be more than one (read: mine :)) opinion what constitutes a good
naming practice for files or directories. Or which things someone would like to
exclude … so **READ THE CODE** and change the rules accordingly. F.e.: I don't
use cvs anymore, but maybe you do.


## Examples

Edit: I will include some examples in the near future.


## Licence

Currently GPL 2.0 <https://www.gnu.org/licenses/gpl-2.0.txt>

