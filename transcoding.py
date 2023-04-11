import chardet

def judge(data):
    return chardet.detect(data)["encoding"]

def error(e,q=1):
    exit(0)

def trans(path):
    data = open(path, "rb").read()
    coding = judge(data)
    if coding == "GB2312":
        coding = "GBK"
    try:
        arr = [i.rstrip() for i in data.decode(coding).split("\n")]
        if len(arr) == 1:
            return [i for i in arr[0].split("\r")]
        return arr
    except Exception as e:
        print(e)
        error("[!] 无法使用此文本,请使用utf8编码的文本")
