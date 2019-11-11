from  random import uniform
from subprocess import call
import timeit
import os

def dump_to_file(filename,contents):
	f = open(filename,"w")
	f.write(contents)
	f.close()


topo_template = open("topo.template","r").read()
xp_template = open("xp.template","r").read()

schemes = ['quic','https']
losses = [0,2.5]
band_widths = [0.1,100]
delays = [0,150]
file_sizes = [1024,2048,4096,8192]
ccs = ['olia','cubic']

number_of_xp = 30
xp_no = 0
exp_run_time_stamp = int(timeit.default_timer())
os.mkdir("/home/mininet/exps/{:d}".format(exp_run_time_stamp))

for _ in range(number_of_xp):
	for file_size in file_sizes:
		for sch in schemes:
			for cc in ccs:
						file_path="/home/mininet/exps/{:d}/exp_{}.json".format(exp_run_time_stamp,xp_no)
						xp_no+=1
						loss=[uniform(losses[0],losses[1]),uniform(losses[0],losses[1])]
						band_width=[uniform(band_widths[0],band_widths[1]),uniform(band_widths[0],band_widths[1])]
						delay=[uniform(delays[0],delays[1]),uniform(delays[0],delays[1])]
						additional=""
						if sch == "quic":
							additional="quicMultipath:{:d}\n".format(1 if cc == "olia" else 0)

						topo_file = topo_template.format(loss=loss,delay=delay,bandwidth=band_width)
						xp_file = xp_template.format(additional=additional,filesize=file_size,type=sch,cc=cc,output=file_path)
						dump_to_file("exp.topo",topo_file)
						dump_to_file("exp.xp",xp_file)
						rc = call("sudo /home/mininet/git/minitopo/src/mpPerf.py -x exp.xp -t exp.topo", shell=True)
						print(file_path,rc)

				
				