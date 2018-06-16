import os
import subprocess
import sys

def help():
    """
Usage:
    test_func
    download_ts
    download
    ts2mp4
    download_mp4_from_ts
    """
    print(help.__doc__)

def test_func():
    print("test_func succesfull.")

def get_stdout(cmd):
  return subprocess.Popen(
      cmd, stdout=subprocess.PIPE,
      shell=True).communicate()[0]

def download_ts(list_dir, tag_name):
    """

Usage: download_ts LIST_DIR TAG_NAME
Example:
    $ ls
    result/ list/ this.py
    $ ls result/
    $ ls list/
    foo bar
    $ cat list/foo
    https://hoge.com/1.ts
    https://hoge.com/2.ts
    https://hoge.com/3.ts

    >>> download_ts("list", "foo")

    $ ls result/
    foo
    $ ls result/foo
    foo_1.ts foo_2.ts foo_3.ts
    """
    if not os.path.exists(list_dir + "/" + tag_name):
        print("** ERROR **")
        print("try:\n  $ cat > " + list_dir + "/" + tag_name)
        exit(1)
    if not os.path.exists("result"):
        os.mkdir("result")
        print("$ mkdir result")
    if not os.path.exists("result/" + tag_name):
        os.mkdir("result/" + tag_name)
        print("$ mkdir result/" + tag_name)

    f = open(list_dir + "/" + tag_name, "r")
    lines = f.readlines()
    f.close()
    i = 1
    for url in lines:
        url = url.split()[0]
        if "http" in url:
            os.system("curl \"" + url + "\" -o result/" + tag_name + "/" + tag_name + "_" + str(i) + ".ts")
            i += 1

def download(list_path):
    """
$ ls
list/ this.py
$ ls list/
mp4_list
$ cat list/mp4_list
https://hoge.com/fuga.mp4 movie_01.mp4
https://foo.com/bar.mp4 great.png dir1 dir2
https://abc.com/xyz.mp4 this_is_file_name.jpeg

>>> download_mp4("list/mp4_list")

$ ls
list/ result/ this.py
$ ls result/
mp4_list/
$ ls result/mp4_list/
dir1/ dir2/ movie_01.mp4 this_is_file_name.mp4
$ ls dir1/
great.png
$ ls dir2/
great.png
    """
    list_name = list_path.split("/")[-1]
    if not os.path.exists(list_path):
        print("** ERROR **")
        print("try:\n  $ cat > " + list_path)
        exit(1)
    if not os.path.exists("result"):
        os.mkdir("result")
        print("$ mkdir result")
    if not os.path.exists("result/" + list_name):
        os.mkdir("result/" + list_name)
        print("$ mkdir result/" + list_name)

    lines = open(list_path).readlines()
    for line in lines:
        line = line.replace("\n", "")
        print("line:", line) #d
        splited_line = line.split(" ")
        url = splited_line[0]
        file_name = splited_line[1]
        if len(splited_line) == 2:
            dst_path = "result/" + list_name + "/" + file_name
            print("url:", url) #d
            print("dst_path:", dst_path) #d
            os.system("curl \"" + url + "\" -o " + dst_path)
        else:
            dirs = splited_line[2:]
            for d in dirs:
                d_path = "result/" + list_name + "/" + d
                if not os.path.exists(d_path):
                    os.mkdir(d_path)
                    print("$ mkdir " + d_path)
                dst_path = d_path + "/" + file_name
                i = 2
                while os.path.exists(dst_path):
                    dst_path = format_replace(dst_path, "_" + str(i))
                    i += 1
                print("url:", url) #d
                print("dst_path:", dst_path) #d
                os.system("curl \"" + url + "\" -o " + dst_path)

def format_replace(url, s):
    """
>>> format_replace("/path/to/hoge.mp4", "_2.mp4")

/path/to/hoge.mp4 -> /path/to/hoge_2.mp4
    """
    url = url.replace(".mp4", s + ".mp4")
    url = url.replace(".jpeg", s + ".jpeg")
    url = url.replace(".jpg", s + ".jpg")
    url = url.replace(".png", s + ".png")
    url = url.replace(".m3u8", s + ".m3u8")
    url = url.replace(".mpeg", s + ".mpeg")
    url = url.replace(".mpg", s + ".mpg")
    return url

def ts2mp4(tag_name):
    """
Usage: ts2mp4 TAG_NAME
Example:
    $ ls result/
    foo/
    $ ls result/foo/
    foo_1.ts foo_2.ts foo_3.ts
    $ ts2mp4 foo
    $ ls result/
    foo.mp4
    """
    ls = "exa --group-directories-first "
    res = get_stdout(ls + "result/" + tag_name + "/")
    res = res.decode("utf-8")
    res = res.split("\n")
    pwd = os.getcwd()
    for i in range(len(res)):
        line = res[i]
        if line == "":
            continue
        line = "file " + pwd + "/result/" + tag_name + "/" + line
        res[i] = line
    os.system("rm -rf ts_files.tmp")
    f = open("ts_files.tmp", "a")
    for x in res:
        f.write(x + "\n")
    f.close()
    os.system("ffmpeg -f concat -safe 0 -i ts_files.tmp -c copy result/" + tag_name + ".mp4")
    os.system("rm -rf result/" + tag_name)

def download_mp4_from_ts(list_dir, tag_name):
    download_ts(list_dir, tag_name)
    ts2mp4(tag_name)

def create_args(argv):
    args = ""
    for arg in argv[2:]:
        args += "\"" + arg + "\", "
    return args[:-2]

if __name__ == '__main__':
    if len(sys.argv) == 1 or sys.argv[1] in ("-h", "--help"):
        print("Usage: python " + sys.argv[0] + " FUNCTION_NAME [ARG...]")
        exit(0)
    elif len(sys.argv) > 2 and sys.argv[2] in ("-h", "--help"):
        cmd = "print(" + sys.argv[1] + ".__doc__)"
        exec(cmd)
        exit(0)
    cmd = sys.argv[1] + "(" + create_args(sys.argv) + ")"
    exec(cmd)
