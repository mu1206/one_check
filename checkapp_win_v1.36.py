#!C:/Python27/python.exe
# -*- coding: utf-8 -*-
'''
Note:The script is only used in Windows

Created on 2018/8/2

Version:App check V1.35

Author:01040252
'''
import commands
import os
import sys
import socket
import urllib2
import logging
import json
import time
import subprocess
import datetime
import string
import linecache
import ctypes
import re
reload(sys)
sys.setdefaultencoding( "utf-8" )
def shell(cmd):
    result = str(commands.getoutput(cmd))
    return result
def go(cmd):
    if not cmd:
        return
    output = ''
    try:
        output = subprocess.check_output(cmd, shell=True)
    except:
        pass
    return output
    
def check_self_proc():
    psname = sys.argv[0][3:19]
    cmd = 'tasklist -v|findstr /i "python taskeng"|find "%s"' % psname
    cmd1 = 'tasklist -v|findstr /i "python"|find /i "taskeng" /c'
    result = os.popen(cmd).read()
    result1 = int(os.popen(cmd1).read())
    psnumber = result.count(psname) + result1
    if psnumber >= 5 :
        print "ERROR: The %s should be < 5 [%s]" % (psname,psnumber)
        sys.exit(1)
        
# set time task
# parameter: -timetask user
def timetask():
    parameters = get_parameters()
    if parameters.get('-timetask'):
        user = parameters.get('-timetask')
    else:
        user = ""
        return
    go('chcp 437')
    aaa = go('schtasks /query|findstr "Update"')
    go('chcp 936')
    cmd = 'ver | findstr "6\."'
    password = "aaa"
    path = "C:/apptools/checkapp_win.py"
    date_time = datetime.datetime.today().strftime('%Y-%m-%dT%H:%M:%S')
    filename = "C:/apptools/registerSchtasks.xml"
    with open(filename,'a+') as f:
        f.write('<?xml version="1.0" encoding="UTF-16"?>'+'\n')
        f.write('<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">'+'\n')
        f.write('<Triggers>'+'\n')
        f.write('<LogonTrigger>'+'\n')
        f.write('<StartBoundary>'+date_time+'</StartBoundary>'+'\n')
        f.write('<Enabled>true</Enabled>'+'\n')
        f.write('<UserId>'+user+'</UserId>'+'\n')
        f.write('</LogonTrigger>'+'\n')
        f.write('</Triggers>'+'\n')
        f.write('<Principals>'+'\n')
        f.write('<Principal id="Author">'+'\n')
        f.write('<RunLevel>HighestAvailable</RunLevel>'+'\n')
        f.write('<UserId>'+user+'</UserId>'+'\n')
        f.write('<LogonType>InteractiveToken</LogonType>'+'\n')
        f.write('</Principal>'+'\n')
        f.write('</Principals>'+'\n')
        f.write('<Settings>'+'\n')
        f.write('<MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>'+'\n')
        f.write('<DisallowStartIfOnBatteries>true</DisallowStartIfOnBatteries>'+'\n')
        f.write('<StopIfGoingOnBatteries>true</StopIfGoingOnBatteries>'+'\n')
        f.write('<AllowHardTerminate>true</AllowHardTerminate>'+'\n')
        f.write('<StartWhenAvailable>false</StartWhenAvailable>'+'\n')
        f.write('<RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>'+'\n')
        f.write('<IdleSettings>'+'\n')
        f.write('<StopOnIdleEnd>true</StopOnIdleEnd>'+'\n')
        f.write('<RestartOnIdle>false</RestartOnIdle>'+'\n')
        f.write('</IdleSettings>'+'\n')
        f.write('<AllowStartOnDemand>true</AllowStartOnDemand>'+'\n')
        f.write('<Enabled>true</Enabled>'+'\n')
        f.write('<Hidden>false</Hidden>'+'\n')
        f.write('<RunOnlyIfIdle>false</RunOnlyIfIdle>'+'\n')
        f.write('<WakeToRun>false</WakeToRun>'+'\n')
        f.write('<ExecutionTimeLimit>P3D</ExecutionTimeLimit>'+'\n')
        f.write('<Priority>7</Priority>'+'\n')
        f.write('</Settings>'+'\n')
        f.write('<Actions Context="Author">'+'\n')
        f.write('<Exec>'+'\n')
        f.write('<Command>'+path+'</Command>'+'\n')
        f.write('</Exec>'+'\n')
        f.write('</Actions>'+'\n')
        f.write('</Task>'+'\n')
    cmd1 = "schtasks /create /tn Entegor_Agent /xml %s /f" % filename
    try:
        go(cmd1)
        print "Timetask set successful"
    except exception as e:
        print e
    os.remove(filename)
        
class Logger(object): 
    def __init__(self, filename="Default.log",mode=""): 
        self.terminal = sys.stdout 
        self.log = open(filename,mode) 
        
    def write(self, message): 
        self.terminal.write(message) 
        self.log.write(message)

    def flush(self): 
        pass 
        
def clean_log(path):
    if os.path.exists(path) and os.path.isdir(path):
        today = datetime.date.today().strftime('%Y-%m-%d')  # 2017-01-02
        i = 0
        file_name_list = [today,]
        #保留10天日志
        for day in range(9):
            i = i - 1
            day = (datetime.date.today() + datetime.timedelta(i)).strftime('%Y-%m-%d')
            file_name_list.append(day)
        for f in os.listdir(path):
            file_name_sp = f.split('.')
            if len(file_name_sp) > 2:
                file_date = file_name_sp[1]  # 取文件名里面的日期
                if file_date not in file_name_list:
                    abs_path = os.path.join(path, f)
                    os.remove(abs_path)
                    
def saveLog():
    if not os.path.exists('C:/apptools/logs'):
        os.makedirs('C:/apptools/logs')
    clean_log('C:/apptools/logs')
    today = "C:/apptools/logs/checkapp." + datetime.date.today().strftime('%Y-%m-%d') + ".log"
    now = "C:/apptools/logs/now.log"
    sys.stdout = Logger(today,mode='a+')
    sys.stdout = Logger(now,mode='w')
        
def removebom(file):
    f = open(file,"r")
    s = f.read()
    u = s.decode("utf-8-sig")
    s = u.encode("utf-8")
    f.close()
    return s

def get_parameters():
    list1 = sys.argv[1:][::2]
    list2 = sys.argv[1:][1::2]
    parameters = dict(zip(list1,list2))
    return parameters
    
# 配置休眠时间
def timesleep():
    parameters = get_parameters()
    if parameters.get('-sleep'):
        num = int(parameters.get('-sleep'))
    else:
        num = 300
    return num 
    
def get_appconf():
    parameters = get_parameters()
    if parameters.get('-cfgfile'):
        name = parameters.get('-cfgfile')
    else:
        name = "C:\\apptools\\appconf.json"
    return name 
    
STD_OUTPUT_HANDLE = -11
 
#字体颜色定义 text colors
FOREGROUND_BLUE = 0x0b # blue.
FOREGROUND_GREEN = 0x0a # green.
FOREGROUND_RED = 0x0c # red.
 
# get handle
std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
 
def set_cmd_text_color(color, handle=std_out_handle):
    Bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
    return Bool
 
#reset white
def resetColor():
    set_cmd_text_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)
 
#green
def printGreen(mess):
    set_cmd_text_color(FOREGROUND_GREEN)
    sys.stdout.write(mess + '\n')
    resetColor()

#red
def printRed(mess):
    set_cmd_text_color(FOREGROUND_RED)
    sys.stdout.write(mess + '\n')
    resetColor()
  
#blue
def printBlue(mess):
    set_cmd_text_color(FOREGROUND_BLUE)
    sys.stdout.write(mess + '\n')
    resetColor()
    
def printResult(result):
    if result == 0:
        printGreen("Everything is OK !!!")
    elif result == 100:
        printBlue("COLD_STANDBY !!!")
        printGreen("Everything is OK !!!")
    elif result == 101:
        printBlue("COLD_STANDBY !!!")
        printRed("Something is ERROR !!!")
    else:
        printRed("Something is ERROR !!!")
    
# define reverse search class
class BackwardsReader:
    '''Read a file line by line, backwards'''
    BLKSIZE = 4096

    def readline(self):
        while 1:
            newline_pos = string.rfind(self.buf, '\n')
            # print newline_pos
            pos = self.thefile.tell()
            # print pos
            if newline_pos != -1:
                # Found a newline
                line = self.buf[newline_pos+1:]
                self.buf = self.buf[:newline_pos]
                if pos != 0 or newline_pos != 0 or self.trailing_newline:
                    line += '\n'
                return line
            else:
                if pos == 0:
                    # Start-of-thefile
                    return 'break'
                else:
                    # Need to fill buffer
                    toread = min(self.BLKSIZE, pos)
                    self.thefile.seek(-toread, 1)
                    self.buf = self.thefile.read(toread) + self.buf
                    self.thefile.seek(-toread, 1)
                    if pos - toread == 0:
                        self.buf = '\n' + self.buf

    def __init__(self, thefile):
        self.thefile = thefile
        self.buf = ''
        self.thefile.seek(-1, 2)
        self.trailing_newline = 0
        lastchar = self.thefile.read(1)
        if lastchar == '\n':
            self.trailing_newline = 1
            self.thefile.seek(-1, 2)

    def close(self):
        self.thefile.close()
        
class MyApp(object):
    
    def __init__(self, app_info):
        '''
         GetAppInfo
        '''
        self.name = app_info.get('name')
        self.path = app_info.get('path')
        self.proclist = app_info.get('process')
        self.portlistenlist = app_info.get('port_listen')
        self.porttimewaitlist = app_info.get('port_timewait')
        self.capacitycmd = app_info.get('capacity')
        self.runcmd = app_info.get('runcmd')
        self.netDstlist = app_info.get('netDst')
        self.customcmd = app_info.get('custom')
        self.startcmdlist = app_info.get("show_startcmd")
        self.stopcmdlist = app_info.get("show_stopcmd")
        self.encrypt_portlist = app_info.get("encrypt_port")
        self.iplist = app_info.get('net_ping')
        self.encrypt_portlist = app_info.get("encrypt_port")
        self.service_names = app_info.get('service_win')
        self.iis_status = app_info.get('iis_status')
        self.ip_portlist = app_info.get('net_conn')
        self.normal_keywords = app_info.get('log_normal')
        self.abnormal_keywords = app_info.get('log_abnormal')
        self.ip_portsfok = app_info.get('check_msg')
        self.shared_filelist = app_info.get('shared_file')
        self.urllists = app_info.get('check_url')
        self.iis_weblist = app_info.get('iis_web')
        self.iis_applist = app_info.get('iis_app')
        self.comment = app_info.get('comment')
        self.commentfile = app_info.get('comment_file')
        self.consistency_files = app_info.get('consistency_file')
        self.standby_mode = app_info.get('standby_mode')
        self.cpu_usage = app_info.get('cpu_usage')
        self.mem_usage = app_info.get('mem_usage')
        self.fs_usage = app_info.get('fs_usage')

    def code_conversion(self,result):
        try:
            result = result.decode('utf-8')
        except:
            result = result.decode('gb2312')
        return result
        
    def check_service(self):
        resultstr = ""
        if not self.service_names:
            return resultstr
        print "[%s-SERVICE_WIN]" % self.name
        print "{%s}" % self.service_names
        cmd = 'sc query | find "_NAME:"'
        result = os.popen(cmd).read()
        for servicename in self.service_names.split(","):
            if result.count(servicename.encode('gb2312')) < 1:
                resultstr = resultstr  + "ERROR:SERVICE NAME %s STATE IS NOT RUNNING !\r\n" % (servicename)
        if resultstr == "":
            print "OK: CHECK OK ! \r\n"
        else:
            print resultstr
        return resultstr
        
    def show_standby_mode_normal(self):
        parameters = get_parameters()
        if parameters.get('-standby_mode'):
            self.standby_mode = parameters.get('-standby_mode')
        if self.standby_mode:
            print "{%s-STANDBY_MODE}" % self.name
            print self.standby_mode
            print
        
    def check_keyword_by_url(self,urllist):
        url = urllist.split("|")[0]
        keyword = urllist.split("|")[1]
        result = "ERROR: %s is False ! \r\n" % urllist
        try:
            req = urllib2.Request(url)
            res_data = urllib2.urlopen(req,None,5)
            content = res_data.read()
            if content.find(keyword) >= 0:
                result = ""
        except Exception, e:
            logging.error(str(e))
        return result
        
    def check_by_url(self,urllist):
        try:
            urllib2.urlopen(urllist)
            result = ""
        except Exception, e:
            result = "ERROR: %s \n" % e
        return result
        
    def find_keyword_by_url(self):
        if not self.urllists:
            return ""
        print "[%s-CHECK_URL]" % self.name
        print "{%s}" % self.urllists
        result = ""
        for urllist in self.urllists.split(';'):
            if "|" in urllist:
                result = result + self.check_keyword_by_url(urllist)
            else:
                result = result + self.check_by_url(urllist)
        if result != "":
            print result 
        else:
            print "OK: CHECK OK ! \r\n"
        return result
    
    def check_iis_status(self):
        if not self.iis_status:
            return
        print "[%s-IIS_STAUTS]" % self.name
        print "{%s}" % self.iis_status
        if self.iis_status and self.iis_status.lower() != "check":
            result = "ERROR :config not right ! \n"
            print result
            return result
        resultstr = ""
        cmd = 'wmic.exe service where name="W3SVC" get State,StartMode,StartName'
        output = go(cmd)
        check = output.split('\r\n')[0:2]
        values = [x.replace(' ', '') for x in check[1].rstrip('\r').split(' ') if x]
        if len(values) < 3:
            resultstr = "ERROR: IIS SERVICE NOT EXIST !\r\n"
            print resultstr
            return resultstr
        if values[2] == "Running":
            print "OK: CHECK OK !\r\n"
        else:
            resultstr = "ERROR: IIS SERVICE STATE IS %s !\r\n" % values[2]
            print resultstr
        return resultstr
    
    def check_app_pool(self):
        if not self.iis_applist:
            return
        print "[%s-IIS_APP]" % self.name
        print "{%s}" % self.iis_applist
        resultstr = ""
        status = ""
        for pool in self.iis_applist.split(','):
            value = 'unchecked'
            cmd = 'C:\\windows\\system32\\inetsrv\\appcmd.exe list apppool | ' +\
                  'findstr /c:"%s"' % pool
            output = go(cmd)
            if output == "":
                resultstr = resultstr + "ERROR: IIS APP %s is WRONG!\r\n" % pool
                continue
            check = output.split('\r\n')[0]
            result = [x.replace(' ', '')
                     for x in check.rstrip('\r').split(' ') if x]
            try:
                ln = result[-1].split(',')[-1].replace(')', '').split(':')
            except:
                resultstr = resultstr + "ERROR :Please check the parameters !\r\n"
                status = "error"
            if status == "error":
               continue
            if ln[0] == 'state':
                value = ln[1]
            if value and value != "Started":
                resultstr = resultstr + "ERROR: IIS APP %s STATE IS %s !\r\n" % (pool,value)
        if resultstr == "":
            print "OK: CHECK OK ! \r\n"
        else:
            print resultstr
        return resultstr
        
    def check_iis_web(self):
        
        if not self.iis_weblist:
            return
        print "[%s-IIS_WEB]" % self.name
        print "{%s}" % self.iis_weblist
        resultstr = ""
        for site in self.iis_weblist.split(','):
            value = 'unchecked'
            cmd = 'c:\\windows\\system32\\inetsrv\\appcmd.exe list sites | ' +\
                  'findstr \"%s\"' % site
            output = go(cmd)
            if output == "":
                resultstr = resultstr + "ERROR: IIS WEB %s is WRONG!\r\n" % site
                continue
            check = output.split('\r\n')[0]
            result = [x.replace(' ', '')
                      for x in check.rstrip('\r').split(' ') if x]
            ln = result[-1].split(',')[-1].replace(')', '').split(':')
            if ln[0] == 'state':
                value = ln[1]
            if value and value != "Started":
                resultstr = resultstr + "ERROR: IIS WEB %s IS %s !\r\n" % (site,value)
        if resultstr == "":
            print "OK: CHECK OK !\r\n"
        else:
            print resultstr
        return resultstr
        
    def showCmd(self, cmdstr):
        print "<%s>" % cmdstr
        
    def showcomment(self):
        if not self.comment:
            return ""
        print "[%s-COMMENT]" % self.name
        print "%s" % self.comment
        
    def showcommentfile(self):
        if not self.commentfile:
            return ""
        print "[%s-COMMENT_FILE]" % self.name
        try:
            with open(self.commentfile) as f:
                print f.read().decode('utf-8-sig')
        except:
            with open(self.commentfile) as f:
                print f.read().decode('gb2312')
        
        
    def showCapacity(self):
        if self.capacitycmd:
            print "[CAPACITY]"
            cmd = self.capacitycmd
            resultlist = go(cmd)
            self.showCmd(cmd)
            print resultlist
        print
        return True

    def aleatory_variable(self,keywords,resultlist):
        count = 0
        counts = 0
        resultnumber = 0
        for keyword in keywords:
            try:
                resultnumber = resultlist.count(keyword)
            except:
                resultnumber = resultlist.count(keyword.encode('utf-8'))
            if resultnumber >= 1:
                count += 1
                counts = counts + resultnumber
        return count,counts
        
    def aleatory_variable_and(self,keywords,resultlist):
        count = 0
        counts = []
        resultnumber = 0
        for keyword in keywords:
            try:
                resultnumber = resultlist.count(keyword)
            except:
                resultnumber = resultlist.count(keyword.encode('utf-8'))
            if resultnumber >= 1:
                count += 1
                counts.append(resultnumber)
        if counts:
            counts = min(counts)
        else:
            counts = 0
        return count,counts
        
    def checkruncmd(self):
        resultstr = ""
        if self.runcmd:
            print "[%s-RUNCMD]" % self.name
            print "{%s}" % self.runcmd
            for runcmd in self.runcmd.split(";"):
                resultnumber = 0
                resultabnumber = 0
                runcmdlist = runcmd.split('|=')
                cmd = runcmdlist[0].decode('utf-8').encode('gb2312')
                resultlist = os.popen(cmd).read()
                #print chardet.detect(resultlist)
                try:
                    resultlist = self.code_conversion(resultlist)
                except:
                    pass
                print resultlist
                print
                if len(runcmdlist) == 2 and not runcmdlist[1]:
                    return
                if len(runcmdlist) >= 2:
                    flag = 0
                    if "&&" in runcmdlist[1] and "++"  not in runcmdlist[1]:
                        keywords = runcmdlist[1].split("&&")
                        count,counts = self.aleatory_variable_and(keywords,resultlist)
                        if count >= len(keywords):
                            resultnumber = counts
                    if "++" in runcmdlist[1] and "&&" not in runcmdlist[1]:
                        keywords = runcmdlist[1].split("++")
                        count,counts = self.aleatory_variable(keywords,resultlist)
                        if count > 0:
                            resultnumber = counts
                    if "&&" in runcmdlist[1] and "++"  in runcmdlist[1]:
                        keywords = runcmdlist[1].split("&&")
                        keywordlist_or = []
                        keywordlist_and = []
                        for keyword in keywords:
                            if "++" in keyword:
                                keywordlist_or.append(keyword)
                            if "++" not in keyword:
                                keywordlist_and.append(keyword)
                        if keywordlist_or:
                            for keyword in keywordlist_or:
                                count,counts_or = self.aleatory_variable(keyword.split('++'),resultlist)
                        if count == 0:
                            flag += 1
                        if keywordlist_and:
                            count,counts_and = self.aleatory_variable_and(keywordlist_and,resultlist)
                        if count >= len(keywordlist_and) and flag == 0:
                            resultnumber = counts_and + counts_or
                        else:
                            resultnumber = 0
                    if "&&" not in runcmdlist[1] and "++" not in runcmdlist[1]:
                        try:
                            resultnumber = resultlist.count(runcmdlist[1])
                        except:
                            resultnumber = resultlist.count(runcmdlist[1].encode('utf-8'))
                if len(runcmdlist) == 3:
                    flag = 0
                    if "&&" in runcmdlist[2] and "++" not in runcmdlist[2]:
                        keywords = runcmdlist[2].split("&&")
                        count,counts = self.aleatory_variable_and(keywords,resultlist)
                        if count >= len(keywords):
                            resultabnumber = counts
                    if "++" in runcmdlist[2] and "&&" not in runcmdlist[2]:
                        keywords = runcmdlist[2].split("++")
                        count,counts = self.aleatory_variable(keywords,resultlist)
                        if count > 0:
                            resultabnumber = counts
                    if "&&" in runcmdlist[2] and "++"  in runcmdlist[2]:
                        keywords = runcmdlist[2].split("&&")
                        keywordlist_or = []
                        keywordlist_and = []
                        for keyword in keywords:
                            if "++" in keyword:
                                keywordlist_or.append(keyword)
                            if "++" not in keyword:
                                keywordlist_and.append(keyword)
                        if keywordlist_or:
                            for keyword in keywordlist_or:
                                count,counts_or = self.aleatory_variable(keyword.split('++'),resultlist)
                        if count == 0:
                            flag += 1
                        if keywordlist_and:
                            count,counts_and = self.aleatory_variable_and(keywordlist_and,resultlist)
                        if count >= len(keywordlist_and) and flag == 0:
                            resultabnumber = counts_and + counts_or
                    if "&&" not in runcmdlist[2] and "++" not in runcmdlist[2]:
                        try:
                            resultabnumber = resultlist.count(runcmdlist[2])
                        except:
                            resultabnumber = resultlist.count(runcmdlist[2].encode('utf-8'))
                if len(runcmdlist) == 2 and resultnumber == 0 :
                    resultstr = resultstr + "ERROR: NORMAL KEYWORD %s NUMBER IS %s ! \r\n" % (runcmdlist[1],resultnumber)
                if len(runcmdlist) == 3 and not runcmdlist[1]:
                    if resultabnumber > 0:
                        resultstr = resultstr + "ERROR: ABNORMAL KEYWORD %s NUMBER IS %s !\r\n" \
                        % (runcmdlist[2],resultabnumber)
                if len(runcmdlist) == 3 and runcmdlist[1]:
                    if resultnumber == 0:
                        resultstr = resultstr + "ERROR: NORMAL KEYWORD %s NUMBER IS %s !\r\n" % (runcmdlist[1],resultnumber)
                    if resultabnumber > 0:
                        resultstr = resultstr + "ERROR: ABNORMAL KEYWORD %s NUMBER IS %s !\r\n" % (runcmdlist[2],resultabnumber)
            if resultstr != "":
                print resultstr
            else:
                if len(runcmdlist) > 1:
                    print "OK: CHECK OK !\r\n"
            return resultstr
            
    #根据传入参数的符号,进行判断
    def judgement(self,number,errorinfo,resultnumber):
        resultstr = ""
        if number[0] == '>' and resultnumber <= int(number[1:]):
                resultstr = errorinfo
        if number[0] == '<' and resultnumber >= int(number[1:]):
                resultstr = errorinfo
        if number[0] == '=' and resultnumber != int(number[1:]):
                resultstr = errorinfo
        return resultstr
            
    def checkProc(self,psnames,_item):
        resultstr = ""
        for psname in psnames:
            resultnumber = 0
            ps_name = psname.replace("&&",'"|find /i "')
            cmd = 'tasklist.exe -v|find /i "%s" /c' % ps_name
            if not go(cmd):
                resultstr = resultstr + "ERROR: PROCESS %s NUMBER IS 0 ! \r\n" % psname
                continue
            resultnumber = int(go(cmd))
            psname = psname.encode('gb2312')
            if "cmd" in cmd:
                resultnumber = resultnumber - 1
            if len(_item) >= 2 and _item[1][0] in ">=<" and not _item[1][1:].isdigit():
                resultstr = resultstr + "ERROR: THE SECOND PARAMETER %s IS ERROR !\r\n" % _item[1].encode('gb2312')
                break
            if len(_item) >= 2 and _item[1] and _item[1][0] not in ">=<":
                _item[1] = _item[1].encode('gb2312')
                psname_1 = "%%" + psname.split('&&')[0] + "%%"
                commandline = "\" and commandline like \"%%" + _item[1].replace('&&','%%" and commandline like "%%') + "%%"
                psname_1 = psname_1 + commandline
                if resultnumber >= 1:
                    count = 0
                    cmd_a = '''wmic.exe process where 'caption like "%s" ' get commandline ''' % psname_1
                    result = os.popen(cmd_a).read()
                    if not result:
                        resultnumber = 0
                        resultstr = resultstr + "ERROR: PROCESS %s COMMANDLINE %s IS NULL ! \r\n" % (psname,_item[1])
                        continue
                    result = result.count(_item[1].split("&&")[0])
                    if 'cmd' in cmd_a:
                        count = result - 1
                    else:
                        count = result
                    resultnumber = count
            if len(_item) == 2 :
                if ">" in _item[1] or "=" in _item[1] or "<" in _item[1]:
                    errorinfo = "ERROR: PROCESS %s NUMBER IS %s ! \r\n" % (psname,resultnumber)
                    resultstr = resultstr + self.judgement(_item[1],errorinfo,resultnumber)
                else:
                    if resultnumber == 0:
                        resultstr = resultstr + "ERROR: PROCESS %s COMMANDLINE %s IS 0 ! \r\n" % (psname,_item[1])
            if len(_item) == 3 and _item[1]:
                errorinfo = "ERROR: PROCESS %s COMMANDLINE %s IS %s ! \r\n" % (psname,_item[1],resultnumber)
                resultstr = resultstr + self.judgement(_item[2],errorinfo,resultnumber)
            if len(_item) == 3 and not _item[1]:
                errorinfo = "ERROR: PROCESS '%s' NUMBER IS %s ! \r\n" % (psname,resultnumber)
                resultstr = resultstr + self.judgement(_item[2],errorinfo,resultnumber)
            if len(_item) == 1:
                if resultnumber < 1:
                    resultstr = resultstr + "ERROR: PROCESS '%s' NUMBER IS %s ! \r\n" % (psname,resultnumber)
        return resultstr.decode('gb2312')
                        
    def showProc(self):
        if self.proclist:
            print "[%s-PROCESS]" % self.name
            print "{%s}" % self.proclist
            #/usr/sbin/atd|>3;/usr/sbin/atd
            proc_list=self.proclist.split(';')
            #['/usr/sbin/atd|>3','/usr/sbin/atd']
            ProcList = []
            resultstr = ""
            for item in proc_list:
                ProcList.append(item.split('|'))
            #[['/usr/sbin/atd','>3'],['/usr/sbin/atd']]
            for item in ProcList:
                if "," in item[0]:
                    psnames = item[0].split(",")
                    resultstr = resultstr + self.checkProc(psnames,item)
                else:
                    psnames = [item[0]]
                    resultstr = resultstr + self.checkProc(psnames,item)
            if not resultstr:
                print "OK:CHECK OK !\r\n"
            else:
                print resultstr
            return resultstr
        
        
    def showPortListen(self):
        resultstr = ""
        if self.portlistenlist:
            print "[%s-PORT_LISTEN]" % self.name
            print "{%s}" % self.portlistenlist
            portlistenlist=self.portlistenlist.split(',')
            for _item in portlistenlist:
                resultnumber = 0
                cmd = 'netstat -an|findstr ":%s\>" |find "LISTENING"' % _item
                result = os.popen(cmd).read()
                resultnumber = result.count(_item)
                if resultnumber == 0:
                    resultstr = resultstr + "ERROR: PORT %s NOT LISTENING ! \r\n" % _item
            if resultstr != "":
                print resultstr
            else:
                print "OK:CHECK OK !\r\n"
            return resultstr
        
    def check_prottime_wait(self,ptnames,_item):
        resultstr = ""
        for ptname in ptnames:
            cmd = 'netstat -an|find "TIME_WAIT"|findstr "%s "' % ptname
            result = os.popen(cmd).read()
            resultnumber = result.count(ptname)
            if len(_item) == 1:
                if resultnumber >= 1000:
                    resultstr = resultstr + "ERROR: PORT %s TIMEWAIT NUMBER IS %s [>=1000] !\r\n" % (ptname,resultnumber)
            if len(_item) == 2:
                psnumber = _item[1]
                errorinfo = "ERROR: PORT %s TIMEWAIT NUMBER IS %s ! \r\n" % (ptname,resultnumber)
                resultstr = resultstr + self.judgement(psnumber,errorinfo,resultnumber)
        return resultstr
        
    def prot_time_wait(self):
        resultstr = ""
        if self.porttimewaitlist:
            print "[%s-PORT_TIMEWAIT]" % self.name
            print "{%s}" % self.porttimewaitlist
            porttimewaitlist=self.porttimewaitlist.split(';')
            ProtList = []
            for item in porttimewaitlist:
                ProtList.append(item.split('|'))
            for item in ProtList:
                if "," in item[0]:
                    ptnames = item[0].split(",")
                    resultstr = resultstr + self.check_prottime_wait(ptnames,item)
                else:
                    ptnames = [item[0]]
                    resultstr = resultstr + self.check_prottime_wait(ptnames,item)
            if resultstr != "":
                print resultstr
            else:
                print "OK: CHECK OK !\r\n"
        return resultstr
        
    
    def showCustom(self):
        if self.customcmd != "":
            print "[Custom-checkapp]"
            print self.customcmd
            print
        
    def showStart(self):
        if not self.startcmdlist:
            return ""
        print "[%s-START_CMD]" % self.name
        for _item in self.startcmdlist.split(";"):
            print _item
        print
            
    def showStop(self):
        if not self.stopcmdlist:
            return ""
        print "[%s-STOP_CMD]" % self.name
        for _item in self.stopcmdlist.split(";"):
            print _item
        print
        

    def get_line_count(self,filename):
        line_count = 0
        f = open(filename,'r')
        while True:
            BLKSIZE = f.read(8192 * 1024)
            if not BLKSIZE:
                break
            line_count += BLKSIZE.count('\n')
        f.close()
        return line_count

    def read_log(self,filename,num,keywords):
        lines = ""
        linecache.clearcache()
        line_count = self.get_line_count(filename)
        if num == 0:
            num = line_count
            n = num
        else:
            n = int(num)      #get the last n lines
        result_count = 0
        line_count = line_count - n + 1
        if keywords:
            for i in range(n+1):        #the last n lines
                count = 0
                last_line = linecache.getline(filename, line_count)
                last_line = self.code_conversion(last_line)
                for keyword in keywords:
                    if keyword in last_line:
                        count += 1
                if count >= 1:
                    result_count += 1
                    if result_count <= 10:
                        lines = lines + last_line
                line_count += 1
        else:
            for i in range(n+1):        #the last n lines
                last_line = linecache.getline(filename, line_count)
                last_line = self.code_conversion(last_line)
                lines = lines + last_line
                line_count += 1
        return result_count,lines
        
    def read_log_line(self,filename,num,keywords):
        lines = ""
        linecache.clearcache()
        line_count = self.get_line_count(filename)
        if num == 0:
            num = line_count
            n = num
        else:
            n = int(num)      #get the last n lines 
        line_count = line_count - n + 1
        result_count = 0
        for i in range(n+1):        #the last n lines
            count = 0
            last_line = linecache.getline(filename, line_count)
            last_line = self.code_conversion(last_line)
            for keyword in keywords:
                if keyword in last_line:
                    count += 1
            if count >= len(keywords):
                result_count += 1
                if result_count <= 10:
                    lines = lines + last_line
            line_count = i + 1
        return result_count,lines
        
    def read_log_and_or_line(self,filename,num,keywordlist_and,keywordlist_or):
        lines = ""
        linecache.clearcache()
        line_count = self.get_line_count(filename)
        if num == 0:
            num = line_count
            n = num
        else:
            n = int(num)      #get the last n lines
        line_count = line_count - n + 1
        result_count = 0
        for i in range(n+1):        #the last n lines
            count_or = 0
            count_and = 0
            result_count_and = 0
            result_count_or = 0
            flag = 0
            last_line = linecache.getline(filename, line_count)
            last_line = self.code_conversion(last_line)
            for keyword in keywordlist_and:
                if keyword in last_line:
                    count_and += 1
            if count_and >= len(keywordlist_and):
                result_count_and += 1
            for keywords in keywordlist_or:
                for keyword in keywords.split('++'):
                    if keyword in last_line:
                        count_or += 1
                if count_or != 0:
                    result_count_or += 1
                else:
                    flag += 1
            line_count = i + 1
            if result_count_and > 0 and result_count_or > 0 and flag == 0:
                result_count += 1
                if result_count <= 10:
                    lines = lines + last_line
        return result_count,lines
        
    def check_log_keywords(self,_filename,value,num):
        _value = ""
        resultnumber = 0
        if "*" not in _filename and "(new)" not in _filename:
            if "++" in value and "&&" not in value:
                value = value.split('++')
                resultnumber,lines = self.read_log(_filename,num,value)
            elif "&&" in value and "++" not in value:
                value = value.split('&&')
                resultnumber,lines = self.read_log_line(_filename,num,value)
            elif "&&" in value and "++" in value:
                value = value.split('&&')
                keywordlist_or = []
                keywordlist_and = []
                for keyword in value:
                    if "++" in keyword:
                        keywordlist_or.append(keyword)
                    if "++" not in keyword:
                        keywordlist_and.append(keyword)
                resultnumber,lines = self.read_log_and_or_line(_filename,num,keywordlist_and,keywordlist_or)
            else:
                value = [value]
                resultnumber,lines = self.read_log(_filename,num,value)
            number,lines_ok = self.read_log(_filename,10,"")
        return resultnumber,lines,lines_ok

    def keyword_code_conversion(self,line,keyword):
        number = 0
        try:
            number = line.count(keyword)
        except:
            number = line.count(keyword.encode('gb2312'))
        return number
    def search_keywords(self,keyword_counts,keywords,line):
        count = 0
        flag = 0
        if "++" in keywords and "&&" not in keywords:
            for keyword in keywords.split("++"):
                if self.keyword_code_conversion(line,keyword) > 0:
                    count += 1
            if count >= 1:
                keyword_counts += 1
        elif "&&" in keywords and "++" not in keywords:
            for keyword in keywords.split("&&"):
                if self.keyword_code_conversion(line,keyword) > 0:
                    count += 1
            if count >= len(keywords.split("&&")):
                keyword_counts += 1
        elif "&&" in keywords and "++" in keywords:
            keywords = keywords.split("&&")
            keywordlist_or = []
            keywordlist_and = []
            for keyword in keywords:
                if "++" in keyword:
                    keywordlist_or.append(keyword)
                if "++" not in keyword:
                    keywordlist_and.append(keyword)
            if keywordlist_or:
                count = 0
                for keywords in keywordlist_or:
                    for keyword in keywords.split('++'):
                        if self.keyword_code_conversion(line,keyword) > 0:
                            count += 1
                    if count == 0:
                        flag += 1
            if keywordlist_and:
                count = 0
                for keyword in keywordlist_and:
                    if self.keyword_code_conversion(line,keyword) > 0:
                        count += 1
            if count >= len(keywordlist_and) and flag == 0:
                keyword_counts += 1
        else:
            if self.keyword_code_conversion(line,keywords) > 0:
                keyword_counts += 1
        return keyword_counts
        
    def check_log_for_keywords(self, log, keywords, interval, fmt, location):
        # check if file exists or is empty
        num_lines_updated = 0
        keyword_counts = 0
        try:
            log_file = open(log, 'r')
        except:
            logging.error('failed to read %s' % log)
        br = BackwardsReader(log_file)
        # log content example:
        #   20150120 11:47:10  [ERROR] com.cmbchina...
        switch = {
            "d":lambda interval:datetime.timedelta(days=int(interval[:-1])),
            "h":lambda interval:datetime.timedelta(hours=int(interval[:-1])),
            "m":lambda interval:datetime.timedelta(minutes=int(interval[:-1])),
            "s":lambda interval:datetime.timedelta(seconds=int(interval[:-1]))
        }
        time_unit = interval[-1:]
        location_left = location.split(":")[0]
        location_right = location.split(":")[1]
        no_time_counts = 0
        lines = ""
        lines_ok = ""
        while True:
            counts = keyword_counts
            line = br.readline().replace("  "," ")
            if not line:
                continue
            if not location.split(":")[0]:
                str_tm_log = line[:int(location_right)]
            elif not location.split(":")[1]:
                str_tm_log = line[int(location_left):]
            else:
                str_tm_log = line[int(location_left):int(location_right)]
            time_now = datetime.datetime.today()
            time_log = datetime.datetime.today()
            try:
                time_log = datetime.datetime.strptime(str_tm_log, fmt.replace("/","\\"))
            except:
                pass
            delta = time_now - time_log
            # check if log is older then time ago
            # if the last line's timestamp is older than time ago
            # there's no check
            if delta > switch[time_unit](interval) or line == "break":
                break
            if datetime.timedelta(seconds=0) < delta:
                no_time_counts = 0
            if delta <= datetime.timedelta(seconds=0):
                no_time_counts = self.search_keywords(no_time_counts,keywords,line)
            num_lines_updated += 1
            # search for keywords and count
            keyword_counts = self.search_keywords(keyword_counts,keywords,line)
            if (keyword_counts - counts) == 1 and keyword_counts <= 10:
                lines = lines + line
            if num_lines_updated == 0:
                print "log has not been updated : %s" % log
            if num_lines_updated <= 10:
                lines_ok = lines_ok + line
        keyword_counts = keyword_counts - no_time_counts
        if keyword_counts == 0:
            lines = ""
        br.close()
        return keyword_counts,lines,lines_ok
        
    def check_log(self,logname,keywords,num,nums,fmt,location,status):
        resultstr = ""
        logname_list = ""
        keyword_counts = 0
        result_lines = ""
        resultstr_ok = ""
        if "*" in logname and "(new)" not in logname:
            vlogname = logname.replace('/','\\').encode('gb2312')
            cmd = 'dir /b %s' % vlogname
            try:
                res = subprocess.check_output(cmd,stderr = subprocess.STDOUT,shell = True)
            except:
                resultstr = resultstr + "ERROR: FILENAME NOT FOUND %s !\r\n" % logname
                return resultstr,resultstr_ok
            logname_list = res.split('\r\n')
            filenames = []
            logname_list.pop()
            for item in logname_list:
                filename = vlogname[0:vlogname.rfind('\\', 1) + 1] + item
                filenames.append(filename.decode('gb2312'))
            logname_list = filenames
            for log_name in logname_list:
                
                if not os.path.exists(log_name):
                    resultstr = resultstr + "ERROR: FILENAME NOT FOUND %s" % log_name
                    continue
                if not fmt and not location:
                    counts,result_line,lines_ok = self.check_log_keywords(log_name,keywords,num)
                    result_lines = result_lines + result_line
                    keyword_counts = keyword_counts + counts
                else:
                    counts,result_line,lines_ok = self.check_log_for_keywords(log_name,keywords,num,fmt,location)
                    result_lines = result_lines + result_line
                    keyword_counts = keyword_counts + counts
        else:
            if "(new)" in logname:
                logname = logname.replace("(new)","*")
                path = logname[0:logname.rfind('/', 1) + 1]
                logname = logname.replace("/","\\").encode('gb2312')
                cmd = "dir /b /O-D %s" % logname
                result = os.popen(cmd).read()
                logname = result.split("\n")[0]
                logname = (path.encode('gb2312') + logname).decode('gb2312')
            if not os.path.exists(logname):
                resultstr = "ERROR: FILENAME NOT FOUND %s \r\n" % logname
                return resultstr,resultstr_ok
            if not fmt and not location:
                keyword_counts,result_lines,lines_ok = self.check_log_keywords(logname,keywords,num)
            else:
                keyword_counts,result_lines,lines_ok = self.check_log_for_keywords(logname,keywords,num,fmt,location)
        if nums:
            errorinfo = "ERROR: CHECK LOG KEYWORD %s %s NUMBER IS %s \r\n" % (logname,keywords,keyword_counts)
            errorinfos = self.judgement(nums,errorinfo,keyword_counts)
            if errorinfos and result_lines:
                resultstr = resultstr + errorinfos + result_lines + "\r\n"
            else:
                resultstr = resultstr + errorinfos
        if status == "normal" and not nums and keyword_counts == 0:
            resultstr = resultstr + "ERROR: CHECK LOG KEYWORD %s %s NUMBER IS %s \r\n" \
            % (logname,keywords,keyword_counts)
        if status == "abnormal" and not nums and keyword_counts > 0:
            resultstr = resultstr + "ERROR: CHECK LOG KEYWORD %s %s NUMBER IS %s \r\n" \
            % (logname,keywords,keyword_counts) + result_lines
        if resultstr == "":
            resultstr_ok = "LOGNAME: %s" % logname + "\r\n" + lines_ok + "\r\n"
        return resultstr,resultstr_ok
            
    def show_log_normal(self):
        if self.normal_keywords:
            print "[%s-LOG_NORMAL]" % self.name
            print "{%s}" % self.normal_keywords
            normal_keywords = self.normal_keywords.split(';')
            logkeywordlist = []
            resultstr = ""
            resultstr_ok = ""
            for item in normal_keywords:
                logkeywordlist.append(item.split('|'))
            for logkeyword in logkeywordlist:
                logname = logkeyword[0]
                keywords = logkeyword[1]
                if len(logkeyword) == 2:
                    result_str,result_str_ok = self.check_log(logname,keywords,num = 0,nums="",fmt="",location="",status="normal")
                if len(logkeyword) == 3:
                    if not logkeyword[2]:
                        num = 0
                    else:
                        num = logkeyword[2]
                    result_str,result_str_ok = self.check_log(logname,keywords,num,nums="",fmt="",location="",status="normal")
                if len(logkeyword) == 4:
                    num = logkeyword[2]
                    if not logkeyword[2]:
                        num = 0
                    nums = logkeyword[3]
                    result_str,result_str_ok = self.check_log(logname,keywords,num,nums,fmt="",location="",status="normal")
                if len(logkeyword) >= 5:
                    nums = logkeyword[3]
                    fmt = logkeyword[4]
                    try:
                        location = logkeyword[5]
                    except:
                        resultstr = resultstr + "ERROR:PLEASE INPUT THE SIXTH PARAMETER !\r\n"
                    result_str,result_str_ok = self.check_log(logname,keywords,logkeyword[2],nums,fmt,location,status="normal")
                resultstr = resultstr + result_str
                resultstr_ok = resultstr_ok + result_str_ok
            if not resultstr:
                print "OK: CHECK OK ! \r\n"
            else:
                print resultstr
            if resultstr_ok != "":
                print resultstr_ok.encode('gbk', 'ignore')
            return resultstr
    
    def show_log_abnormal(self):
        if self.abnormal_keywords:
            print "[%s-LOG_ABNORMAL]" % self.name
            print "{%s}" % self.abnormal_keywords
            abnormal_keywords = self.abnormal_keywords.split(';')
            logkeywordlist = []
            resultstr = ""
            resultstr_ok = ""
            for item in abnormal_keywords:
                logkeywordlist.append(item.split('|'))
            for logkeyword in logkeywordlist:
                logname = logkeyword[0]
                keywords = logkeyword[1]
                if len(logkeyword) == 2:
                    result_str,result_str_ok = self.check_log(logname,keywords,num = 0,nums="",fmt="",location="",status="abnormal")
                if len(logkeyword) == 3:
                    if not logkeyword[2]:
                        num = 0
                    else:
                        num = logkeyword[2]
                    result_str,result_str_ok = self.check_log(logname,keywords,num,nums="",fmt="",location="",status="abnormal")
                if len(logkeyword) == 4:
                    num = logkeyword[2]
                    if not logkeyword[2]:
                        num = 0
                    nums = logkeyword[3]
                    result_str,result_str_ok = self.check_log(logname,keywords,num,nums,fmt="",location="",status="abnormal")
                if len(logkeyword) >= 5:
                    nums = logkeyword[3]
                    fmt = logkeyword[4]
                    try:
                        location = logkeyword[5]
                    except:
                        resultstr = resultstr + "ERROR:PLEASE INPUT THE SIXTH PARAMETER !\r\n"
                    result_str,result_str_ok = self.check_log(logname,keywords,logkeyword[2],nums,fmt,location,status="abnormal")
                resultstr = resultstr + result_str
                resultstr_ok = resultstr_ok + result_str_ok
            if not resultstr:
                print "OK: CHECK OK ! \r\n"
            else:
                print resultstr
            if resultstr_ok:
                print resultstr_ok.encode('gbk', 'ignore')
            return resultstr
            
        
    def check_ip_port_num(self,ip,ports,num,status):
        resultstr = ""
        if ip == "*":
            ip = ""
        if not num:
            num = ">0"
        for port in ports:
            if status:
                cmd = 'netstat -an|findstr %s:%s|find /i "%s"' % (ip,port,status)
            else:
                cmd = 'netstat -an|findstr %s:%s' % (ip,port)
            result = os.popen(cmd).read()
            resultnumber = result.count(port)
            errorinfo = "ERROR: IP %s PORT %s NUMBER IS %s [%s]\r\n" % (ip,port,resultnumber,num)
            resultstr = resultstr + self.judgement(num,errorinfo,resultnumber)
        return resultstr
        
    def check_ip_num(self,ip):
        resultstr = ""
        cmd = 'netstat -an|findstr "\<%s:"' % ip
        result = os.popen(cmd).read()
        resultnumber = result.count(ip)
        if resultnumber == 0:
            resultstr = resultstr + "ERROR: IP CONN %s NUMBER IS %s! \r\n" % (ip,resultnumber)
        return resultstr
        
    def check_conn_to_remote_port(self):
        if self.ip_portlist:
            print "[%s-NET_CONN]" % self.name
            print "{%s}" % self.ip_portlist
            ip_ports = []
            resultstr = ""
            for item in self.ip_portlist.split(';'):
                ip_ports.append(item.split('|'))
            for ip_port in ip_ports:
                ip_port_info = ip_port[0].split(':')
                ip = ip_port_info[0]
                if "," in ip_port_info[1:]:
                    ports = []
                    for port in ip_port_info[1:]:
                        ports.append(port)
                else:
                    if ip_port_info[1:]:
                        ports = ip_port[0].split(':')[1]
                        ports = ports.split(',')
                if ":" not in ip_port[0] and len(ip_port) == 1:
                    resultstr = resultstr + self.check_ip_num(ip)
                if len(ip_port) == 1 and ":" in ip_port[0]:
                    resultstr = resultstr + self.check_ip_port_num(ip,ports,num="",status="")
                if len(ip_port) == 2:
                    resultstr = resultstr + self.check_ip_port_num(ip,ports,ip_port[1],status="")
                if len(ip_port) == 3 and not ip_port[1]:
                    resultstr = resultstr + self.check_ip_port_num(ip,ports,ip_port[1],ip_port[2])
                if len(ip_port) == 3 and ip_port[1]:
                    resultstr = resultstr + self.check_ip_port_num(ip,ports,ip_port[1],ip_port[2])
            if resultstr != "":
                print resultstr
            else:
                print "OK: CHECK OK ! \r\n"
            return resultstr
            
    def check_ping_ip(self,ip):
        cmd = 'ping -n 2 -i 1 %s' % ip
        p = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)
        resultstr= ""
        if p.wait() != 0:
            resultstr = resultstr + "ERROR: PING %s IS FALSE !\r\n" % ip
        return resultstr
        
    def check_remote_port_state(self,address,port):
    # Create a TCP socket
        resultstr = ""
        s = socket.socket()
        s.settimeout(3)
        status = "False"
        port =int(port)
        try:
            s.connect((address, port))
            s.close()
            status = "True"
        except socket.error, e:
            logging.info(e)
            status = "False"
            s.close()
        finally:
            s.close()
        if status == "False":
            resultstr = "ERROR: CONN STATUS %s %s IS %s \r\n" % (address,port,status)
        return resultstr
                    
    def check_encrypt_port(self):
        if not self.encrypt_portlist:
            return
        resultstr = ""
        print "[%s-ENCRYPT_PORT]" % self.name
        print "{%s}" % self.encrypt_portlist
        for encrypt_port in self.encrypt_portlist.split(';'):
            ip = encrypt_port.split(':')[0]
            ports = encrypt_port.split(':')[1]
            if "," in ports:
                ports = (encrypt_port.split(":")[1]).split(",")
                for port in ports:
                    resultstr = resultstr + self.check_remote_port_state(ip,port)
            else:
                resultstr = resultstr + self.check_remote_port_state(ip,ports)
        if resultstr != "":
            print resultstr
        else:
            print "OK: CHECK OK ! \r\n"
        return resultstr
                   
    def check_ping(self):
        #127.0.0.1:1500,1501|127.0.0.2:1502,1503
        if not self.iplist:
            return
        resultstr = ""
        print "[%s-NET_PING]" % self.name
        print "{%s}" % self.iplist
        for iplist in self.iplist.split(";"):
            ip = iplist.split(":")[0]
            if "," in iplist or ":" in iplist:
                ports = (iplist.split(":")[1]).split(",")
                for port in ports:
                    resultstr = resultstr + self.check_remote_port_state(ip,port)
            if "," not in iplist and ":" not in iplist:
                resultstr = resultstr + self.check_ping_ip(ip)
        if resultstr != "":
            print resultstr
        else:
            print "OK: CHECK OK ! \r\n"
        return resultstr
        
    def check_msg(self,address, port, str_send, str_recv):
        # Create a TCP socket
        port = int(port)
        s = socket.socket()
        s.settimeout(3)
        value = False
        #
        try:
            s.connect((address, port))
            s.sendall(str_send)
            receive_data = s.recv(2048)
            s.close()
            if receive_data == str_recv:
                value = ""
        except Exception, e:
            logging.error(str(e))
        finally:
            s.close()
        if value != "":
            value = "ERROR: CHECK MSG IS FALSE"
        return value
    def show_check_msg(self):
        if self.ip_portsfok:
            print "[%s-CHECK_MSG]" % self.name
            self.ip_portsfok = self.ip_portsfok.split(';')
            checkmsglist = []
            result_str = ""
            for item in self.ip_portsfok:
                checkmsglist.append(item.split('|'))
            for checkmsg in checkmsglist:
                ip = checkmsg[0].split(':')[0]
                port = checkmsg[0].split(':')[1]
                str_send = checkmsg[1]
                str_recv = checkmsg[2]
                result_str = result_str + self.check_msg(ip,port,str_send,str_recv)
            if result_str == "":
                print "OK: CHECK OK !"
            else:
                print result_str
            return result_str
            
    def check_shared_file(self):
        if self.shared_filelist:
            print "[%s-SHARED_FILE]" % self.name
            resultstr = ""
            for shared_file in self.shared_filelist.split(','):
                if not os.path.exists(shared_file):
                    resultstr = resultstr + "ERROR: %s is not exists \n" % shared_file
                if os.path.isfile(shared_file):
                    if os.path.exists(shared_file):
                        try:
                            f = open(shared_file)
                        except:
                            resultstr = resultstr + "ERROR: %s is not exists \n" % shared_file
                        finally:
                            f.close()
            if not resultstr:
                print "OK: CHECK OK ! \n"
            else:
                print resultstr
            return resultstr
          
            
        
    def diff(self):
        if not self.consistency_files:
            return
        print "[%s-CONSISTENCY_FILE]" % self.name
        print "{%s}" % self.consistency_files
        result_str = ""
        files = self.consistency_files.split('|')
        f1, f2=str(files[0]),str(files[1])  
        try:  
            f1=open(f1, "r")  
            m=f1.readlines()  
        except IOError:  
            result_str = "ERROR: %s does not exist!" % f1
            sys.exit(2)  
        finally:  
            if f1:  
                f1.close()  
        # read lines from mids2.txt  
        try:  
            f2=open(f2, "r")
            n=f2.readlines()  
        except IOError:  
            result_str = "ERROR: %s does not exist!" % f2  
        finally:  
            if f2:  
                f2.close()  
        #filter  
        for a in m:  
            for b in n:  
                if a==b:  
                    n.remove(b)      
        for i in range(len(n)):  
            n[i]=n[i].strip()   
        if n:
            result_str = "ERROR: %s and %s are different !\r\n" % (files[0],files[1])
            print result_str
        else:
            print "OK: %s and %s are the same !\r\n" % (files[0],files[1])
        return result_str

    def showSummary(self,proc_result,port_result,port_time_wait_result,msg_result \
        ,service_result,url_result,app_pool_result,iis_status_result,runcmd_result \
        ,iis_web_result,diff_result,ping_result,net_conn_result,log_result,log_ab_result \
        ,encrypt_port_result,shared_file_result):
        proc_error = "ERROR: [%s-PROCESS]  {%s}" % (self.name,self.proclist)
        port_error = "ERROR: [%s-PORT_LISTEN]  {%s}" % (self.name,self.portlistenlist)
        port_time_wait_error = "ERROR: [%s-PORT_TIMEWAIT]  {%s}" % (self.name,self.porttimewaitlist)
        runcmd_error = "ERROR: [%s-RUNCMD]  {%s}" % (self.name,self.runcmd)
        ping_error = "ERROR: [%s-NET_PING]  {%s}" % (self.name,self.iplist)
        url_error = "ERROR: [%s-CHECK_URL]  {%s}" % (self.name,self.urllists)
        encrypt_port_error = "ERROR: [%s-ENCRYPT_PORT]  {%s}" % (self.name,self.encrypt_portlist)
        iis_status_error = "ERROR: [%s-IIS_STAUTS]  {%s}" % (self.name,self.iis_status)
        iis_web_error = "ERROR: [%s-IIS_WEB]  {%s}" % (self.name,self.iis_weblist)
        app_pool_error = "ERROR: [%s-IIS_APP]  {%s}" % (self.name,self.iis_applist)
        service_error = "ERROR: [%s-SERVICE_WIN]  {%s}" % (self.name,self.service_names)
        log_error = "ERROR: [%s-LOG_NORMAL]  {%s}" % (self.name,self.normal_keywords)
        log_ab_error = "ERROR: [%s-LOG_ABNORMAL]  {%s}" % (self.name,self.abnormal_keywords)
        msg_errorr = "ERROR: [%s-CHECK_MSG]  {%s}" % (self.name,self.ip_portsfok)
        shared_file_error = "ERROR: [%s-SHARED_FILE]  {%s}" % (self.name,self.shared_filelist)
        diff_error = "ERROR: [%s-CONSISTENCY_FILE]  {%s}" % (self.name,self.consistency_files)
        net_conn_error = "ERROR: [%s-NET_CONN]  {%s}" % (self.name,self.ip_portlist)
        error_str = "[%s-Summary]\r\n" % self.name 
        result_str = error_str
        if proc_result:
            error_str += proc_error +"\r\n"
        if port_result:
            error_str += port_error +"\r\n"
        if port_time_wait_result:
            error_str += port_time_wait_error +"\r\n"
        if net_conn_result:
            error_str += net_conn_error +"\r\n"
        if ping_result:
            error_str += ping_error +"\r\n"
        if url_result: 
            error_str += url_error +"\r\n"
        if iis_status_result: 
            error_str += iis_status_error +"\r\n"
        if iis_web_result: 
            error_str += iis_web_error +"\r\n"
        if app_pool_result: 
            error_str += app_pool_error +"\r\n"
        if encrypt_port_result:
            error_str += encrypt_port_error +"\r\n"
        if log_result: 
            error_str += log_error +"\r\n"
        if log_ab_result: 
            error_str += log_ab_error +"\r\n"
        if runcmd_result:
            error_str += runcmd_error +"\r\n"
        if service_result:
            error_str += service_error +"\r\n"
        if msg_result:
            error_str += msg_errorr +"\r\n"
        if shared_file_result:
            error_str += shared_file_error +"\r\n"
        if diff_result:
            error_str += diff_error +"\r\n"
        if error_str == result_str:
            result_str = "%s is OK !" % self.name
        else:
            result_str = error_str
        return result_str
        
    def commentlist(self,str):
        self.showStart()
        self.showStop()
        self.showcomment()
        self.showcommentfile()
        if str == "end":
            print "\r\n##CHECK_END:"+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"#"*47
        else:
            print "-"*79
        
    def global_variable(self):
        num = 1
        
    def check(self,str):
        if str == "begin":
            print "##CHECK_BEGIN:"+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"#"+sys.argv[0]+"#"+"v1.35"+"#"*16
        else:
            print "#"*79
        if self.name:
            print "[NAME] " + self.name
        else:
            return ""
        if self.path:
            print "[PATH] " + self.path
        print
        self.show_standby_mode_normal()
        proc_result = self.showProc()
        service_result = self.check_service()
        port_result = self.showPortListen()
        port_time_wait_result = self.prot_time_wait()
        net_conn_result = self.check_conn_to_remote_port()
        ping_result = self.check_ping()
        encrypt_port_result = self.check_encrypt_port()
        url_result = self.find_keyword_by_url()
        msg_result = self.show_check_msg()
        iis_status_result = self.check_iis_status()
        iis_web_result = self.check_iis_web()
        app_pool_result = self.check_app_pool()
        shared_file_result = self.check_shared_file()
        diff_result = self.diff()
        log_result = self.show_log_normal()
        log_ab_result = self.show_log_abnormal()
        runcmd_result = self.checkruncmd()
        summary = self.showSummary(proc_result,port_result,port_time_wait_result,msg_result \
        ,service_result,url_result,app_pool_result,iis_status_result,runcmd_result \
        ,iis_web_result,diff_result,ping_result,net_conn_result,log_result,log_ab_result \
        ,encrypt_port_result,shared_file_result)
        print "###############################################################################"
        return summary
        
class MyOS(object):
    def shell2(self,cmd):
        if not cmd:
            return
        output = ''
        try:
            output = subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError, e:
            logging.error(str(e))
        return output


    def check_cpu_usage(self,cpu_usage):
        print "[CHECK_CPU_USAGE]"
        cmd = 'wmic.exe cpu get LoadPercentage /every:60 /repeat:1'
        output = self.shell2(cmd)
        nums = []
        resultstr = ""
        for line in output.split('\r\n'):
            ln = [x.replace(' ', '') for x in line.rstrip('\r').split(' ') if x]
            if not ln:
                continue
            if len(ln) == 1 and ln[0].isdigit():
                nums.append(int(ln[0]))
        value = 'unchecked'
        if nums:
            value = 0
            for x in nums:
                value += x
            value = int(value / len(nums))
        if value >= cpu_usage:
            resultstr = "ERROR: cpu_usage is %s%% !\r\n" % value
            print resultstr
        else:
            print "OK: cpu_usage is %s%% !\r\n" % value
        return resultstr


    def check_disk(self,fs_usage):
        print "[CHECK_DISK]"
        cmd = 'wmic.exe path win32_logicaldisk ' +\
              'where drivetype=3 get freespace,name,size'
        output = self.shell2(cmd)
        resultstr = ""
        showdisks = ""
        m = {}
        for line in output.split('\r\n'):
            ln = [x.replace(' ', '') for x in line.rstrip('\r').split(' ') if x]
            if not len(ln) == 3:
                continue
            (free, name, size) = (ln[0], ln[1], ln[2])
            if re.match('[A-Z][:]', name):
                pc = 0.5
                if int(size) > 0:
                    pc = (int(free) * 100) / int(size)
                m[name[0]] = int(pc)
        for (disk, value) in m.items():
            key = 'disk_usage_%s' % disk
            showdisks = showdisks + key + ": " + str(100-value) + "%\r\n"
            if (100-value) >= fs_usage:
                resultstr = resultstr + "ERROR: %s IS %s !\r\n" % (key,value)
        if resultstr:
            print resultstr
        else:
            print "OK: disks_usage is OK !\r\n"
        print showdisks
        return resultstr

    def check_memory(self,mem_usage):
        print "[CHECK_MEM_USAGE]"
        (free, total) = (0, 1)
        cmd = 'wmic.exe os get FreePhysicalMemory'
        output = self.shell2(cmd)
        resultstr = ""
        for line in output.split('\r\n'):
            ln = [x.replace(' ', '') for x in line.rstrip('\r').split(' ') if x]
            if re.match('[0-9]', ln[0]):
                free = int(ln[0])
                break
        cmd = 'wmic.exe computersystem get TotalPhysicalMemory'
        output = self.shell2(cmd)
        for line in output.split('\r\n'):
            ln = [x.replace(' ', '') for x in line.rstrip('\r').split(' ') if x]
            if re.match('[0-9]', ln[0]):
                total = int(ln[0])
                break
        value = 100 - int((free * 100 * 1024) / total)
        if value >= mem_usage:
            resultstr = "ERROR: mem_usage is %s%% !\r\n" % value
            print resultstr
        else:
            print "OK: mem_usage is %s%% !\r\n" % value
        return resultstr
        
    def showSummary(self,result_cpu,result_mem,result_fs):
        cpu_error = "ERROR: [CHECKOS-CPU]"
        mem_error = "ERROR: [CHECKOS-MEM]"
        fs_error = "ERROR: [CHECKOS-DISK]"
        error_str = "[CHECKOS-Summary]\r\n"
        result_str = error_str
        if result_cpu:
            error_str += cpu_error +"\r\n"
        if result_mem:
            error_str += mem_error +"\r\n"
        if result_fs: 
            error_str += fs_error +"\r\n"
        if error_str == result_str:
            result_str = "CHECKOS IS OK !\r\n"
        else:
            result_str = error_str
        return result_str
            
    def check(self):
        print '[CHECK_OS]'
        resultstr = ""
        mem_usage = 90
        cpu_usage = 90
        fs_usage = 90
        for app_inst in self.parameter:
            if app_inst.mem_usage:
                mem_usage = app_inst.mem_usage
            if app_inst.cpu_usage:
                cpu_usage = app_inst.cpu_usage
            if app_inst.fs_usage:
                fs_usage = app_inst.fs_usage
        result_cpu = self.check_cpu_usage(cpu_usage)
        result_mem = self.check_memory(mem_usage)
        result_fs = self.check_disk(fs_usage)
        resultstr = self.showSummary(result_cpu,result_mem,result_fs)
        return resultstr
    def __init__(self, app_instlist):
        self.parameter = app_instlist
        
class CheckApp(object):
    '''
    classdocs
    '''
    def __init__(self, applist):
        '''
        Constructor
        '''
        self.app_instlist = []
        self.check_resultlist = []
        self.resultstr = ""
        self.show_resultlist = []
        self.result_os = ""
        if applist:
            for app_item in applist:
                app_inst = MyApp(app_item)
                self.app_instlist.append(app_inst)
    def action(self):
        if self.app_instlist:
            i = 0
            oscheck_status = ""
            for app_inst in self.app_instlist:
                i += 1
                if i == 1:
                    flag = "begin"
                else:
                    flag = ""
                check_result = app_inst.check(flag)
                self.check_resultlist.append(check_result)
                self.resultstr = self.resultstr + check_result
                # if app_inst.oscheck:
                    # oscheck_status = app_inst.oscheck
            # if oscheck_status != "close":
            self.result_os = self.showos()
            self.resultstr = self.resultstr + self.result_os
                
    def showSummary(self):
        if self.check_resultlist:
            for item in self.check_resultlist:
                print item
            print self.result_os
            # if "OK" in self.result_os:
            num = 0
            for app_inst in self.app_instlist:
                if app_inst.standby_mode and app_inst.standby_mode.lower() == "cold":
                    num += 1
        if "ERROR" not in self.resultstr:
            if num >= 1:
                printBlue("COLD_STANDBY !!!")
                printGreen("Everything is OK !!!")
                return 100
            else:
                printGreen("Everything is OK !!!")
                return 0
        elif num >= 1 and "ERROR" in self.resultstr:
            printBlue("COLD_STANDBY !!!")
            printRed("Something is ERROR !!!")
            return 101
        else:
            printRed("Something is ERROR !!!")
            return 1
                
    def showos(self):
        checkos = MyOS(self.app_instlist)
        result = checkos.check()
        print "#"*79
        return result
        
    def showComment(self):
        if self.app_instlist:
            num = len(self.app_instlist)
            i = 0
            for app_inst in self.app_instlist:
                i = i + 1
                if i == num:
                    flag = "end"
                else:
                    flag = ""
                app_inst.commentlist(flag)
                
if __name__ == '__main__':
    timetask()
    saveLog() # 保存近10天的日志
    check_self_proc()
    appconf_file = get_appconf()
    if not os.path.exists(appconf_file):
        print "config file not exist"
        sys.exit(1)
    s = removebom(appconf_file)
    with open(appconf_file,'w') as f:
        f.write(s)
    f = file(appconf_file)
    jsondata = json.load(f,strict=False)
    applist = jsondata["apps"]
    try:
        oslist = jsondata["os"]
        applist = applist + oslist
    except:
        oslist = ""
    myCheck = CheckApp(applist)
    myCheck.action()
    print "[Summary]"
    result = myCheck.showSummary()
    print
    print "-"*79
    print "[INFO]"
    myCheck.showComment()
    print "Auto Close after 5 minutes !!!"
    printResult(result)
    time.sleep(timesleep())
    exit(result)
    
  