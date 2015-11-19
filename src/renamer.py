#!/usr/bin/env python3.4
'''rename arbitrary files and folders to a specified format'''
import os
import sys
import re
import argparse

'''
License: GPL 2.0 <https://www.gnu.org/licenses/gpl-2.0.txt>
'''

'''
renaming utility that will relentlessly break
 - your LaTeX documents (if you include some files that have been changed)
 - webpages (in the improbable case that you are using an image or something)
 - everything else, f.e.: if config files are changed

but it will make clean filenames for your media files :)
so use it selectively and check changes before applying them

WILL FIX MAYBE
 - do not rename by default, use -n or --no-act by default
 - do not traverse into subdirectories by default, use -r or --recurse for that
 - be verbose by default, use -q or --quiet for this
'''

def verbose(msg):
    if args.verbose == True:
        print(msg)


def debug(msg):
    if args.debug == True:
        print(msg)


def needs_rename(filename):
    if make_name(filename) != filename:
        return True
    return False


def is_valid(check_entity, rootdir, entity, exclude_entities, exclude_regexes):
    entity_path = os.path.abspath(os.path.join(rootdir, entity))
    if check_entity(entity_path) and (not os.path.islink(entity_path)):
        try:
            index = exclude_entities.index(entity)
        except ValueError:
            for exclude_regex in exclude_regexes:
                if re.match(exclude_regex, entity):
                    debug("     %s matches exclude regex %s" %
                          (entity, exclude_regex))
                    return False
            return True
        debug("     %s matches exclude entry %s" %
              (entity, exclude_entities[index]))
    return False


def is_valid_file(dirname, filename):
    exclude_entities = ['.gitignore', 'Makefile']
    exclude_regexes = [r'^[A-Z]+$', r'.*Makefile.*', r'.*VERSION.*',
                       r'.BUGS.*', r'.*TODO.*',
                       r'.*README.*', r'.*LICEN[SC]E.*', r'\..*']
    return is_valid(os.path.isfile, dirname, filename,
                    exclude_entities, exclude_regexes)


def is_valid_dir(dirname, filename):
    exclude_entities = [
        'vagrant', 'opt', 'work', '.git', '.svn', '.hg', '.env']
    exclude_regexes = [r'\..*']
    return is_valid(os.path.isdir, dirname, filename,
                    exclude_entities, exclude_regexes)


def recursive_rename(rootdir, dirname, recurse=True):
    if is_valid_file(rootdir, dirname):
        return renamer(rootdir, dirname)
    elif not is_valid_dir(rootdir, dirname):
        return True

    dirpath = os.path.abspath(os.path.join(rootdir, dirname))
    debug("traversing dir: %s" % os.path.join(rootdir, dirname))

    # attention! os.listdir returns unicode filenames
    # what happens with chinese files, or russian, or malformed names or
    # undecodable stuff?

    if recurse == True:
        # Why is the used directory called twice?
        for item in os.listdir(dirpath):
            recursive_rename(dirpath, item, True)
    return renamer(rootdir, dirname)


def make_name(name):
    # maybe lowercasing everything is not good (see LaTeX or locales de_DE)
    name = name.lower()
    new_name = re.sub(r'\s', '-', name)
    new_name = re.sub(r'[-]+', '-', new_name)
    '''
    # do not delete dots that separate a filename ending:
        foo.pdf
        foo.ps
        foo.c
        foo.README (seriously)
    new_name = re.sub(r'\.(?!..?.?$)', '-', new_name)
    #this is excluded because there is stuff like
    #    .tar.gz and variations.
    '''
    new_name = re.sub(r'[\\\"\'\{\}\(\)\[\]]', '', new_name)
    new_name = re.sub(r'\s', '-', name)
    new_name = re.sub(r'[-]+', '-', new_name)

    # check if deletion matched everything
    if len(new_name) < 1:
        return name

    return new_name


def renamer(root, name):
    if not (is_valid_file(root, name) or is_valid_dir(root, name)):
        return False

    if needs_rename(name) is False:
        return False

    # - when you are in a directory: Foo and specify all by *
    # - the new file/pathname operates on the whole path: foo/newfile
    # - but foo does not exist
    if not root:
        root,name = os.path.split(name)

    new_target = os.path.join(root, make_name(name))
    if not os.path.exists(new_target):
        try:
            os.rename(os.path.join(root, name), new_target)
            verbose("renamed %s to %s" %
                    (os.path.join(root, name), new_target))
        except KeyboardInterrupt:
            pass
        except OSError:
            # this should not happen
            print(("can not rename %s to %s" % (os.path.join(root, name), new_target)))
    return True


def main():
    global args
    # traverse top down because files of excluded dirs should be excluded
    # recursively traverse directories until no dirs in dir (dirs first)
    # rename all files if file is not in excluded files
    # visited all dirs? means the dirs in this directory can be renamed

    '''
    print("(Obviously you can edit the source to remove the following check)")
    print('YES, I KNOW, that this script may brake my things and')
    print("YES, I READ THE SOURCE! I hereby confirm these two facts!")
    yes = raw_input("Type: yes!: ")
    if yes != "yes!":
        sys.exit(0)
    '''

    parser = argparse.ArgumentParser(
        description='Options are optional. All other values are passed in as the seedlist. Seedlist defaults to the current directory.')
    parser.set_defaults(verbose=False, recursive=False, act=True, debug=False)
    parser.add_argument(
        '-v', '--verbose',  dest='verbose', help='be verbose', action='store_true')
    parser.add_argument(
        '-d', '--debug',  dest='debug', help='be debuggy', action='store_true')
    parser.add_argument('-r', '--recursive',  dest='recursive',
                        help='recurse into directories', action='store_true')
    parser.add_argument('-n', '--no-act',  dest='act',
                        help='no act, only simulate (only useful with --verbose)', action='store_false')
    parser.add_argument('seedlist', nargs='*')
    args = parser.parse_args()

    if len(args.seedlist) < 1:
        args.seedlist.append(os.curdir)

    try:
        for seed in args.seedlist:
            seedpath = os.path.abspath(os.path.realpath(seed))
            recursive_rename('', seedpath, args.recursive)
    except IOError:
        # TODO: what todo here? head wants
        # maybe 10 lines, therefore a broken
        # pipe emerges.

        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(0)
    return True

if __name__ == '__main__':
    main()
