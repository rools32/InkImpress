import os

def create_zip_file(filename, files):
	import zipfile

	zip = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)

	for name, file in files.items():
		zip.write(file, name)
	
	zip.close()

def create_tar_file(filename, files):
	import tarfile

	tar = tarfile.open(filename, 'w:gz')

	for name, file in files.items():
		tar.add(file, name)
	
	tar.close()

def create_package_file_dict(prefix, source):
	files = {}

	for file in source:
		if str(file).find("inkscapeExtensions") != -1:
			files[prefix + os.sep + "inkscapeExtensions" + os.sep + os.path.basename(str(file))] = str(file)
		elif str(file).find("scripts") != -1:
			files[prefix + os.sep + "inkscapeExtensions" + os.sep + os.path.basename(str(file))] = str(file)
		elif str(file).find("documentation") != -1:
			files[prefix + os.sep + os.path.basename(str(file))] = str(file)

	return files

def create_zip_archive(target, source, env):
	package_name = str(target[0])

	files = create_package_file_dict(os.path.basename(package_name), source)
	create_zip_file(package_name, files)

	return None

def create_tar_gz_archive(target, source, env):
	package_name = str(target[0])

	files = create_package_file_dict(os.path.basename(package_name), source)
	create_tar_file(package_name, files)

	return None

env = Environment()

env.Append(BUILDERS = {'tarGzArchive' : Builder(action = create_tar_gz_archive)})
env.Append(BUILDERS = {'zipArchive' : Builder(action = create_zip_archive)})
env.tarGzArchive('jessyink-1.5.6.tar.gz', ['documentation/mpl.txt', 'documentation/gpl.txt', 'documentation/JessyInk.svg', 'documentation/README.txt', env.Glob('inkscapeExtensions/*'), env.Glob('scripts/*')])
env.zipArchive('JessyInk-1.5.6.zip', ['documentation/mpl.txt', 'documentation/gpl.txt', 'documentation/JessyInk.svg', 'documentation/README.txt', env.Glob('inkscapeExtensions/*'), env.Glob('scripts/*')])

