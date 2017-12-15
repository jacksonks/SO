#!/usr/bin/env python

import thread
import time, random
import threading
 
class BancoDados:
   contLeitor = 0
   mutex      = threading.Semaphore(1)
   bd         = threading.Semaphore(1)

   def acquireReadLock(self):
      global contLeitor
      self.mutex.acquire()
      self.contLeitor += 1

      # E o primeiro leitor?
      if self.contLeitor == 1:
         self.bd.acquire()

      self.mutex.release()

   def releaseReadLock(self):
      global contLeitor
      self.mutex.acquire()
      self.contLeitor -= 1

      # E o ultimo leitor?
      if self.contLeitor == 0:
         self.bd.release()

      self.mutex.release()

   def acquireWriteLock(self):
      self.bd.acquire()

   def releaseWriteLock(self):
      self.bd.release()

bd = BancoDados()

def escritor(e):
   while True:
      time.sleep(random.randint(1, 5))
      bd.acquireWriteLock()
      print "Escritor %i - escrevendo..." %e
      time.sleep(random.randint(1, 5))
      bd.releaseWriteLock()
      print "Escritor %i - parou de escrever." %e

def leitor(l):
   while True:
      time.sleep(random.randint(1, 10))
      bd.acquireReadLock()
      print "Leitor %i - lendo..." %l
      time.sleep(random.randint(1, 5))
      bd.releaseReadLock()
      print "Leitor %i - parou de ler." %l

for i in range(2):
   print "Escritor", i
   thread.start_new_thread(escritor, tuple([i]))
for i in range(3):
   print "Leitor", i
   thread.start_new_thread(leitor, tuple([i]))

while 1: pass
