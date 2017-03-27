'''
Created on Jun 18, 2015
@author: CityLinda
Launch and run BI Publisher bursting job on demand.

'''


#import libraries

from suds.client import Client
import sys


username = sys.argv[1]
password = sys.argv[2]
scheduled_service = sys.argv[3]
report_service = sys.argv[4]
report_path = sys.argv[5]
job_name = sys.argv[6] 

#WSDL URL

url_schedule_service = scheduled_service

url_report_service = report_service


scheClient=Client(url_schedule_service)
rptClient=Client(url_report_service)


#FileDataSource

fds=rptClient.factory.create('FileDataSource')
fds.dynamicDataSourcePath=''
fds.temporaryDataSource=False

#JDBCDataSource

jds=rptClient.factory.create('JDBCDataSource')
jds.JDBCDriverClass='oracle.jdbc.OracleDriver'
jds.JDBCDriverType='oracle 9i/10g/11g'


#BIPDataSource
ds=rptClient.factory.create('BIPDataSource')
ds.fileDataSource=fds
ds.JDBCDataSource=jds


#ReportRequest
rptReq=rptClient.factory.create('ReportRequest')
rptReq.byPassCache=False
rptReq.dynamicDataSource=ds
rptReq.reportAbsolutePath=report_path
rptReq.flattenXML=False
rptReq.sizeOfDataChunkDownload=0


#ScheduleRequest
schReq=scheClient.factory.create('ScheduleRequest')
schReq.bookBindingOutputOption=False
schReq.mergeOutputOption=False
schReq.notifyWhenFailed=False
schReq.notifyWhenSuccess=False
schReq.notifyHttpWhenFailed=False
schReq.notifyHttpWhenSuccess=False
schReq.notifyHttpWhenWarning=False
schReq.notifyHttpWhenSkipped=False
schReq.notifyWhenSkipped=False
schReq.notifyWhenWarning=False
schReq.notifyWhenSuccess=False
schReq.repeatCount=0
schReq.repeatInterval=10
schReq.scheduleBurstingOption=True
schReq.schedulePublicOption=True
schReq.useUTF8Option=True
schReq.reportRequest=rptReq   # report request
schReq.saveDataOption=False
schReq.saveOutputOption=False
schReq.userJobName=job_name


job_passing_id=scheClient.service.scheduleReport(schReq,username,password)



