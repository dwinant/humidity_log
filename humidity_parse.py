import os
import sys

OUTFILE = 'humidity_data.csv'
DIRSEP = '/'
DEFAULT_DIR = 'h_files'


def parse_line (out, line, filename):
	flds = line.split(',')
	if len(flds) == 4:
		out.write ("%s,%s,%s,%s,%s\n" % (flds[0], flds[1], flds[2], flds[3].rstrip(), filename))
	else:
		print ("skip line: %s" % line)

def parse_file (filename, outfile):
	with open(outfile, "a") as out:
		with open(filename, "r") as inf:
			for line in inf:
				parse_line (out, line, filename)


def parse_all (dir):
	# clear out any old output
	with open(OUTFILE, "w"):
		pass

	for file in os.listdir (dir):
		if file.endswith (".log"):
			print ("parsing: %s" % file)
			parse_file ("%s%s%s" % (dir, DIRSEP, file), OUTFILE)


def main ():
	if len(sys.argv) > 1:
		dirname = sys.argv[1]
	else:
		dirname = DEFAULT_DIR
	

	print ("executing in %s%s%s" % (os.getcwd(), DIRSEP, dirname))
	parse_all (dirname)

main()


