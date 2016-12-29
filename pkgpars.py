#!/usr/bin/env python
#-*- coding: utf-8 -*-



# Kutuphaneler import ediliyor
from pisi.db.filesdb import FilesDB
import re
import sys

# files_db sinifi ornekleniyor
files_db = FilesDB()
dosyalar = files_db.search_file(".pc")

#listeler tanımlanıyor-----------------------------------------
dep_list = []
dep_list_duzenli = []
dep_tam_list = []
bulunanlar = []
sirala = []

#kümeler tanımlanıyor------------------------------------------
piside_nedir = {}
version = {}

#dosya okunuyor------------------------------------------------

pkg_dep = sys.argv[1]
pkg_dep_oku = open(pkg_dep,"r")
parcala = pkg_dep_oku.readlines()
pkg_dep_oku.close()

#fonksiyonlar tanımlanıyor-------------------------------------

def duzenle():
    # Bu fonksiyon .pc dosyasını işlenebilir hale getirir
    for i in parcala:
        if re.match("Requires",i):
            dep_list.append(i.split(":")[1].strip().strip("\n"))
    for i in dep_list:
        if "," in i:
            i = i.replace(","," ")
        for j in i.split(" "):
            dep_list_duzenli.append(j)
        
def version_ulas():
    # Bu fonksiyon version değerlerine ulaşır
    while "" in dep_list_duzenli:
        for i in dep_list_duzenli:
            if i == "":
                dep_list_duzenli.pop(dep_list_duzenli.index(i))
    for i in dep_list_duzenli:
        if re.match(">=",i) or re.match("<=",i) or re.match("=",i):
            if i == (">="):
                version[dep_list_duzenli[dep_list_duzenli.index(i) - 1]] = "versionFrom=\"%s\"" % dep_list_duzenli[dep_list_duzenli.index(i) + 1]
                dep_list_duzenli.pop(dep_list_duzenli.index(i))
            elif i == ("<="):
                version[dep_list_duzenli[dep_list_duzenli.index(i) - 1]] = "version=\"%s\"" % dep_list_duzenli[dep_list_duzenli.index(i) + 1]
                dep_list_duzenli.pop(dep_list_duzenli.index(i))
            elif i == ("="):
                version[dep_list_duzenli[dep_list_duzenli.index(i) - 1]] = "version=\"%s\"" % dep_list_duzenli[dep_list_duzenli.index(i) + 1]
                dep_list_duzenli.pop(dep_list_duzenli.index(i))
        else:
            if (">=") in i:
                version[i.split(">=")[0]] = "versionFrom=\"%s\"" % i.split(">=")[1]
            
            elif ("<=") in i:
                version[i.split("<=")[0]] = "version=\"%s\"" % i.split("<=")[1]
                
            elif ("=") in i:
                version[i.split("=")[0]] = "version=\"%s\"" % i.split("=")[1]
            
            
            
def bag_ulas():
    # Bu fonksiyon bağımlılıkların hepsini sıralamak için bir listede tutar
    for i in dep_list_duzenli:
        if i != ("" or ">=" or "<=" or "="):
            if len(i) != 0 and re.match("[a-zA-Z]",i):
                if (">=") in i:
                    if i.split(">=")[0] not in dep_tam_list:
                        dep_tam_list.append(i.split(">=")[0])
                
                elif ("<=") in i:
                    if i.split("<=")[0] not in dep_tam_list:
                        dep_tam_list.append(i.split("<=")[0])
            
                elif ("=") in i:
                    if i.split("=")[0] not in dep_tam_list:
                        dep_tam_list.append(i.split("=")[0])
                else:
                    if i not in dep_tam_list:
                        dep_tam_list.append(i.split("=")[0])
def bag_list(): 
    # Bu fonksiyon bağımlılıkları listeler
    print "-----Bağımlılıklar Listeleniyor-----"

    for i in dep_tam_list:
        print i
        

def dizin_list():
    
    #Bu fonksiyon bağımlılıkların bulunduğu dizinleri listeler
    print "-----Bağımlılıkların bulunduğu dizinler listeleniyor-----"

    for i in dep_tam_list:
            for j in dosyalar:
                for t in j:
                    for k in t:
                        if k.endswith(("/" + i + ".pc")):
                            print i+ "-"*(30 - len(i)) +"> " + j[0] + " <" + "-"*(40 - len(j[0])) + "> "  + k
                            bulunanlar.append(i)
                            piside_nedir[i] = j[0]


def bulunamayan_list():
    # Bu fonksiyon dizinleri bulunamayan bağımlılıkları listeler
    print "-----Bulunamayanlar Listeleniyor-----"

    bulunamayanlar = set(dep_tam_list) - set(bulunanlar)
    if len(bulunamayanlar) == 0:
        print "bulunamayan yok"
    else:
        for i in bulunamayanlar:
            print i

  
def pspec_list():
    # Bu fonksiyon pspec.xml için gerekli taglar ile listeleme yapar
    print "-----pspec.xml için listeleniyor-----"

    for i in bulunanlar:
        if i in version.keys():
            a = "             <Dependency %s>%s</Dependency>" % (version[i],piside_nedir[i])
            if a not in sirala:
                sirala.append(a)
        else:
            a = "             <Dependency>%s</Dependency>" % (piside_nedir[i])
            if a not in sirala:
                sirala.append(a)
    sirala.sort()

    for i in sirala:
        print i


def calistir():
    # Bu fonksiyon diğer fonksiyonları sırası ile çalıştırır.
    duzenle()
    version_ulas()
    bag_ulas()
    bag_list()
    print ""
    dizin_list()
    print ""
    bulunamayan_list()
    print ""
    pspec_list()
    print ""


calistir()
