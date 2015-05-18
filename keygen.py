from bitcoin import *
import webbrowser, time, os

directory = '/home/jack/bitcoin/keys' # CHANGE THIS!

while True:
	
	passphrase = raw_input("""
Create a passphrase or press enter to
generate a random key:\n> """)

# 256-bit private key:

	if passphrase == "":
			priv_256 = random_key()
	else:
			priv_256 = sha256(passphrase)

	print "\n256-bit private key:\n%s" % priv_256

# Wallet interchangable format (WIF) private key:
	priv_wif = encode_privkey(priv_256, 'wif')
	print """\nWallet interchangable format (WIF) private key:
%s""" % priv_wif

# 512-bit public key:
	pub = privkey_to_pubkey(priv_256)
	print "\n512-bit public key:\n%s" % pub

# 160-bit public key hash:
	h160 = hash160(pub.decode('hex'))
	print "\nHash160:\n%s" % h160

# Address:
	addr = hex_to_b58check(h160)
	print "\nAddress:\n%s (send money to this!)" % addr
	h = history(addr)

	if h == []:
			pass
	else:
			print "\nWARNING! This address has been used previously."

	url = "https://blockchain.info/address/%s" % addr
	webbrowser.open_new_tab(url)
   
	os.chdir(directory)
	new_file = '%s.txt' % addr

	f = open(new_file,'w')
	f.write("""%s %s %s %s""" % (priv_256, priv_wif, pub, h160))
	f.close()
	print "\n", ("-" * 55)
	print "File saved to %s as:\n%s" % (directory, new_file)
	print ("-" * 55), "\n"
	time.sleep(1.5)
