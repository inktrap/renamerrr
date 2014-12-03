# renamerrr

Simple script that recursively renames your files and folders. It won't follow
symlinks, but recurses in all the folders that don't match an exclude. Think of
it as a list for `rename`, but with excludes (regex and/or list). So it will
turn:

 - `Filename in caps with Spaces--and-[something].doc` into `filename-in-caps-with-spaces-and-something.doc`


But obviously you can change all of that, so **READ THE CODE** before using it!
I am in **NO WAY** responsible if you break something or if this script breaks!

Additionaly, there might be more than one opinion what constitutes a good naming
practice for files or directories. Or which things you like to exclude … so
**READ THE CODE** and change the rules accordingly.
(F.e.: I don't use cvs anymore, but maybe you do.)

**RTFC: Read The Fucking Code!**

I wont include a list of patterns or defaults here, because …

(If you seriously don't know why, please do not use this script!)

Licence: GPL 2.0 <https://www.gnu.org/licenses/gpl-2.0.txt>
