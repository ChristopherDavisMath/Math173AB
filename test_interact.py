import ipywidgets as widgets
from ipywidgets import interact, interactive, fixed, interact_manual
import string
from string import ascii_lowercase, ascii_uppercase
from random import shuffle
from random import choice
from itertools import izip
# izip is used to turn two lists into a dictionary.  One list is the inputs, the other list is the outputs.
# presumably the two lists need to be the same length for this to work.

# letterset records the letters a-zA-Z
letterset = frozenset(string.ascii_letters)

# letterfreq lists the letters a-z, listed in decreasing order of frequency, as given in HPS.
letterfreq = list("etaonrishdlfcmugypwbvkxjqz")
letterprops = [['e','.131'], ['t','.105'], ['a','.082'], ['o', '.080'], ['n', '.071'], ['r','.068'], ['i','.064'], ['s','.061'],['h', '.053'],['d','.038'],['l','.034'],['f','.029'],['c','.028'],['m','.025'],['u','.025'],['g','.020'],['y','.020'],['p','.020'],['w','.015'],['b','.014'],['v','.009'],['k','.004'],['x','.002'],['j','.001'],['q','.001'],['z','.001']]

englishdictionary = {}
for pair in letterprops:
    englishdictionary[pair[0].upper()] = float(pair[1])

# this function removes all punctuation and spaces from X, and makes all the letters lowercase.
def onlyletters(X):
    return filter(letterset.__contains__, X).lower()

# this function counts substrings of the string X of length n.  It returns a dictionary whose keys are the
# substrings which occur and whose values are the number of times they occur.
def countsubstrings(X,n):
    subdict = {}
    for i in range(0,len(X)-n+1):
        if X[i:i+n] in subdict:
            subdict[X[i:i+n]] += 1
        else:
            subdict[X[i:i+n]] = 1
    return subdict

def countletters(X):
    return countsubstrings(X,1)

def makeplot(Y):
      import numpy
      import matplotlib.pyplot as plt
      Y = Y.upper()
      listholder = []
      for i in range(0,26):
          listholder.append(i+.5)
      bar_centers = numpy.array(listholder)
      fig, ax1 = plt.subplots()
      cipherfreq = countsubstrings(Y,1)
      for ch in letterset:
         if ch.isupper() and ch not in cipherfreq:
            cipherfreq[ch] = 0
      totalchars = len(Y)
      heightlist = []
      ticklabels = []
      # The +.001 is just a hack to prevent the fact that if Z = 0, then the plot rescaled to take up 25 units, not 26.
      for i in range(ord('A'),ord('Z')+1):
         heightlist.append((100*cipherfreq[chr(i)]/totalchars)+.001)
         ticklabels.append(chr(i))

      data = numpy.array(heightlist)

      # Plot
      ax1.bar(bar_centers, data, 
              width=1.0, align='center', color='blue', ecolor='black')
      ax1.set_ylabel('% frequency in the text')

      # Label ticks on x axis
      ax1.set_xticks(bar_centers)
      ax1.set_xticklabels(ticklabels)
      plt.show()


def compareplots(Y,shift_amount):
      # This was adapted from code found at http://www.packtpub.com/article/plotting-data-sage
      import numpy
      import matplotlib.pyplot as plt
      data = numpy.array([8.15, 1.44, 2.76, 3.79,13.11, 2.92, 1.99, 5.26, 6.35, .13, .42, 3.39, 2.54, 7.1, 8, 1.98, .12, 6.83, 6.10, 10.47, 2.46, .92, 1.54, .17, 1.98, .08])
      listholder = []
      for i in range(0,26):
          listholder.append(i+.5)
      bar_centers = numpy.array(listholder)

      # Plot
      fig, (ax0, ax1) = plt.subplots(ncols=2, sharex=True,figsize=(12,3))
      ax0.bar(bar_centers, data, 
              width=1.0, align='center', color='orange', ecolor='black')
      ax0.set_ylabel('% frequency in English')

      # Label ticks on x axis
      ax0.set_xticks(bar_centers)
      ax0.set_xticklabels(['a', 'b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'])

      cipherfreq = countsubstrings(Y,1)
      for ch in letterset:
         if ch.isupper() and ch not in cipherfreq:
            cipherfreq[ch] = 0
      totalchars = len(Y)
      heightlist = []
      ticklabels = []
      # The +.001 is just a hack to prevent the fact that if Z = 0, then the plot rescaled to take up 25 units, not 26.
      for i in range(ord('A'),ord('Z')+1):
         heightlist.append((100*cipherfreq[chr(i)]/totalchars)+.001)
         ticklabels.append(chr(i))

      data = numpy.array(heightlist)

      # Plot
      ax1.bar(bar_centers, data, 
              width=1.0, align='center', color='blue', ecolor='black')
      ax1.set_ylabel('% frequency in the ciphertext')

      # Label ticks on x axis
      ax1.set_xticks(bar_centers)
      ax1.set_xticklabels(ticklabels)
      plt.show()

def shift_encrypt(plaintext,amt):
    outlist = ascii_lowercase[amt:] + ascii_lowercase[:amt]
    plaintext = plaintext.lower()
    print plaintext
    Y = plaintext.translate(string.maketrans(ascii_lowercase,outlist)).upper()
    print Y
    #compareplots(Y,amt);
    return None

def shift_decrypt(ciphertext,amt):
    outlist = ascii_uppercase[amt:] + ascii_uppercase[:amt]
    ciphertext = onlyletters(ciphertext).upper()
    Y = ciphertext.translate(string.maketrans(ascii_uppercase,outlist))
    return Y

def shift_encrypt2(plaintext,amt):
    outlist = ascii_lowercase[amt:] + ascii_lowercase[:amt]
    plaintext = onlyletters(plaintext)
    print plaintext
    Y = plaintext.translate(string.maketrans(ascii_lowercase,outlist)).upper()
    print Y
    #compareplots(Y,amt);
    
def break_shift(ciphertext,amt):
    outlist = ascii_uppercase[amt:] + ascii_uppercase[:amt]
    ciphertext = onlyletters(ciphertext).upper()
    print ciphertext
    Y = ciphertext.translate(string.maketrans(ascii_uppercase,outlist)).lower()
    print Y
    compareplots(Y.upper(),amt);

def shift_encrypt_interact(x):
    mywidget=widgets.Dropdown(options=range(-26,27),value=0,description='Key:',disabled=False)
    interact(shift_encrypt,plaintext=fixed(x),amt=mywidget);
    
def shift_encrypt_interact2(x):
    mywidget=widgets.Dropdown(options=range(-26,27),value=0,description='Key:',disabled=False)
    interact(shift_encrypt2,plaintext=fixed(x),amt=mywidget);
    
def break_shift_interact(x):
    mywidget=widgets.Dropdown(options=range(-26,27),value=0,description='Key:',disabled=False)
    interact(break_shift,ciphertext=fixed(x),amt=mywidget);
    
# this function returns a dictionary which describes the encryption
# for a substitution cipher.
# for example, if the dictionary is called dict, and we want to know
# how to encrypt the letter "c", we can evaluate dict['c'].
def subcipherdict():
   alph = string.ascii_lowercase
   beta = list(alph)
   shuffle(beta)
   outputdict = dict(izip(alph, beta))
   return outputdict

#this function encrypts the string X using a randomly chosen dict from subcipherdict().
def subencrypt(X):
   X = onlyletters(X)
   subdict = subcipherdict()
   output = ''.join(subdict[ch] for ch in X)
   return output.upper()

#n is the length of the string
def randomletters(n):
    letters = list(string.ascii_uppercase)
    st = ''
    while len(st) < n:
        st = st + choice(letters)
    return st
    