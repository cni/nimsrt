#!/usr/bin/python
import re
from datetime import datetime
# iterate search, use match.end() to get next start pos, use .groupdict() to get dict
DATE = '(?P<datetime>(?:[a-zA-Z]{3} ){2}\d{2} \d{4}\n\d{2}:\d{2}:\d{2}.\d{3})\s+'
DATE_FORMAT_IN = '%a %b %d %Y\n%H:%M:%S.%f'
DATE_FORMAT_OUT = '%Y%m%d%H%M%S%f'
RE_EXAM_PREP = re.compile(DATE + 'LxSessionProvider : Got Request \[readyForNewExam\]\n') # datetime
RE_EXAM_NAME = re.compile(DATE + 'LxSession createNewExam sessionName \[(?P<exam_name>.+?)\]\n') # datetime, exam_name
RE_EXAM_NUMBER = re.compile(DATE + 'LxSession::sendStudyNumber \[(?P<study_id>\d+)\]\n') # datetime, study_id
RE_TASK_NAME = re.compile(DATE + 'LxTask CreateTask Name\[(?P<task_name>.+)\], Type\[\d+\], index\[\d+\] BEGIN\n') # datetime, task_name
RE_TASK_DIR = re.compile(DATE + 'DVMR: node->Task Dir Name\[.+\] node->FileName\[(?P<task_file>.+?)\]\n') # datetime, task_file
RE_DBDT_ACCEPT = re.compile(DATE + 'LxSession onRequest SarDbDtInfo SarMode\[\d+\], DbdtMode\[\d+\]\n') # datetime
RE_LANDMARK_PATINFO = re.compile(DATE + 'PublishLandmark \[LandmarkData: value=\d+ uid=\d+(?:\.\d+)* ' \
    + 'patid=(?P<patient_id>.+) patent=.+ patpos=.+ exist=\d+ state=\d+\]\n') # datetime, patient_id
RE_SERIES_NUM = re.compile(DATE + 'Sending startAlloc\(\d+\) \[exam:(?P<study_id>\d+), ser:(?P<series_num>\d+)\]\n') # datetime, study_id
RE_SERIES_NAME = re.compile(DATE + 'sendSeriesInfo No\[(?P<series_num>\d+)\], UID\[\d+(?:\.\d+)*\], Desc\[(?P<series_desc>.+?)\]\n') # datetime, series_num, series_desc
RE_TEMP = re.compile(DATE + 'FindScanRoomTemperature: Got Scan Room Temperature \[(?P<room_temp>\d+)\]\n') # datetime, room_temp
RE_SCAN_PREP = re.compile(DATE + 'LxTask\[0x[a-fA-F0-9]+\] Name\[(?P<series_desc>.+?)\] onRequest\[scanStart\] BEGIN\n') # datetime, series_desc
RE_FIRST_IMAGE = re.compile(DATE + 'Got First Image Available for exam\[(?P<study_id>\d+)\], series\[(?P<series_num>\d+)\]\n') # datetime, study_id, series_num 
RE_FIRST_IMAGE_PATH = re.compile(DATE + 'path->exam_path of image: (?P<path>.+?)\n') # datetime, path
RE_SCAN_START = re.compile(DATE + 'Sending start scan\(\d+\)\n') # datetime
RE_SCAN_END = re.compile(DATE + 'Entry gotScanStopped\n') # datetime
RE_EXAM_END = re.compile(DATE + '...operator confirmed \[End Exam\]\n') # datetime

def ProcessEvent(string, eventList, compiledRegExpr, name):
    searchFromIndex = 0
    while True:
        matchObject = compiledRegExpr.search(string, searchFromIndex) 
        if not matchObject:
            break
        resultDict = matchObject.groupdict()
        resultDateTime = datetime.strptime(resultDict['datetime'], DATE_FORMAT_IN) 
        resultDict['datetime'] = int(resultDateTime.strftime(DATE_FORMAT_OUT))
        searchFromIndex = matchObject.end()
        eventList.append((name, resultDict))

def ParseLog(string):
    eventList = []
    ProcessEvent(string, eventList, RE_EXAM_PREP, 'EXAM_PREP')
    ProcessEvent(string, eventList, RE_EXAM_NAME, 'EXAM_NAME')
    ProcessEvent(string, eventList, RE_EXAM_NUMBER, 'EXAM_NUMBER')
    ProcessEvent(string, eventList, RE_TASK_NAME, 'TASK_NAME')
    ProcessEvent(string, eventList, RE_TASK_DIR, 'TASK_DIR')
    ProcessEvent(string, eventList, RE_DBDT_ACCEPT, 'DBDT_ACCEPT')
    ProcessEvent(string, eventList, RE_LANDMARK_PATINFO, 'LANDMARK_PATINFO')
    ProcessEvent(string, eventList, RE_SERIES_NUM, 'SERIES_NUM')
    ProcessEvent(string, eventList, RE_TEMP, 'TEMP')
    ProcessEvent(string, eventList, RE_SCAN_PREP, 'SCAN_PREP')
    ProcessEvent(string, eventList, RE_FIRST_IMAGE, 'FIRST_IMAGE')
    ProcessEvent(string, eventList, RE_FIRST_IMAGE_PATH, 'FIRST_IMAGE_PATH')
    ProcessEvent(string, eventList, RE_SCAN_START, 'SCAN_START')
    ProcessEvent(string, eventList, RE_SCAN_END, 'SCAN_END')
    ProcessEvent(string, eventList, RE_EXAM_END, 'EXAM_END')
    return eventList
