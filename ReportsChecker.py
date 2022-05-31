import glob, json, hashlib, copy
#Simple translations.
conclusion = "Під час створення висновку сталася помилка."
nofilesatall = "Немає жодних файлів."
filename = "Звіт"
errornoreportfile = "Помилка! Не можу знайти файл звіту."
noerrorsfound = "Помилки не знайдено. Файли цілі."
hashiswrong = "Помилка Хеш файла {} не збігається. Файл пошкоджено."
filenotfound = "Помилка! Файл {} не знайдений."
filemustnotexist = "Помилка! Файл {} існує, проте не має існувати відповідно до звіту."
#Result translation.
result = "Результат"
hashiswrongfiles = "Кількість пошкождених файлів: {}."
filenotfoundfiles = "Кількість відсутніх файлів: {}."
filemustnotexistfiles = "Кількість файлів, яких не має бути: {}."
totalfilesinreport = "Усі файли в рапорті: {}."
conclusiontext = "Висновок: {}."
conclusionallcorrupted = "Усі файли пошкождено."
conclusionsomecorrupted = "Деякі файли пошкоджено."
conclusionsomemustnotexistsomenotexist = "Деякі файли присутні, деякі відсутні."
conclusionsomefilesnotexist = "Є відсутні файли."
conclusionsomefilesmustnotexist = "Є файли, яких не має бути."
conclusionallfilescomplete = "Всі файли цілі й присутні."

filenotfoundcounter = 0;
filemustnotexistcounter = 0;
hashiswrongcounter = 0;

reportfile = filename + ".txt"
autoreportfile = "autoreport.json"
autoreportfile_check = filename + "-check.json"
included_files = glob.glob("**/*.*", recursive=True)
#if reportfile in included_files:
#	included_files.remove(reportfile)
if autoreportfile in included_files:
	included_files.remove(autoreportfile)
if "/" in __file__:
	if __file__.rsplit('/', 1)[1]in included_files:
		included_files.remove(__file__.rsplit('/', 1)[1])
else:
	if __file__ in included_files:
		included_files.remove(__file__)
if len(included_files)==0:
	print(nofilesatall)
	input(">>>")
	exit()
try:
	autoreportfile = open(autoreportfile, "r")
	autoreport = json.load(autoreportfile)
	autoreportfile.close()
except(FileNotFoundError):
	print(errornoreportfile)
	input(">>>")
	exit()
#if(autoreport == jsondata):
#	print(noerrorsfound)
#else:
#	print(filescanbecorrupted)
autoreportclone = copy.deepcopy(autoreport)
for i in included_files:
	if not i in autoreport:
		print(filemustnotexist.format(i))
		filemustnotexistcounter += 1;
		continue
	calculatedfile = open(i, "rb")
	md5_hash = hashlib.md5()
	sha512_hash = hashlib.sha512()
	blake2b_hash = hashlib.blake2b()
	chunk = 0
	for chunk in iter(lambda: calculatedfile.read(4096), b""):
		md5_hash.update(chunk)
		sha512_hash.update(chunk)
		blake2b_hash.update(chunk)
	if md5_hash.hexdigest()!=autoreport[i]["md5_hash"] or sha512_hash.hexdigest()!=autoreport[i]["sha512_hash"] or blake2b_hash.hexdigest()!=autoreport[i]["blake2b_hash"]:
		print(hashiswrong.format(i));
		hashiswrongcounter += 1;
	autoreportclone.pop(i)
	calculatedfile.close()
if len(autoreportclone)>=0:
	for i in autoreportclone.keys():
		print(filenotfound.format(i))
		filenotfoundcounter += 1;
totalfilesinreportnumber = len(autoreport.keys())
if hashiswrongcounter==totalfilesinreportnumber:
	conclusion = conclusionallcorrupted
elif hashiswrongcounter>0:
	conclusion = conclusionsomecorrupted
elif filenotfoundcounter>0 and filemustnotexistcounter>0:
	conclusion = conclusionsomemustnotexistsomenotexist
elif filenotfoundcounter>0:
	conclusion = conclusionsomefilesnotexist
elif filemustnotexistcounter>0:
	conclusion = conclusionsomefilesmustnotexist
else:
	conclusion = conclusionallfilescomplete
print(result)
print("=:=:=:=:=:=:=:=")
print(hashiswrongfiles.format(hashiswrongcounter))
print(filenotfoundfiles.format(filenotfoundcounter))
print(filemustnotexistfiles.format(filemustnotexistcounter))
print("=:=:=:=:=:=:=:=")
print(totalfilesinreport.format(totalfilesinreportnumber))
print(conclusiontext.format(conclusion))
input(">>>")
