#!/usr/bin/python3

import sys
import operator
from prettytable import PrettyTable

def help_():
	print("usage: nahw1-2_0310029.py [-h] filename [-u] [-after AFTER] [-before BEFORE] [-n N] [-t T] [-r]\n\n")
	print("Auth log parser.\n")
	print("position arguments:\n  filename      log file path.\n")
	print("optional arguments:\n  -h, --help      show this hekp message and exit\n")
	print("  -u              Summary failed login log and sort log by user.\n")
	print("  -after AFTER    Filter log after date. Format YYYY-MM-DD-HH:MM:SS")
	print("  -before BEFORE  Filter log before date. Format YYYY-MM-DD-HH:MM:SS")
	print("  -n N            Show only the user of the most N-th times")
	print("  -t T            Show only the user of attacking equal or more than T times")
	print("  -r              Sort in reverse order")

def turn(date):
	date = date.replace("Jan", "01")
	date = date.replace("Feb", "02")
	date = date.replace("Mar", "03")
	date = date.replace("Apr", "04")
	date = date.replace("May", "05")
	date = date.replace("Jun", "06")
	date = date.replace("Jul", "07")
	date = date.replace("Aug", "08")
	date = date.replace("Sep", "09")
	date = date.replace("Oct", "10")
	date = date.replace("Nov", "11")
	date = date.replace("Dec", "12")
	if date[4] == " ":
		date = date[:3] + "0" + date[3:]
	
	date = date.replace(" ", "")
	date = date.replace(":", "")

	return date

def parse_log():
	argv_len = len(sys.argv)
	if argv_len == 2 or argv_len == 3 or "-n" in sys.argv or "-t" in sys.argv:
		if sys.argv[1] == "-h" or sys.argv[1] == "--help":
			help_()
			sys.exit()
		else:
			filename = sys.argv[1]
			with open(filename) as f:
				content = f.readlines()
			content = [x.strip() for x in content]
		
		dict = {}
		dict_list = []

		for cont in content:
			sub = "Invalid user"
			start = cont.find(sub)
			end = cont.find(" ",start+13)
			real_name = cont[start+13:end]
			if real_name in dict:
				count = dict[real_name]
				count = count + 1
				temp_dict = { real_name : count}
				dict.update(temp_dict)
			else:
				count = 1
				temp_dict = { real_name : count}
				dict.update(temp_dict)

		for key, value in dict.items():
			temp = [key, value]
			dict_list.append(temp)
	
		if argv_len == 2 or "-n" in sys.argv or "-t" in sys.argv:
			sorted_dict = sorted(dict_list, key=operator.itemgetter(1), reverse=True)
			#print(type(sorted_dict))
			if "-n" in sys.argv:
				N = int(sys.argv[3])
				top_N_list = sorted_dict[:N]
			elif "-t" in sys.argv:
				T = int(sys.argv[3])
				More_T_list = []
				for key, value in sorted_dict:
					if value >= T:
						temp = [key, value]
						More_T_list.append(temp)


		elif "-r" in sys.argv:
			sorted_dict = sorted(dict_list, key=operator.itemgetter(1))
		else:
			sorted_dict = sorted(dict_list, key=operator.itemgetter(0))

		x = PrettyTable()
		field = [ 'user', 'count']
		x. field_names=field
		
		if "-n" in sys.argv:
			which_dict = top_N_list
		elif "-t" in sys.argv:
			which_dict = More_T_list
		else:
			which_dict = sorted_dict

		for data in which_dict:
			x.add_row(data)
		print(x.get_string())
		sys.exit()

	if "-after" in sys.argv or "-before" in sys.argv:
		if "-after" in sys.argv:
			after_time_index = sys.argv.index('-after') + 1
			after_time = sys.argv[after_time_index]
			after_time = after_time[5:]
			after_time = after_time.replace("-", "")
			after_time = after_time.replace(":", "")
		if "-before" in sys.argv:
			before_time_index = sys.argv.index('-before') + 1
			before_time = sys.argv[before_time_index]
			before_time = before_time[5:]
			before_time = before_time.replace("-", "")
			before_time = before_time.replace(":", "")

		filename = sys.argv[1]
		with open(filename) as f:
			content = f.readlines()
		content = [x.strip() for x in content]

		name_list = []
		main_list = []
	
		for cont in content:
			sub = "Invalid user"
			start = cont.find(sub)
			end = cont.find(" ",start+13)
			real_name = cont[start+13:end]
			date_index = cont.find(":")
			date = cont[:date_index + 6]
			date = turn(date)
			temp_list = [real_name, date]
			main_list.append(temp_list)
		#print(main_list)
		after_list = []
	
		if "-after" in sys.argv:
			A_time = int(after_time)
			for data in main_list:
				data_time = int(data[1])
				if data_time >= A_time:
					after_list.append(data)
		#print(after_list)
		before_list = []
		if "-before" in sys.argv:
			B_time = int(before_time)
			if after_list == []:  # no after in argv, use main_list to do.
				for data in main_list:
					data_time = int(data[1])
					if data_time <= B_time:
						before_list.append(data)
			else:  # have after in argv, use after_list to do.
				for data in after_list:
					data_time = int(data[1])
					if data_time <= B_time:
						before_list.append(data)
		if "-before" in sys.argv:
			final_list = before_list
		else:
			final_list = after_list
	
		#print(final_list)
	
		output_list = []
		for data in final_list:
			if output_list == []:
				temp_list = [data[0], 1]
				output_list.append(temp_list)
				name_list.append(data[0])
			else:
				if data[0] in name_list:
					index = name_list.index(data[0])
					count = output_list[index][1]
					count = count + 1
					output_list[index][1] = count
				else:
					temp_list = [data[0], 1]
					output_list.append(temp_list)
					name_list.append(data[0])
		print(output_list)
	
		y = PrettyTable()
		field = ['user', 'count']
		y.field_names = field

		for data in output_list:
			y.add_row(data)
	
		print(y.get_string())
		sys.exit()

if __name__ == "__main__":
	parse_log()
