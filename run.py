import shutil
from os import listdir, mkdir, remove
from os.path import join, basename
from subprocess import check_output
from pyunpack import Archive
DIR = 'DIR{}'

count = 0
for count in xrange(0,1000):
    path = join(DIR.format(count),listdir(DIR.format(count))[0])
    print path
    count += 1
    try:
        mkdir(DIR.format(count))
    except Exception:
        pass
    file_header = check_output(['file', path])
    print file_header
    if 'ARJ archive data' in file_header:
	shutil.move(path, path + '.arj')
	path = path + '.arj'
    if 'Zoo archive data' in file_header:
	print 'zooing'
	shutil.move(path, path + '.zoo')
	check_output(['zoo', 'x', basename(path) + '.zoo'], cwd=DIR.format(count-1)) 
	remove(path + '.zoo')
	path = join(DIR.format(count-1),listdir(DIR.format(count-1))[0])
	print path
	print "2000000000000000000000"
	shutil.move(path,DIR.format(count)) 
    elif 'NuFile archive' in file_header:
	new_file = check_output(['./nulib2', '-p', path]) 
	with open(join(DIR.format(count), 'newfile'), 'wb') as f:
	   f.write(new_file)
    elif 'bzip2 compressed' in file_header:
	check_output(['bzip2', '-d', path]) 
	shutil.move(path+'.out',DIR.format(count)) 
    elif 'lzip compressed' in file_header:
	check_output(['lzip', '-d', path]) 
	shutil.move(path+'.out',DIR.format(count)) 
    elif 'XZ compressed data' in file_header:
	shutil.move(path, path + '.xz')
	path = path + '.xz'
	check_output(['xz', '-d', path]) 
	path = join(DIR.format(count-1),listdir(DIR.format(count-1))[0])
	shutil.move(path,DIR.format(count)) 
    else:
        Archive(path).extractall(DIR.format(count))

