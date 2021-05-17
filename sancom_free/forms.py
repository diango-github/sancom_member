from django import forms
from account.models import File
from django.contrib.auth.models import User
import openpyxl

class Excel_link:

    def __init__(self, filename, sheet):
        self.fname = filename
        self.sheet = sheet
        self.verb_dic={}
        self.verb_list=[]
        self.listbox=[]
        self.excel_data=[]
    
    def getlist(self):
        wb=openpyxl.load_workbook("./static/" + self.fname)
        sh=wb.get_sheet_by_name(self.sheet)
        #sh=wb.active
        for row in range(2,sh.max_row +1 ):
            #index=sh["A"+str(row)].value
            item=sh["B"+str(row)].value
            category=sh["C"+str(row)].value
            japanese=sh["D"+str(row)].value
            english=sh["E"+str(row)].value
            esound=sh["F"+str(row)].value
            eword1=sh["G"+str(row)].value
            eword2=sh["H"+str(row)].value
            eword3=sh["I"+str(row)].value
            chinese=sh["J"+str(row)].value
            csound=sh["K"+str(row)].value
            cword1=sh["L"+str(row)].value
            cword2=sh["M"+str(row)].value
            cword3=sh["N"+str(row)].value
            self.verb_dic.setdefault(item,{"category":category, "japanese":japanese, "english":english, "esound":esound,"eword1":eword1, "eword2":eword2, "eword3":eword3, "chinese":chinese,"csound":csound,"cword1":cword1,"cword2":cword2,"cword3":cword3})
        self.verb_list=list(self.verb_dic.keys())
        for i in range(len(self.verb_list)):
            self.listbox.append((self.verb_list[i], self.verb_list[i]))
        self.excel_data = [self.verb_dic, self.verb_list, self.listbox]
        return self.excel_data

class Lan_appForm1(forms.Form):

    def __init__(self, filename, sheet, *args, **kwargs):
        super(Lan_appForm1, self).__init__(*args, **kwargs)
        self.fname = filename
        excelfile = self.fname
        self.sheet = sheet
        excelsheet = self.sheet
        excel = Excel_link(excelfile, excelsheet)
        excel_list = excel.getlist()
        self.fields['choice1'] = forms.ChoiceField(label='', choices=excel_list[2], required=True, widget=forms.Select(attrs={'id':'choice1','size':4}))

