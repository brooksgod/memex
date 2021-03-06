import sys
import urllib2
import socket
import traceback
import grequests

def encode(url):
  return urllib2.quote(url).replace("/", "%2F")

def decode(url):
  return urllib2.unquote(url).replace("%2F", "/")

def validate_url(url):
    s = url[:4]
    if s == "http":
        return url
    else:
        url = "http://" + url
        return url

def download(inputfile, outputdir):
  actions = []
  with open(inputfile) as lines:
    for line in lines:
      try:
        url = line.strip("\n")
        url = validate_url(url)
        #handle = urllib2.urlopen(url)
        #src = handle.read()
        action = grequests.get(url)
        actions.append(action)
      except urllib2.HTTPError, e:
        print 'HTTPERROR=' + str(e.code) + "\t" + url
      except socket.timeout, e:
        print 'TIMEOUT=' + str(e) + "\t" + url
      except:
        traceback.print_exc()
        print 'EXCEPTION' + "\t" + url
        
  responses = grequests.map(actions)

  for res in responses:
    if not (res == None):
      src = res.text
      src = src.encode('utf-8')
      print "GOOD\t" + res.url
      encoded_url = encode(res.url)
      f = open(outputdir + "/" + encoded_url, "w")
      f.write(src)
      f.close()

def main(argv):
    if len(argv) != 2:
        print "Invalid arguments"
        print "python download.py inputfile outputdir"
        return
    download(argv[0], argv[1])

if __name__=="__main__":
    main(sys.argv[1:])
