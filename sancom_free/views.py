from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import IntegrityError
from django.contrib.auth.models import User
from account.models import File
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import Lan_appForm1, Excel_link
import openpyxl
import requests
from bs4 import BeautifulSoup
import sys
import wave
import numpy as np
import matplotlib.pyplot as plt
import random
import datetime
from django.utils.datastructures import MultiValueDictKeyError

#@login_required
class Lan_appView(TemplateView):
    def __init__(self):
        self.params = {
            'title':'日英中ビジネス文例',
            'message':'　',
            'form1':'',
            'item':'',
            'category':'',
            'japanese':'',
            'english':'',
            'esound':'',
            'chinese':'',
            'csound':'',
            'error':''
        }

    def get(self, request):
        file = File.objects.filter(owner=request.user).first()
        filename = file.filename1
        sheet = 'sheet1'
        excel = Excel_link(filename, sheet)
        excel_list = excel.getlist()
        form1 = Lan_appForm1(filename, sheet)
        form1.fields['choice1'].choices = excel_list[2]
        self.params['form1'] = form1
        if request.GET.get('item') != None:
            item = request.GET['item']
            category = request.GET['category'] 
            japanese = request.GET['japanese']
            english = request.GET['english']
            esound = request.GET['esound']
            chinese = request.GET['chinese']
            csound = request.GET['csound']
            self.params['item'] = item
            self.params['category'] = category
            self.params['japanese'] = japanese
            self.params['english'] = english
            self.params['esound'] = esound
            self.params['chinese'] = chinese
            self.params['csound'] = csound        
        return render(request, 'sancom_free/sancomcontents.html', self.params)

    def post(self, request):
        global item

        if 'start' in request.POST:
            file = File.objects.filter(owner=request.user).first()
            filename = file.filename1
            sheet = 'sheet1'
            excel = Excel_link(filename, sheet)
            excel_list = excel.getlist()
            verb_dic = excel_list[0]
            try:
                ch1 = request.POST['choice1']
            except MultiValueDictKeyError:
                self.params['error'] = '文例を選択してください。'
                return render(request, 'sancom_free/sancomcontents.html', self.params)
            item=ch1            
            self.params['item'] = item
            self.params['category'] = verb_dic[item]["category"]
            self.params['japanese'] = verb_dic[item]["japanese"]
            self.params['english'] = verb_dic[item]["english"]
            self.params['esound'] = "sancom_free/sound/" + verb_dic[item]["esound"]
            self.params['eword1'] = verb_dic[item]["eword1"]
            self.params['eword2'] = verb_dic[item]["eword2"]
            self.params['eword3'] = verb_dic[item]["eword3"]
            self.params['chinese'] = verb_dic[item]["chinese"]
            self.params['csound'] = "sancom_free/sound/" + verb_dic[item]["csound"]
            self.params['cword1'] = verb_dic[item]["cword1"]
            self.params['cword2'] = verb_dic[item]["cword2"]
            self.params['cword3'] = verb_dic[item]["cword3"]
            self.params['form1'] = Lan_appForm1(filename, sheet, request.POST)
            return render(request, 'sancom_free/sancomcontents.html', self.params)


class Eshadow(TemplateView):
    def __init__(self):
        self.params = {
            'word':'',
            'japanese':'japanese',
            'english':'english',
            'esound':'esound',
            'pronWeblio':'',
            'meaningWeblio':'',
            'error':''
        }

    def get(self, request):
        global item
        global category
        global japanese
        global english
        global esound
        global chinese
        global csound
        item = request.GET['item']
        category = request.GET['category']
        japanese = request.GET['japanese']
        english = request.GET['english']
        esound = request.GET['esound']
        chinese = request.GET['chinese']
        csound = request.GET['csound']
        self.params['item'] = item
        self.params['category'] = category
        self.params['japanese'] = japanese
        self.params['english'] = english
        self.params['esound'] = esound
        self.params['chinese'] = chinese
        self.params['csound'] = csound  
        return render(request, 'sancom_free/eshadow.html', self.params)

    def post(self, request):

        if 'scraping' in request.POST:
            print("Here come!")
            word = request.POST['word']
            load_url1 = "https://ejje.weblio.jp/content/" + word
            html = requests.get(load_url1)
            try:
                soup1 = BeautifulSoup(html.content, "html.parser")
                pronouciation = soup1.find(class_="phoneticEjjeDesc").text
                meaning = soup1.find(class_="content-explanation ej").text
            except AttributeError:
                self.params['error'] = '辞書内に' + word + 'はありませんでした。'
                self.params['japanese'] = japanese
                self.params['english'] = english
                self.params['esound'] = esound            
           
                return render(request, 'sancom_free/eshadow.html', self.params)
            self.params['item'] = item
            self.params['category'] = category           
            self.params['japanese'] = japanese
            self.params['english'] = english
            self.params['esound'] = esound
            self.params['chinese'] = chinese
            self.params['csound'] = csound            
            self.params['word'] = word
            self.params['pronWeblio'] = pronouciation
            self.params['meaningWeblio'] = meaning
            wd = soup1.find(class_="phoneticEjjeDesc").text
            return render(request, 'sancom_free/eshadow.html', self.params)

class Cshadow(TemplateView):
    def __init__(self):
        self.params = {
            'word':'',
            'japanese':'japanese',
            'chinese':'chinese',
            'esound':'esound',
            'pronWeblio':'',
            'meaningWeblio':'',
            'error':''
        }

    def get(self, request):
        global item
        global category
        global japanese
        global english
        global esound
        global chinese
        global csound
        item = request.GET['item']
        category = request.GET['category']
        japanese = request.GET['japanese']
        english = request.GET['english']
        esound = request.GET['esound']
        chinese = request.GET['chinese']
        csound = request.GET['csound']
        self.params['item'] = item
        self.params['category'] = category
        self.params['japanese'] = japanese
        self.params['english'] = english
        self.params['esound'] = esound
        self.params['chinese'] = chinese
        self.params['csound'] = csound  
        return render(request, 'sancom_free/cshadow.html', self.params)

    def post(self, request):

        if 'scraping' in request.POST:
            word = request.POST['word']
            load_url1 = "https://zh.hatsuon.info/word/" + word
            html = requests.get(load_url1)
            try:
                soup1 = BeautifulSoup(html.content, "html.parser")
                pronouciation = soup1.find('div', class_="font4").text
                meaning = soup1.find('div', class_="font1").text
            except AttributeError:
                self.params['error'] = '辞書内に' + word + 'はありませんでした。'
                self.params['japanese'] = japanese
                self.params['english'] = chinese
                self.params['esound'] = csound            
           
                return render(request, 'sancom_free/cshadow.html', self.params)
            self.params['item'] = item
            self.params['category'] = category           
            self.params['japanese'] = japanese
            self.params['english'] = english
            self.params['esound'] = esound
            self.params['chinese'] = chinese
            self.params['csound'] = csound            
            self.params['word'] = word
            self.params['pronWeblio'] = pronouciation
            self.params['meaningWeblio'] = meaning
            #wd = soup1.find(class_="phoneticEjjeDesc").text #要調査
            return render(request, 'sancom_free/cshadow.html', self.params)


class Esplite(TemplateView):
    def __init__(self):
        self.params = {
            'word':'',
            'japanese':'japanese',
            'english':'english',
            'esound':'esound',
            'start':'',
            'length':'',
            'end':'',
            'finish_comment':'',

        }

    def get(self, request):
        global item
        global category
        global japanese
        global english
        global esound
        global chinese
        global csound
        
        item = request.GET['item']
        category = request.GET['category']
        japanese = request.GET['japanese']
        english = request.GET['english']
        esound = request.GET['esound']
        chinese = request.GET['chinese']
        csound = request.GET['csound']
        self.params['item'] = item
        self.params['category'] = category
        self.params['japanese'] = japanese
        self.params['english'] = english
        self.params['esound'] = esound
        self.params['chinese'] = chinese
        self.params['csound'] = csound  
        return render(request, 'sancom_free/esplite.html', self.params)

    def post(self, request):

        if 'split' in request.POST:
            i=-1
            start_position = request.POST['start_position']
            end_position = request.POST['end_position']
            duration = request.POST['duration']
            sound = './sancom_free/static/' + esound
            in_wav = wave.Wave_read(sound)
            nchannels, sampwidth, framerate, nframes, comptype, compname = in_wav.getparams()
            st = float(start_position)/float(duration)
            en = float(end_position)/float(duration)
            start = int(st*float(nframes))  #開始位置の処理
            end   = int(en*float(nframes))  #終了位置の処理
            data = in_wav.readframes(nframes)
            tmp_data = np.frombuffer(data, dtype='int16')
            x = tmp_data[start*nchannels:end*nchannels] #切り出し
            #出力ファイル書き込み
            id = str(self.request.user.id)
            newsound = './sancom_free/static/sancom_free/sound/sound_' + id + '.wav'
            out_wav = wave.Wave_write(newsound)
            nframes = x.size//nchannels
            out_wav.setparams((nchannels, sampwidth, framerate, nframes, comptype, compname))
            out_wav.writeframes(x)
            in_wav.close()
            out_wav.close()
            self.params['item'] = item
            self.params['category'] = category
            self.params['japanese'] = japanese
            self.params['english'] = english
            self.params['esound'] = esound
            self.params['chinese'] = chinese
            self.params['csound'] = csound 
            self.params['sound_splited'] = 'sancom_free/sound/sound_' + id +'.wav'
            self.params['start'] = start_position
            self.params['length'] = duration
            self.params['end'] = end_position
            self.params['finish_comment'] = "以下に分割ファイルを作成しました。手入力で数字を変更して再生位置を微調整できます。"              
            return render(request, 'sancom_free/Esplite.html', self.params) 

class Csplite(TemplateView):
    def __init__(self):
        self.params = {
            'word':'',
            'japanese':'japanese',
            'chinese':'chinese',
            'csound':'csound',
            'start':'',
            'length':'',
            'end':'',
            'finish_comment':'',

        }

    def get(self, request):
        global item
        global category
        global japanese
        global english
        global esound
        global chinese
        global csound
        
        item = request.GET['item']
        category = request.GET['category']
        japanese = request.GET['japanese']
        english = request.GET['english']
        esound = request.GET['esound']
        chinese = request.GET['chinese']
        csound = request.GET['csound']
        self.params['item'] = item
        self.params['category'] = category
        self.params['japanese'] = japanese
        self.params['english'] = english
        self.params['esound'] = esound
        self.params['chinese'] = chinese
        self.params['csound'] = csound  
        return render(request, 'sancom_free/csplite.html', self.params)

    def post(self, request):

        if 'split' in request.POST:
            i=-1
            start_position = request.POST['start_position']
            end_position = request.POST['end_position']
            duration = request.POST['duration']
            sound = './sancom_free/static/' + csound
            in_wav = wave.Wave_read(sound)
            nchannels, sampwidth, framerate, nframes, comptype, compname = in_wav.getparams()
            st = float(start_position)/float(duration)
            en = float(end_position)/float(duration)
            start = int(st*float(nframes))  #開始位置の処理
            end   = int(en*float(nframes))  #終了位置の処理
            data = in_wav.readframes(nframes)
            tmp_data = np.frombuffer(data, dtype='int16')
            x = tmp_data[start*nchannels:end*nchannels] #切り出し
            #出力ファイル書き込み
            id = str(self.request.user.id)
            newsound = './sancom_free/static/sancom_free/sound/sound_' + id + '.wav'
            out_wav = wave.Wave_write(newsound)
            nframes = x.size//nchannels
            out_wav.setparams((nchannels, sampwidth, framerate, nframes, comptype, compname))
            out_wav.writeframes(x)
            in_wav.close()
            out_wav.close()
            self.params['item'] = item
            self.params['category'] = category
            self.params['japanese'] = japanese
            self.params['english'] = english
            self.params['esound'] = esound
            self.params['chinese'] = chinese
            self.params['csound'] = csound
            self.params['sound_splited'] = 'sancom_free/sound/sound_' + id +'.wav'
            self.params['start'] = start_position
            self.params['length'] = duration
            self.params['end'] = end_position
            self.params['finish_comment'] = "以下に分割ファイルを作成しました。手入力で数字を変更して再生位置を微調整できます。"              
            return render(request, 'sancom_free/csplite.html', self.params) 

class Lan_appView2(TemplateView):
    def __init__(self):
        self.params = {
            'title':'一般公開コンテンツ',
            'message':'　',
            'form1':'',
            'item':'',
            'category':'',
            'english':'',
            'esound':'',
            'error':''
        }

    def get(self, request):
        global filename
        global sheet

        file = File.objects.filter(owner=request.user).first()
        filename = file.filename1
        sheet = 'sheet2'
        excel = Excel_link(filename, sheet)
        excel_list = excel.getlist()
        form1 = Lan_appForm1(filename, sheet)
        form1.fields['choice1'].choices = excel_list[2]
        self.params['form1'] = form1
        return render(request, 'sancom_free/publiccontents.html', self.params)

    def post(self, request):
        global item
        global category
        global english
        global esound
        global filename
        global filename

        if 'start' in request.POST:
            file = File.objects.filter(owner=request.user).first()
            filename = file.filename1
            sheet = 'sheet2'
            excel = Excel_link(filename, sheet)
            excel_list = excel.getlist()
            verb_dic = excel_list[0]
            try:
                ch1 = request.POST['choice1']
            except MultiValueDictKeyError:
                self.params['error'] = 'コンテンツを選択してください。'
                return render(request, 'sancom_free/publiccontents.html', self.params)
            item=ch1            
            category = verb_dic[item]["category"]
            english = verb_dic[item]["english"] 
            esound = "sancom_free/sound/" + verb_dic[item]["esound"]
            self.params['item'] = item             
            self.params['category'] = category
            self.params['english'] = english
            self.params['esound'] = esound
            self.params['form1'] = Lan_appForm1(filename, sheet, request.POST)
            return render(request, 'sancom_free/publiccontents.html', self.params)

        if 'scraping' in request.POST:
            file = File.objects.filter(owner=request.user).first()
            filename = file.filename1
            sheet = 'sheet2'
            word = request.POST['word']
            load_url1 = "https://ejje.weblio.jp/content/" + word
            html = requests.get(load_url1)
            try:
                soup1 = BeautifulSoup(html.content, "html.parser")
                pronouciation = soup1.find(class_="phoneticEjjeDesc").text
                meaning = soup1.find(class_="content-explanation ej").text
            except AttributeError:
                self.params['error'] = '辞書内に' + word + 'はありませんでした。'
                self.params['item'] = item
                self.params['category'] = category
                self.params['english'] = english
                self.params['esound'] = esound    
                self.params['form1'] = Lan_appForm1(filename, sheet, request.POST)                        
                return render(request, 'sancom_free/publiccontents.html', self.params)
            self.params['item'] = item
            self.params['category'] = category           
            self.params['english'] = english
            self.params['esound'] = esound
            self.params['word'] = word
            self.params['pronWeblio'] = pronouciation
            self.params['meaningWeblio'] = meaning
            self.params['form1'] = Lan_appForm1(filename, sheet, request.POST)   
            #wd = soup1.find(class_="phoneticEjjeDesc").text
            return render(request, 'sancom_free/publiccontents.html', self.params)

        if 'split' in request.POST:
            file = File.objects.filter(owner=request.user).first()
            filename = file.filename1
            sheet = 'sheet2'            
            start_position = request.POST['start_position']
            end_position = request.POST['end_position']
            duration = request.POST['duration']
            sound = './sancom_free/static/' + esound
            in_wav = wave.Wave_read(sound)
            nchannels, sampwidth, framerate, nframes, comptype, compname = in_wav.getparams()
            st = float(start_position)/float(duration)
            en = float(end_position)/float(duration)
            start = int(st*float(nframes))  #開始位置の処理
            end   = int(en*float(nframes))  #終了位置の処理
            data = in_wav.readframes(nframes)
            tmp_data = np.frombuffer(data, dtype='int16')
            x = tmp_data[start*nchannels:end*nchannels] #切り出し
            #出力ファイル書き込み
            id = str(self.request.user.id)
            newsound = './sancom_free/static/sancom_free/sound/sound_' + id + '.wav'
            out_wav = wave.Wave_write(newsound)
            nframes = x.size//nchannels
            out_wav.setparams((nchannels, sampwidth, framerate, nframes, comptype, compname))
            out_wav.writeframes(x)
            in_wav.close()
            out_wav.close()
            self.params['item'] = item
            self.params['category'] = category
            self.params['english'] = english
            self.params['esound'] = esound
            self.params['sound_splited'] = 'sancom_free/sound/sound_' + id +'.wav'
            self.params['start'] = start_position
            self.params['length'] = duration
            self.params['end'] = end_position
            self.params['finish_comment'] = "以下に分割ファイルを作成しました。" 
            self.params['form1'] = Lan_appForm1(filename, sheet, request.POST)            
            return render(request, 'sancom_free/publiccontents.html', self.params) 