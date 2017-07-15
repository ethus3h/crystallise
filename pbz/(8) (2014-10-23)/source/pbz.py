#Based on punk.py
#Version 8, 23 Oct. 2014
#Help from http://stackoverflow.com/questions/19602931/basic-http-file-downloading-and-saving-to-disk-in-python and https://docs.python.org/2/library/urllib.html
# www.timeapi.org/utc/now?format=%25Y.%25m.%25d.%25H.%25M.%25S.%25Z
#Help on silencing rm error from http://stackoverflow.com/questions/10247472/how-to-prevent-rm-from-reporting-that-a-file-was-not-found
import os
import sys
import time
import uuid
import urllib
running = True
pbzversion = '8'
now = time.strftime("%Y.%m.%d.%H.%M.%S.%f.%z", time.gmtime())+"-"+uuid.uuid4().hex
while running == True:
	action = raw_input('action (save/restore/nothing)? ');

	if action.lower().strip() == 'nothing' or action.lower().strip() == 'quit' or action.lower().strip() == 'close':
		sys.exit()

	if action.lower().strip() == 'save':
		ccgo = os.path.expanduser("~/.pbzc")
		ad = ''
		try:
			ak = open(ccgo,'rb')
			ad = ak.read()
			ak.close()
		except:
			pass
		if len(ad) < 1:
			ad = raw_input('Give a name / description to this computer: ');
			os.system('rm -v ~/.pbzc 2> /dev/null')
			ax = open(ccgo,'wb')
			ax.write(ad)
			ax.close()
		ccgo = os.path.expanduser("~/.pbziid")
		ad = ''
		try:
			ak = open(ccgo,'rb')
			ad = ak.read()
			ak.close()
		except:
			pass
		if len(ad) < 1:
			ad = uuid.uuid4().hex;
			print 'You have been assigned the following pbz installation ID: '+ad
			os.system('rm -v ~/.pbziid 2> /dev/null')
			ax = open(ccgo,'wb')
			ax.write(ad)
			ax.close()
		inf = raw_input('item to save? (Make sure you have maybe 4x the size of the item free space. If no leading / given will be assumed it is in ~): ');
		if not inf.startswith('/'):
			if not inf.startswith('~'):
				inf = '~/'+inf
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
				ad = raw_input('confirm output directory? (Make sure you have maybe 4x the size of the item free space.) ');
				ad = os.path.expanduser(ad)
				os.system('rm -v ~/.pbzl 2> /dev/null')
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
				os.system('rm -v ~/.pbz 2> /dev/null')
				ax = open(cfgp,'wb')
				ax.write(ad)
				ax.close()
		def pack(of):
			os.system('mkdir '+inf+'/.pbz-meta-'+now+'.AddedToPackedDirOnPack.pmb/')
			os.system('mkdir '+inf+'/.pbz-meta-'+now+'.AddedToPackedDirOnPack.pmb/.config-'+now+'.AddedToPackedDirOnPack.pcb/')
			timefile = urllib.URLopener()
			timefn = os.path.expanduser(inf).replace('\\','')+'/.pbz-meta-'+now+'.AddedToPackedDirOnPack.pmb/.Packed-'+now+'.AddedToPackedDirOnPack.ptd'
			try:
				timefile.retrieve("http://www.timeapi.org/utc/now?format=%25Y.%25m.%25d.%25H.%25M.%25S.%25Z", timefn)
			except:
				try:
					timefile.retrieve("http://www.timeapi.org/utc/now?format=%25Y.%25m.%25d.%25H.%25M.%25S.%25Z", timefn)
				except:
					tfl = open(timefn,'wb')
					tfl.write('Error retrieving time; attempt failed twice.')
					tfl.close()
			tfres = open(timefn,'rb')
			tfres.read()
			tfres.close()
			vfl = open(os.path.expanduser(inf).replace('\\','')+'/.pbz-meta-'+now+'.AddedToPackedDirOnPack.pmb/.Packed-'+now+'.AddedToPackedDirOnPack.pbzversion','wb')
			vfl.write(pbzversion)
			vfl.close()
			userpath = os.path.expanduser("~")
			os.system('hashdeep -o f -c sha1 -r '+inf+' > '+inf+'/.pbz-meta-'+now+'.AddedToPackedDirOnPack.pmb/.Packed-'+now+'.AddedToPackedDirOnPack.pdx')
			os.system('cp -v '+userpath+'/.pbz* '+inf+'/.pbz-meta-'+now+'.AddedToPackedDirOnPack.pmb/.config-'+now+'.AddedToPackedDirOnPack.pcb/ '+of+'.pdx')
			os.system('cp -rv '+inf+'/.pbz-meta-'+now+'.AddedToPackedDirOnPack.pmb/ '+of+'.pmb/')
			os.system('tar -cvj --format pax -f '+of+'.pmbz '+of+'.pmb/')
			os.system('cp -v '+inf+'/.pbz-meta-'+now+'.AddedToPackedDirOnPack.pmb/.Packed-'+now+'.AddedToPackedDirOnPack.pdx')
			os.system('bzip2 '+of+'.pdx')
			os.system('tar -cvj --format pax -f '+of+'.pbz '+inf)
		def encrypt(of):
			os.system('gpg --yes -c --cipher-algo AES256 --batch --passphrase-file ~/.pbz '+of+'.pbz')
			os.system('mv -v '+of+'.pbz.gpg '+of+'.pbze')
			os.system('rm -v '+of+'.pbz')
			os.system('gpg --yes -c --cipher-algo AES256 --batch --passphrase-file ~/.pbz '+of+'.pmbz')
			os.system('mv -v '+of+'.pmbz.gpg '+of+'.pmbze')
			os.system('rm -v '+of+'.pmbz')
			os.system('gpg --yes -c --cipher-algo AES256 --batch --passphrase-file ~/.pbz '+of+'.pdx.bz2')
			os.system('mv -v '+of+'.pdx.bz2.gpg '+of+'.pdxe')
			os.system('rm -v '+of+'.pdx.bz2')
		def finish():
			cfgo = os.path.expanduser("~/.pbzl")
			ak = open(cfgo,'rb')
			ad = ak.read()
			ak.close()
			os.system('mv -v '+ad+'/.tmp.Packed-'+now+'.pbze '+ad+'/Packed-'+now+'.pbze')
			os.system('mv -v '+ad+'/.tmp.Packed-'+now+'.pdxe '+ad+'/Packed-'+now+'.pdxe')
			
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
		os.system('rm -v ~/.pbzl 2> /dev/null')
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
			os.system('rm -v ~/.pbz 2> /dev/null')
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
				os.system('rm -v ~/.pbz 2> /dev/null')
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
			try:
				ak = open('./Packed-'+date+'.pmbze','rb')
				ak.close()
			except:
				print "Could not find pmbze."
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
				os.system('rm -v ~/.pbz 2> /dev/null')
				cfgp = os.path.expanduser("~/.pbz")
				ax = open(cfgp,'wb')
				ax.write(ad)
				ax.close()
			os.system('mv -v ./Packed-'+date+'.pbze .tmp-'+date+'.gpg')
			os.system('gpg --yes --batch --passphrase-file ~/.pbz ./.tmp-'+date+'.gpg')
			os.system('rm -v ./.tmp-'+date+'.gpg')
			os.system('mv -v ./Packed-'+date+'.pdxe .tmp-pdx-'+date+'.gpg')
			os.system('gpg --yes --batch --passphrase-file ~/.pbz ./.tmp-pdx-'+date+'.gpg')
			os.system('rm -v ./.tmp-pdx-'+date+'.gpg')
			os.system('mv -v ./.tmp-'+date+' ./.tmp-'+date+'.tbz2')
			os.system('mv -v ./.tmp-pdx-'+date+' ./Packed-'+date+'.pdx.bz2')
		else:
			print 'pbz extract'
			os.system('mv -v ./Packed-'+date+'.pdx ./Packed-'+date+'.pdx.bz2')
			try:
				ak = open('./Packed-'+date+'.pdx','rb')
				ak.close()
			except:
				print "Could not find BOM."
				sys.exit()
			try:
				ak = open('./Packed-'+date+'.pmbze','rb')
				ak.close()
			except:
				print "Could not find pmbze."
				sys.exit()
		os.system('bunzip2 ./Packed-'+date+'.pdx.bz2')
		os.system('tar -xvf ./.tmp-'+date+'.tbz2')
		time.sleep(1)
		os.system('rm -v ./.tmp-'+date+'.tbz2')
		sys.exit()
	print "That wasn't a suggested input; I don't know what to do."