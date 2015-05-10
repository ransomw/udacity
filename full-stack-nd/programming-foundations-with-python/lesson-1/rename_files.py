import os

NUM_CHARS = '0123456789'

def rename_files(dir_name):
    for filename in os.listdir(dir_name):
        new_filename = filter(lambda c: c not in NUM_CHARS, filename)
        if new_filename != filename:
            os.rename(os.path.join(dir_name, filename),
                      os.path.join(dir_name, new_filename))
            print "renamed '"+filename+"' to '"+new_filename+"'"


rename_files('prank')
