#!/usr/bin/env python
u'''rename arbitrary files and folders to a specified format'''
import os
import sys
import re


def needs_rename(filename):
    if make_name(filename) != filename:
        return True
    return False


def is_valid(check_entity, rootdir, entity, exclude_entities, exclude_regexes):
    entity_path = os.path.abspath(os.path.join(rootdir, entity))
    # print "checking " + filepath
    exclude_entities = ['.gitignore', '']
    exclude_regex = [r'TODO.*', r'README.*', r'LICEN[SC]E.*', r'\..*']
    if check_entity(entity_path) and (not os.path.islink(entity_path)):
        try:
            index = exclude_entities.index(entity)
        except ValueError:
            for exclude_regex in exclude_regexes:
                if re.match(exclude_regex, entity):
                    print "     %s matches exclude regex %s" % (entity, exclude_regex)
                    return False
            return True
        print "     %s matches exclude entry %s" % (entity, exclude_entities[index])
    return False


def is_valid_file(dirname, filename):
    exclude_entities = ['.gitignore', '']
    exclude_regexes = [r'TODO.*', r'README.*', r'LICEN[SC]E.*', r'\..*']
    return is_valid(os.path.isfile, dirname, filename, exclude_entities, exclude_regexes)


def is_valid_dir(dirname, filename):
    exclude_entities = [
        'vagrant', 'opt', 'work', '.git', '.svn', '.hg', '.env']
    exclude_regexes = ['\..*']
    return is_valid(os.path.isdir, dirname, filename, exclude_entities, exclude_regexes)


def recursive_rename(rootdir, dirname):
    if is_valid_file(rootdir, dirname):
        return renamer(rootdir, dirname)
    elif not is_valid_dir(rootdir, dirname):
        return True

    dirpath = os.path.abspath(os.path.join(rootdir, dirname))
    print "traversing dir: %s" % os.path.join(rootdir, dirname)

    for item in os.listdir(dirpath):
        recursive_rename(dirpath, item)
    # finally check if the dir needs renaming
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
    #    .tar.gz and bzip2 aso.
    '''
    new_name = re.sub(r'[\\\"\'\{\}\(\)\[\]]', '', new_name)
    return new_name


def renamer(root, name):
    if not is_valid_file(root, name) or is_valid_dir(root, name):
        return False

    print "%s file %s" % (is_valid_file(root, name), name)
    print "%s dir %s" % (is_valid_dir(root, name), name)

    new_name = needs_rename(name)
    if not new_name:
        return False
    new_target = os.path.join(root, new_name)
    if not os.path.exists(new_target):
        # os.rename(os.path.join(root, name), os.path.join(root,
        # make_name(name)))
        print "renamed %s to %s" %\
            (os.path.join(root, name), new_target)
    return True


def usage():
    print "USAGE: x (PATH)"
    return True


def main():
    # traverse top down because files of excluded dirs should be excluded
    # recursively traverse directories until no dirs in dir (dirs first)
    # rename all files if file is not in excluded files
    # visited all dirs? means the dirs in this directory can be renamed

    seedlist = []
    if len(sys.argv) > 1:
        seedlist = sys.argv[1:]
    else:
        seedlist.append(os.curdir)

    for seed in seedlist:
        seedpath = os.path.abspath(os.path.realpath(seed))
        recursive_rename('', seedpath)
    return True

if __name__ == '__main__':
    main()
