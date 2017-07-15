#Based on punk.py
#Version 1, 15 Oct. 2014
#Help on silencing rm error from http://stackoverflow.com/questions/10247472/how-to-prevent-rm-from-reporting-that-a-file-was-not-found
import os
import sys
import time
running = True
now = time.strftime("%Y.%m.%d.%H.%M.%S.%f.%z", time.gmtime())
while running == True:
	action = raw_input('action (save/restore/nothing)? ');

	if action.lower().strip() == 'nothing' or action.lower().strip() == 'quit' or action.lower().strip() == 'close':
		sys.exit()

	if action.lower().strip() == 'save':
		inf = raw_input('item to save? (<15gb) ');
		def filo():
			cfgo = os.path.expanduser("~/.pbzl")
			ad = ''
			try:
				ak = open(cfgo,'rb')
				ad = ak.read()
				ak.close()
			except:
				pass
			if len(ad) < 1:
				ad = raw_input('confirm output directory? (have 30gb free space for it there) ');
				ad = os.path.expanduser(ad)
				os.system('rm ~/.pbzl 2> /dev/null')
				ax = open(cfgo,'wb')
				ax.write(ad)
				ax.close()
			opr = ad+"/.tmp.Packed-"+now
			opd = ad+"/Packed-"+now
			print 'Outputting to: '+opd
			return opr
		def enci():
			cfgp = os.path.expanduser("~/.pbz")
			ad = ''
			try:
				ak = open(cfgp,'rb')
				ad = ak.read()
				ak.close()
			except:
				pass
			if len(ad) < 1:
				ad = raw_input('confirm authkey? ');
				os.system('rm ~/.pbz 2> /dev/null')
				ax = open(cfgp,'wb')
				ax.write(ad)
				ax.close()
		def pack(of):
			os.system('hashdeep -c sha1 -r '+inf+' > '+inf+'/.Packed-'+now+'.AddedToPackedDirOnPack.pdx')
			os.system('cp '+inf+'/.Packed-'+now+'.AddedToPackedDirOnPack.pdx '+of+'.pdx')
			os.system('bzip2 '+of+'.pdx')
			os.system('tar -cvj --format pax -f '+of+'.pbz '+inf)
		def encrypt(of):
			os.system('gpg -c --cipher-algo AES256 --batch --passphrase-file ~/.pbz '+of+'.pbz')
			os.system('mv '+of+'.pbz.gpg '+of+'.pbze')
			os.system('rm '+of+'.pbz')
			os.system('gpg -c --cipher-algo AES256 --batch --passphrase-file ~/.pbz '+of+'.pdx.bz2')
			os.system('mv '+of+'.pdx.bz2.gpg '+of+'.pdxe')
			os.system('rm '+of+'.pdx.bz2')
		def finish():
			cfgo = os.path.expanduser("~/.pbzl")
			ak = open(cfgo,'rb')
			ad = ak.read()
			ak.close()
			os.system('mv '+ad+'/.tmp.Packed-'+now+'.pbze '+ad+'/Packed-'+now+'.pbze')
			os.system('mv '+ad+'/.tmp.Packed-'+now+'.pdxe '+ad+'/Packed-'+now+'.pdxe')
			
			print 'Done!'
			sys.exit()
		qp = raw_input("quick processing (encrypt with default key; output to default path) (y/n)? ")
		if qp.lower().strip() == 'yes' or qp.lower().strip() == 'y':
			of = filo()
			enci()
			pack(of)
			encrypt(of)
			finish()
		#od = raw_input('new output directory? (have 30gb free space for it there) ')
		od = ''
		#od = os.path.expanduser(od)
		cfgo = os.path.expanduser("~/.pbzl")
		os.system('rm ~/.pbzl 2> /dev/null')
		ax = open(cfgo,'wb')
		ax.write(od)
		ax.close()
		of = filo()
		enc = raw_input("encrypt / don't encrypt / replace existing key (y/n/r)? ")
		if enc.lower().strip() == 'replace' or enc.lower().strip() == 'r':
			#akn = raw_input('new authkey? ')
			akn = ''
			#akn = os.path.expanduser(akn)
			cfgkn = os.path.expanduser("~/.pbz")
			os.system('rm ~/.pbz 2> /dev/null')
			akx = open(cfgkn,'wb')
			akx.write(akn)
			akx.close()
			enci()
		if enc.lower().strip() == 'yes' or enc.lower().strip() == 'y':
			enci()
		pack(of)
		if enc.lower().strip() == 'yes' or enc.lower().strip() == 'y' or enc.lower().strip() == 'replace' or enc.lower().strip() == 'r':
			encrypt(of)
		finish()

# 	if action.lower().strip() == 'save':
# 		inf = raw_input('item to save? (<15gb) ');
# 		def filo():
# 			cfgo = os.path.expanduser("~/.pbzl")
# 			ad = ''
# 			try:
# 				ak = open(cfgo,'rb')
# 				ad = ak.read()
# 				ak.close()
# 			except:
# 				pass
# 			if len(ad) < 1:
# 				ad = raw_input('confirm output directory? (have 30gb free space for it there) ');
# 				ad = os.path.expanduser(ad)
# 				os.system('rm ~/.pbzl 2> /dev/null')
# 				ax = open(cfgo,'wb')
# 				ax.write(ad)
# 				ax.close()
# 			opr = ad+"/.tmp.Packed-"+now
# 			print 'Outputting to: '+opr
# 			return opr
# 		def enci():
# 			cfgp = os.path.expanduser("~/.pbz")
# 			ad = ''
# 			try:
# 				ak = open(cfgp,'rb')
# 				ad = ak.read()
# 				ak.close()
# 			except:
# 				pass
# 			if len(ad) < 1:
# 				ad = raw_input('confirm authkey? ');
# 				os.system('rm ~/.pbz 2> /dev/null')
# 				ax = open(cfgp,'wb')
# 				ax.write(ad)
# 				ax.close()
# 		def pack(of):
# 			os.system('hashdeep -c sha1 -r '+inf+' > '+inf+'/.tmp.Packed-'+now+'.AddedTo.tmp.PackedDirOnPack.pdx')
# 			os.system('cp '+inf+'/.tmp.Packed-'+now+'.AddedTo.tmp.PackedDirOnPack.pdx '+of+'.pdx')
# 			os.system('bzip2 '+of+'.pdx')
# 			os.system('tar -cvj --format pax -f '+of+'.pbz '+inf)
# 		def encrypt(of):
# 			os.system('gpg -c --cipher-algo AES256 --batch --passphrase-file ~/.pbz '+of+'.pbz')
# 			os.system('mv '+of+'.pbz.gpg '+of+'.pbze')
# 			os.system('rm '+of+'.pbz')
# 			os.system('gpg -c --cipher-algo AES256 --batch --passphrase-file ~/.pbz '+of+'.pdx.bz2')
# 			os.system('mv '+of+'.pdx.bz2.gpg '+of+'.pdxe')
# 			os.system('rm '+of+'.pdx.bz2')
# 		def finish():
# 			print 'Done!'
# 			sys.exit()
# 		qp = raw_input("quick processing (encrypt with default key; output to default path) (y/n)? ")
# 		if qp.lower().strip() == 'yes' or qp.lower().strip() == 'y':
# 			of = filo()
# 			enci()
# 			pack(of)
# 			encrypt(of)
# 			finish()
# 		#od = raw_input('new output directory? (have 30gb free space for it there) ')
# 		od = ''
# 		#od = os.path.expanduser(od)
# 		cfgo = os.path.expanduser("~/.pbzl")
# 		os.system('rm ~/.pbzl 2> /dev/null')
# 		ax = open(cfgo,'wb')
# 		ax.write(od)
# 		ax.close()
# 		of = filo()
# 		enc = raw_input("encrypt / don't encrypt / replace existing key (y/n/r)? ")
# 		if enc.lower().strip() == 'replace' or enc.lower().strip() == 'r':
# 			#akn = raw_input('new authkey? ')
# 			akn = ''
# 			#akn = os.path.expanduser(akn)
# 			cfgkn = os.path.expanduser("~/.pbz")
# 			os.system('rm ~/.pbz 2> /dev/null')
# 			akx = open(cfgkn,'wb')
# 			akx.write(akn)
# 			akx.close()
# 			enci()
# 		if enc.lower().strip() == 'yes' or enc.lower().strip() == 'y':
# 			enci()
# 		pack(of)
# 		if enc.lower().strip() == 'yes' or enc.lower().strip() == 'y' or enc.lower().strip() == 'replace' or enc.lower().strip() == 'r':
# 			encrypt(of)
# 		finish()

	if action.lower().strip() == 'restore':
		date = raw_input('date to restore? NOTE THAT THE INPUT FILES WILL BE REMOVED AFTER RESTORE! HAVE A BACKUP IN CASE THE RESTORE FAILS! ');
		encr = True
		try:
			ak = open('./Packed-'+date+'.pbze','rb')
			ak.close()
		except:
			try:
				ak = open('./Packed-'+date+'.pbz','rb')
				ak.close()
			except:
				print "Could not find specified date. Please make sure you have cded to the directory it's in."
				sys.exit()
			encr = False
		if encr:
			needsOtherKey = raw_input('Replace key? (y/n) ');
			if needsOtherKey.lower().strip() == 'yes' or needsOtherKey.lower().strip() == 'y':
				#akn = raw_input('new authkey? ')
				#akn = os.path.expanduser(akn)
				akn = ''
				cfgkn = os.path.expanduser("~/.pbz")
				os.system('rm ~/.pbz 2> /dev/null')
				akx = open(cfgkn,'wb')
				akx.write(akn)
				akx.close()
			print 'pbze extract'
			try:
				ak = open('./Packed-'+date+'.pdxe','rb')
				ak.close()
			except:
				print "Could not find BOMe."
				sys.exit()
			cfgp = os.path.expanduser("~/.pbz")
			ad = ''
			try:
				ak = open(cfgp,'rb')
				ad = ak.read()
				ak.close()
			except:
				pass
			if len(ad) < 1:
				ad = raw_input('authkey? ');
				os.system('rm ~/.pbz 2> /dev/null')
				cfgp = os.path.expanduser("~/.pbz")
				ax = open(cfgp,'wb')
				ax.write(ad)
				ax.close()
			os.system('mv ./Packed-'+date+'.pbze .tmp-'+date+'.gpg')
			os.system('gpg --batch --passphrase-file ~/.pbz ./.tmp-'+date+'.gpg')
			os.system('rm ./.tmp-'+date+'.gpg')
			os.system('mv ./Packed-'+date+'.pdxe .tmp-pdx-'+date+'.gpg')
			os.system('gpg --batch --passphrase-file ~/.pbz ./.tmp-pdx-'+date+'.gpg')
			os.system('rm ./.tmp-pdx-'+date+'.gpg')
			os.system('mv ./.tmp-'+date+' ./.tmp-'+date+'.tbz2')
			os.system('mv ./.tmp-pdx-'+date+' ./Packed-'+date+'.pdx.bz2')
		else:
			print 'pbz extract'
			os.system('mv ./Packed-'+date+'.pdx ./Packed-'+date+'.pdx.bz2')
			try:
				ak = open('./Packed-'+date+'.pdx','rb')
				ak.close()
			except:
				print "Could not find BOM."
				sys.exit()
		os.system('bunzip2 ./Packed-'+date+'.pdx.bz2')
		os.system('tar -xvf ./.tmp-'+date+'.tbz2')
		os.system('rm ./.tmp-'+date+'.tbz2')
		sys.exit()
	print "That wasn't a suggested input; I don't know what to do."