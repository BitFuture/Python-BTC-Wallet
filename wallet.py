from bitcoin import *
import webbrowser, time, os

directory = '/home/jack/bitcoin/keys' # CHANGE THIS!

os.chdir(directory)
key_files = os.listdir(directory)

# keydict = {"Address": ["Private Key (256)", "Private Key (WIF)", "Public Key", "Hash 160", "Index"]}
# ----------------------------------------------------------------------------------------------------

# Organises the text files into a dictionary
def key_dictionary():
	keydict = {}
	index = 0
	
	for files in key_files:
		f = open(files, 'r')
		text = f.read()
		list = text.split()
		list.append(index)
		address_txt = str(files)
		address = address_txt[:-4]
		keydict[address] = list
		index += 1
		
	return keydict


# Creates an index number for each address
def list_of_indices(keydict):
	index = 0
	index_list = []
	
	for x in range(len(keydict)):
		index_list.append(index)
		index += 1
	
	return index_list

		
# Lists the addesses and their unspent outputs
def address_menu(keydict, index_list):
	print "\nAddresses:"
	addresses = keydict.keys()
	
	for address_index in index_list:
		each_address = addresses[address_index]
		unspent_dict_list = bci_unspent(each_address)
		
		if unspent_dict_list == []:
			unspent_values = 0
		else:
			unspent_value_list = []
			
			for x in range(len(unspent_dict_list)):
				each_unspent_dict = unspent_dict_list[x]
				each_unspent_value = float(each_unspent_dict['value'])
				unspent_value_list.append(each_unspent_value)
			
			unspent_values = sum(unspent_value_list)
			
		print "[%s] %s ----- (%s)" % (address_index, each_address, unspent_values / 100000000)
		
	return addresses
		
		
def list_unspent_outputs(address):
	unspent_dict_list = bci_unspent(address)
	
	if unspent_dict_list == []:
		unspent_outputs = 0
	else:
		unspent_outputs_list = []
		
		for x in range(len(unspent_dict_list)):
			unspent_dict = unspent_dict_list[x]
			unspent_outputs = unspent_dict['output']
			unspent_outputs_list.append(unspent_outputs)
		
	return unspent_outputs_list
	

def list_unspent_values(address):
	unspent_dict_list = bci_unspent(address)
	
	if unspent_dict_list == []:
		unspent_values = 0
	else:
		unspent_values_list = []
		
		for x in range(len(unspent_dict_list)):
			unspent_dict = unspent_dict_list[x]
			unspent_values = unspent_dict['value']
			unspent_values_list.append(unspent_values)

	return unspent_values_list


def address_options(addresses):
	
	while True:
		try:
			print "\nSelect an address:"
			select = int(raw_input("> "))
			break
		except:
			print "Please enter a valid address number"
			pass

	selected_address = addresses[select]
	print "\n%s\n" % selected_address
	print "[0] blockchain.info"
	print "[1] Make a payment"
	print "[2] Select another address"
	
	return selected_address
	

def pubkey(address, keydict):
	selected_pubkey = keydict[address][2]
	return selected_pubkey
	
	
def privkey(address, keydict):
	selected_privkey = keydict[address][0]
	return selected_privkey	
	
	
def make_a_payment(address, selected_privkey):
	print "\nPlease enter the recipient's address."
	recipient = raw_input("> ")
	print "\nHow much would you like to send (in BTC)?"
 	amount = raw_input("> ")
	h = history(address)
	outs = [{'value': amount, 'address': recipient}]
	tx = mktx(h, outs)
	tx2 = sign(tx,0,selected_privkey)
	tx3 = sign(tx2,1,selected_privkey)
	print "First hash...\n"
	print tx
	print "\nSecond hash...\n"
	print tx2
	print "\nFinal hash...\n"
	print tx3
	pushtx(tx3)
		
	
keydict = key_dictionary()	
index_list = list_of_indices(keydict)
addresses = address_menu(keydict, index_list)
selected_address = address_options(addresses)
	
while True:
	print "\nSelect an option:"
	option = raw_input("> ")
	
	if "0" in option:
		url = "https://blockchain.info/address/%s" % selected_address
		webbrowser.open_new_tab(url)
		time.sleep(1.5)
		pass
	elif "1" in option:
		selected_privkey = privkey(selected_address, keydict)
		unspent_values_list = list_unspent_values(selected_address)
		make_a_payment(selected_address, selected_privkey)
		pass
	elif "2" in option:
		make_a_payment
		while True:
			try:
				keydict = key_dictionary()	
				index_list = list_of_indices(keydict)
				addresses = address_menu(keydict, index_list)
				selected_address = address_options(addresses)
				break
			except:
				print "\n\nPlease enter a valid address number"
				pass
				
	else:
		print "\nPlease enter a valid option number\n"
		print "[0] blockchain.info"
		print "[1] Make a payment"
		print "[2] Select another address"
		pass
		
		

	
