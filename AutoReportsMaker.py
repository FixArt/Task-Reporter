import glob, json, hashlib

def intersperse(lst, item):
	result = [item] * (len(lst) * 2 - 1)
	result[0::2] = lst
	return result

filename = "Звіт"
filecontent = "Я - {} з {}, звітую про виконання завдання. До завдання прикріплений автоматично згенерований комп'ютерний звіт, який дозволяє перевірити цілісність прикріплених файлів."
allconnectedfiles = "\nУсі прикріплені файли:\n"
name = "приклад"
myclass = "класу-прикладу"
reportfile = filename + ".txt"
autoreportfile = "autoreport.json"
included_files = glob.glob("**/*.*", recursive=True)
if reportfile in included_files:
	included_files.remove(reportfile)
if autoreportfile in included_files:
	included_files.remove(autoreportfile)
if "/" in __file__:
	if __file__.rsplit('/', 1)[1] in included_files:
		included_files.remove(__file__.rsplit('/', 1)[1])
else:
	if __file__ in included_files:
		included_files.remove(__file__)
lines_to_type = [filecontent.format(name, myclass), allconnectedfiles] + intersperse(included_files, "\n")
myreport = open(reportfile, "w")
myreport.writelines(lines_to_type)
myreport.close()
included_files.append(reportfile)
autoreport = open(autoreportfile, "w")
#{"Test.py":["md5_hash":"1342000kg034g", "sha512_hash":"grog3o4g53g339g5ng3", "blake2b_hash":"gi54mg95gng04g59gb0g4"]}
jsondata = {}
for i in included_files:
	calculatedfile = open(i, "rb")
	md5_hash = hashlib.md5()
	sha512_hash = hashlib.sha512()
	blake2b_hash = hashlib.blake2b()
	chunk = 0
	for chunk in iter(lambda: calculatedfile.read(4096), b""):
		md5_hash.update(chunk)
		sha512_hash.update(chunk)
		blake2b_hash.update(chunk)
	jsondata[i] = {"md5_hash": md5_hash.hexdigest(), "sha512_hash": sha512_hash.hexdigest(), "blake2b_hash": blake2b_hash.hexdigest()}
json.dump(jsondata, autoreport, ensure_ascii=False)
autoreport.close()
