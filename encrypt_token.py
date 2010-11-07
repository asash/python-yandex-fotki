import sys, copy

#some magic
#see http://habrahabr.ru/blogs/firefox/83710/
if __name__ == '__main__':
  if len(sys.argv) != 3 : print "usage: python %s <public-key> <text>" % sys.argv[0]; sys.exit()
  NSTR,ESTR = sys.argv[1].split("#")
  DATA_ARR = [ord(x) for x in sys.argv[2]]
  N,E,STEP_SIZE = int(NSTR,16),int(ESTR,16), len(NSTR)/2-1
  
  prev_crypted = [0]*STEP_SIZE
  
  hex_out = ""
  for i in range(0,(len(DATA_ARR)-1)/STEP_SIZE+1):
    tmp = DATA_ARR[i*STEP_SIZE:(i+1)*STEP_SIZE]
    tmp = [tmp[i] ^ prev_crypted[i] for i in range(0,len(tmp))]
    tmp.reverse()
    plain = 0
    for x in range(0,len(tmp)): plain+= tmp[x]*pow(256, x, N)
    hex_result = "%x" % pow(plain,E,N)
    hex_result = "".join(['0']*( len(NSTR)- len(hex_result))) + hex_result

    for x in range(0,min(len(hex_result),len(prev_crypted)*2),2):
      prev_crypted[x/2] = int(hex_result[x:x+2],16)
      
    hex_out += ("0" if len(tmp) < 16 else "") + ("%x" % len(tmp)) + "00" # current size
    ks = len(NSTR)/2
    hex_out += ("0" if ks < 16 else "") + ("%x" % ks) + "00" # key size
    hex_out += hex_result

  print hex_out.decode("hex").encode("base64").replace("\n","")
