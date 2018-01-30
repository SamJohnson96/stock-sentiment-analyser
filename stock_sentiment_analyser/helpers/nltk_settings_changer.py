import fileinput

for line in fileinput.input('/home/ec2-user/cloud-data-miner/package/tmp/nltk/data.py', inplace=True):
      print line.rstrip().replace("      str('/usr/share/nltk_data'),", "      str('/var/task/nltk_data'),")
