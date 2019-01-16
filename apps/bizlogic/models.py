# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
import uuid

class BCity(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=40)  # Field name made lowercase.
    cityname = models.CharField(db_column='CITYNAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    zipcode = models.CharField(db_column='ZIPCODE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    provinceid = models.CharField(db_column='PROVINCEID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    enabled = models.IntegerField(db_column='ENABLED')  # Field name made lowercase.
    deletemark = models.IntegerField(db_column='DELETEMARK')  # Field name made lowercase.
    sortcode = models.IntegerField(db_column='SORTCODE', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    createon = models.DateTimeField(db_column='CREATEON')  # Field name made lowercase.
    createuserid = models.CharField(db_column='CREATEUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createby = models.CharField(db_column='CREATEBY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedon = models.DateTimeField(db_column='MODIFIEDON')  # Field name made lowercase.
    modifieduserid = models.CharField(db_column='MODIFIEDUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.CharField(db_column='MODIFIEDBY', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'b_city'


class BDistrict(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=40)  # Field name made lowercase.
    districtname = models.CharField(db_column='DISTRICTNAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    cityid = models.CharField(db_column='CITYID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    enabled = models.IntegerField(db_column='ENABLED')  # Field name made lowercase.
    deletemark = models.IntegerField(db_column='DELETEMARK')  # Field name made lowercase.
    sortcode = models.IntegerField(db_column='SORTCODE', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    createon = models.DateTimeField(db_column='CREATEON')  # Field name made lowercase.
    createuserid = models.CharField(db_column='CREATEUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createby = models.CharField(db_column='CREATEBY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedon = models.DateTimeField(db_column='MODIFIEDON')  # Field name made lowercase.
    modifieduserid = models.CharField(db_column='MODIFIEDUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.CharField(db_column='MODIFIEDBY', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'b_district'


class BProvince(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=40)  # Field name made lowercase.
    provincename = models.CharField(db_column='PROVINCENAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    enabled = models.IntegerField(db_column='ENABLED')  # Field name made lowercase.
    deletemark = models.IntegerField(db_column='DELETEMARK')  # Field name made lowercase.
    sortcode = models.IntegerField(db_column='SORTCODE', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    createon = models.DateTimeField(db_column='CREATEON')  # Field name made lowercase.
    createuserid = models.CharField(db_column='CREATEUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createby = models.CharField(db_column='CREATEBY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedon = models.DateTimeField(db_column='MODIFIEDON')  # Field name made lowercase.
    modifieduserid = models.CharField(db_column='MODIFIEDUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.CharField(db_column='MODIFIEDBY', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'b_province'








class Ciautotextsql(models.Model):
    tag = models.IntegerField(db_column='TAG', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    gridcolumn = models.TextField(db_column='GRIDCOLUMN', blank=True, null=True)  # Field name made lowercase.
    sql = models.CharField(db_column='SQL', max_length=255, blank=True, null=True)  # Field name made lowercase.
    comment = models.CharField(db_column='COMMENT', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CREATEDATE')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'ciautotextsql'


class Cidblinkdefine(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=40)  # Field name made lowercase.
    linkname = models.CharField(db_column='LINKNAME', max_length=50)  # Field name made lowercase.
    linktype = models.CharField(db_column='LINKTYPE', max_length=20)  # Field name made lowercase.
    linkdata = models.TextField(db_column='LINKDATA', blank=True, null=True)  # Field name made lowercase.
    deletemark = models.IntegerField(db_column='DELETEMARK')  # Field name made lowercase.
    sortcode = models.IntegerField(db_column='SORTCODE', blank=True, null=True)  # Field name made lowercase.
    enabled = models.IntegerField(db_column='ENABLED')  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    createon = models.DateTimeField(db_column='CREATEON')  # Field name made lowercase.
    createuserid = models.CharField(db_column='CREATEUSERID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    createby = models.CharField(db_column='CREATEBY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedon = models.DateTimeField(db_column='MODIFIEDON')  # Field name made lowercase.
    modifieduserid = models.CharField(db_column='MODIFIEDUSERID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.CharField(db_column='MODIFIEDBY', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'cidblinkdefine'


class Ciexception(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=40)  # Field name made lowercase.
    eventid = models.CharField(db_column='EVENTID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(db_column='CATEGORY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    priority = models.CharField(db_column='PRIORITY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    severity = models.CharField(db_column='SEVERITY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(db_column='TITLE', max_length=200, blank=True, null=True)  # Field name made lowercase.
    timestamp = models.DateTimeField(db_column='TIMESTAMP', blank=True, null=True)  # Field name made lowercase.
    machinename = models.CharField(db_column='MACHINENAME', max_length=200, blank=True, null=True)  # Field name made lowercase.
    appdomainname = models.CharField(db_column='APPDOMAINNAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    processid = models.CharField(db_column='PROCESSID', max_length=100, blank=True, null=True)  # Field name made lowercase.
    processname = models.CharField(db_column='PROCESSNAME', max_length=200, blank=True, null=True)  # Field name made lowercase.
    threadname = models.CharField(db_column='THREADNAME', max_length=200, blank=True, null=True)  # Field name made lowercase.
    win32threadid = models.CharField(db_column='WIN32THREADID', max_length=200, blank=True, null=True)  # Field name made lowercase.
    message = models.TextField(db_column='MESSAGE', blank=True, null=True)  # Field name made lowercase.
    formattedmessage = models.TextField(db_column='FORMATTEDMESSAGE', blank=True, null=True)  # Field name made lowercase.
    createon = models.DateTimeField(db_column='CREATEON', blank=True, null=True)  # Field name made lowercase.
    createuserid = models.CharField(db_column='CREATEUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createby = models.CharField(db_column='CREATEBY', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'ciexception'


class Cifile(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=40)  # Field name made lowercase.
    folderid = models.CharField(db_column='FOLDERID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    filename = models.CharField(db_column='FILENAME', max_length=200, blank=True, null=True)  # Field name made lowercase.
    filepath = models.CharField(db_column='FILEPATH', max_length=255, blank=True, null=True)  # Field name made lowercase.
    filecontent = models.BinaryField(db_column='FILECONTENT', blank=True, null=True)  # Field name made lowercase.
    filesize = models.FloatField(db_column='FILESIZE', blank=True, null=True)  # Field name made lowercase.
    imageurl = models.CharField(db_column='IMAGEURL', max_length=200, blank=True, null=True)  # Field name made lowercase.
    readcount = models.IntegerField(db_column='READCOUNT', blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(db_column='CATEGORY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    enabled = models.IntegerField(db_column='ENABLED')  # Field name made lowercase.
    sortcode = models.IntegerField(db_column='SORTCODE', blank=True, null=True)  # Field name made lowercase.
    deletemark = models.IntegerField(db_column='DELETEMARK')  # Field name made lowercase.
    createon = models.DateTimeField(db_column='CREATEON', blank=True, null=True)  # Field name made lowercase.
    createuserid = models.CharField(db_column='CREATEUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createby = models.CharField(db_column='CREATEBY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedon = models.DateTimeField(db_column='MODIFIEDON', blank=True, null=True)  # Field name made lowercase.
    modifieduserid = models.CharField(db_column='MODIFIEDUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.CharField(db_column='MODIFIEDBY', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'cifile'


class Cifolder(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=40)  # Field name made lowercase.
    parentid = models.CharField(db_column='PARENTID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    foldername = models.CharField(db_column='FOLDERNAME', max_length=200, blank=True, null=True)  # Field name made lowercase.
    statecode = models.CharField(db_column='STATECODE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sortcode = models.IntegerField(db_column='SORTCODE', blank=True, null=True)  # Field name made lowercase.
    enabled = models.IntegerField(db_column='ENABLED')  # Field name made lowercase.
    deletemark = models.IntegerField(db_column='DELETEMARK')  # Field name made lowercase.
    createon = models.DateTimeField(db_column='CREATEON')  # Field name made lowercase.
    createuserid = models.CharField(db_column='CREATEUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createby = models.CharField(db_column='CREATEBY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedon = models.DateTimeField(db_column='MODIFIEDON')  # Field name made lowercase.
    modifieduserid = models.CharField(db_column='MODIFIEDUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.CharField(db_column='MODIFIEDBY', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'cifolder'


class Ciitemdetails(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=40)  # Field name made lowercase.
    itemid = models.CharField(db_column='ITEMID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    parentid = models.CharField(db_column='PARENTID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    itemcode = models.CharField(db_column='ITEMCODE', max_length=200, blank=True, null=True)  # Field name made lowercase.
    itemname = models.CharField(db_column='ITEMNAME', max_length=200, blank=True, null=True)  # Field name made lowercase.
    itemvalue = models.CharField(db_column='ITEMVALUE', max_length=200, blank=True, null=True)  # Field name made lowercase.
    allowedit = models.IntegerField(db_column='ALLOWEDIT', blank=True, null=True)  # Field name made lowercase.
    allowdelete = models.IntegerField(db_column='ALLOWDELETE', blank=True, null=True)  # Field name made lowercase.
    ispublic = models.IntegerField(db_column='ISPUBLIC', blank=True, null=True)  # Field name made lowercase.
    enabled = models.IntegerField(db_column='ENABLED')  # Field name made lowercase.
    deletemark = models.IntegerField(db_column='DELETEMARK')  # Field name made lowercase.
    sortcode = models.IntegerField(db_column='SORTCODE', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    createon = models.DateTimeField(db_column='CREATEON')  # Field name made lowercase.
    createuserid = models.CharField(db_column='CREATEUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createby = models.CharField(db_column='CREATEBY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedon = models.DateTimeField(db_column='MODIFIEDON')  # Field name made lowercase.
    modifieduserid = models.CharField(db_column='MODIFIEDUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.CharField(db_column='MODIFIEDBY', max_length=50, blank=True, null=True)  # Field name made lowercase.

    def toJSON(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)

        d = {}
        import datetime
        for attr in fields:
            if isinstance(getattr(self, attr), datetime.datetime):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(getattr(self, attr), datetime.date):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d')
            else:
                d[attr] = getattr(self, attr)

        import json
        return json.dumps(d)

    class Meta:
        managed = True
        db_table = 'ciitemdetails'


class Ciitems(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=40)  # Field name made lowercase.
    parentid = models.CharField(db_column='PARENTID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    code = models.CharField(db_column='CODE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fullname = models.CharField(db_column='FULLNAME', max_length=200, blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(db_column='CATEGORY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    targettable = models.CharField(db_column='TARGETTABLE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    istree = models.IntegerField(db_column='ISTREE', blank=True, null=True)  # Field name made lowercase.
    useitemcode = models.CharField(db_column='USEITEMCODE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    useitemname = models.CharField(db_column='USEITEMNAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    useitemvalue = models.CharField(db_column='USEITEMVALUE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    allowedit = models.IntegerField(db_column='ALLOWEDIT')  # Field name made lowercase.
    allowdelete = models.IntegerField(db_column='ALLOWDELETE')  # Field name made lowercase.
    deletemark = models.IntegerField(db_column='DELETEMARK')  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    enabled = models.IntegerField(db_column='ENABLED')  # Field name made lowercase.
    sortcode = models.IntegerField(db_column='SORTCODE', blank=True, null=True)  # Field name made lowercase.
    createon = models.DateTimeField(db_column='CREATEON')  # Field name made lowercase.
    createuserid = models.CharField(db_column='CREATEUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createby = models.CharField(db_column='CREATEBY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedon = models.DateTimeField(db_column='MODIFIEDON')  # Field name made lowercase.
    modifieduserid = models.CharField(db_column='MODIFIEDUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.CharField(db_column='MODIFIEDBY', max_length=50, blank=True, null=True)  # Field name made lowercase.

    def toJSON(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)

        d = {}
        import datetime
        for attr in fields:
            if isinstance(getattr(self, attr), datetime.datetime):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(getattr(self, attr), datetime.date):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d')
            else:
                d[attr] = getattr(self, attr)

        import json
        return json.dumps(d)

    class Meta:
        managed = True
        db_table = 'ciitems'


class Cilog(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=40)  # Field name made lowercase.
    processid = models.CharField(db_column='PROCESSID', max_length=100, blank=True, null=True)  # Field name made lowercase.
    processname = models.CharField(db_column='PROCESSNAME', max_length=200, blank=True, null=True)  # Field name made lowercase.
    methodengname = models.CharField(db_column='METHODENGNAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    methodname = models.CharField(db_column='METHODNAME', max_length=200, blank=True, null=True)  # Field name made lowercase.
    parameters = models.CharField(db_column='PARAMETERS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    userrealname = models.CharField(db_column='USERREALNAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ipaddress = models.CharField(db_column='IPADDRESS', max_length=50, blank=True, null=True)  # Field name made lowercase.
    weburl = models.CharField(db_column='WEBURL', max_length=255, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    createon = models.DateTimeField(db_column='CREATEON')  # Field name made lowercase.
    createuserid = models.CharField(db_column='CREATEUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createby = models.CharField(db_column='CREATEBY', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'cilog'


class Cimessage(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=40)  # Field name made lowercase.
    parentid = models.CharField(db_column='PARENTID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    functioncode = models.CharField(db_column='FUNCTIONCODE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    categorycode = models.CharField(db_column='CATEGORYCODE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    objectid = models.CharField(db_column='OBJECTID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(db_column='TITLE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    msgcontent = models.CharField(db_column='MSGCONTENT', max_length=255, blank=True, null=True)  # Field name made lowercase.
    receiverid = models.CharField(db_column='RECEIVERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    receiverrealname = models.CharField(db_column='RECEIVERREALNAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    isnew = models.IntegerField(db_column='ISNEW', blank=True, null=True)  # Field name made lowercase.
    readcount = models.IntegerField(db_column='READCOUNT', blank=True, null=True)  # Field name made lowercase.
    readdate = models.DateTimeField(db_column='READDATE', blank=True, null=True)  # Field name made lowercase.
    targeturl = models.CharField(db_column='TARGETURL', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ipaddress = models.CharField(db_column='IPADDRESS', max_length=50, blank=True, null=True)  # Field name made lowercase.
    deletemark = models.IntegerField(db_column='DELETEMARK')  # Field name made lowercase.
    enabled = models.IntegerField(db_column='ENABLED')  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=200, blank=True, null=True)  # Field name made lowercase.
    sortcode = models.IntegerField(db_column='SORTCODE', blank=True, null=True)  # Field name made lowercase.
    createon = models.DateTimeField(db_column='CREATEON')  # Field name made lowercase.
    createuserid = models.CharField(db_column='CREATEUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createby = models.CharField(db_column='CREATEBY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedon = models.DateTimeField(db_column='MODIFIEDON')  # Field name made lowercase.
    modifieduserid = models.CharField(db_column='MODIFIEDUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.CharField(db_column='MODIFIEDBY', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'cimessage'


class Ciparameter(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=40)  # Field name made lowercase.
    categorykey = models.CharField(db_column='CATEGORYKEY', max_length=100, blank=True, null=True)  # Field name made lowercase.
    parameterid = models.CharField(db_column='PARAMETERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    parametercode = models.CharField(db_column='PARAMETERCODE', max_length=200, blank=True, null=True)  # Field name made lowercase.
    parametercontent = models.CharField(db_column='PARAMETERCONTENT', max_length=255, blank=True, null=True)  # Field name made lowercase.
    worked = models.IntegerField(db_column='WORKED', blank=True, null=True)  # Field name made lowercase.
    enabled = models.IntegerField(db_column='ENABLED')  # Field name made lowercase.
    allowedit = models.IntegerField(db_column='ALLOWEDIT')  # Field name made lowercase.
    allowdelete = models.IntegerField(db_column='ALLOWDELETE')  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sortcode = models.IntegerField(db_column='SORTCODE', blank=True, null=True)  # Field name made lowercase.
    deletemark = models.IntegerField(db_column='DELETEMARK')  # Field name made lowercase.
    createon = models.DateTimeField(db_column='CREATEON')  # Field name made lowercase.
    createuserid = models.CharField(db_column='CREATEUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createby = models.CharField(db_column='CREATEBY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedon = models.DateTimeField(db_column='MODIFIEDON')  # Field name made lowercase.
    modifieduserid = models.CharField(db_column='MODIFIEDUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.CharField(db_column='MODIFIEDBY', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'ciparameter'


class Cisequence(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=40)  # Field name made lowercase.
    fullname = models.CharField(db_column='FULLNAME', max_length=200, blank=True, null=True)  # Field name made lowercase.
    prefix = models.CharField(db_column='PREFIX', max_length=50, blank=True, null=True)  # Field name made lowercase.
    separate = models.CharField(db_column='SEPARATE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sequence = models.IntegerField(db_column='SEQUENCE', blank=True, null=True)  # Field name made lowercase.
    reduction = models.IntegerField(db_column='REDUCTION', blank=True, null=True)  # Field name made lowercase.
    step = models.IntegerField(db_column='STEP', blank=True, null=True)  # Field name made lowercase.
    deletemark = models.IntegerField(db_column='DELETEMARK')  # Field name made lowercase.
    createon = models.DateTimeField(db_column='CREATEON')  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'cisequence'


class Citablecolumns(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=40)  # Field name made lowercase.
    tablecode = models.CharField(db_column='TABLECODE', max_length=200, blank=True, null=True)  # Field name made lowercase.
    tablename = models.CharField(db_column='TABLENAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    columncode = models.CharField(db_column='COLUMNCODE', max_length=200, blank=True, null=True)  # Field name made lowercase.
    columnname = models.CharField(db_column='COLUMNNAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ispublic = models.IntegerField(db_column='ISPUBLIC')  # Field name made lowercase.
    columnaccess = models.IntegerField(db_column='COLUMNACCESS')  # Field name made lowercase.
    columnedit = models.IntegerField(db_column='COLUMNEDIT')  # Field name made lowercase.
    columndeney = models.IntegerField(db_column='COLUMNDENEY')  # Field name made lowercase.
    useconstraint = models.IntegerField(db_column='USECONSTRAINT')  # Field name made lowercase.
    datatype = models.CharField(db_column='DATATYPE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    targettable = models.CharField(db_column='TARGETTABLE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    issearchcolumn = models.IntegerField(db_column='ISSEARCHCOLUMN')  # Field name made lowercase.
    isexhibitcolumn = models.IntegerField(db_column='ISEXHIBITCOLUMN')  # Field name made lowercase.
    enabled = models.IntegerField(db_column='ENABLED')  # Field name made lowercase.
    allowedit = models.IntegerField(db_column='ALLOWEDIT')  # Field name made lowercase.
    allowdelete = models.IntegerField(db_column='ALLOWDELETE')  # Field name made lowercase.
    deletemark = models.IntegerField(db_column='DELETEMARK')  # Field name made lowercase.
    sortcode = models.IntegerField(db_column='SORTCODE', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    createon = models.DateTimeField(db_column='CREATEON', blank=True, null=True)  # Field name made lowercase.
    createuserid = models.CharField(db_column='CREATEUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createby = models.CharField(db_column='CREATEBY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedon = models.DateTimeField(db_column='MODIFIEDON', blank=True, null=True)  # Field name made lowercase.
    modifieduserid = models.CharField(db_column='MODIFIEDUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.CharField(db_column='MODIFIEDBY', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'citablecolumns'


class Dboperationdetaillog(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=40)  # Field name made lowercase.
    dboperationlogid = models.CharField(db_column='DBOPERATIONLOGID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    tablename = models.CharField(db_column='TABLENAME', max_length=128, blank=True, null=True)  # Field name made lowercase.
    tableprimarykey = models.CharField(db_column='TABLEPRIMARYKEY', max_length=30, blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(db_column='DESCRIPTION', blank=True, null=True)  # Field name made lowercase.
    operationtype = models.CharField(db_column='OPERATIONTYPE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    flag = models.IntegerField(db_column='FLAG', blank=True, null=True)  # Field name made lowercase.
    operadate = models.DateTimeField(db_column='OPERADATE')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'dboperationdetaillog'


class Dboperationlog(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=40)  # Field name made lowercase.
    logdate = models.DateTimeField(db_column='LOGDATE')  # Field name made lowercase.
    operator = models.CharField(db_column='OPERATOR', max_length=50, blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='NOTE', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'dboperationlog'


class Pimodule(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=40)  # Field name made lowercase.
    parentid = models.CharField(db_column='PARENTID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    code = models.CharField(db_column='CODE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fullname = models.CharField(db_column='FULLNAME', max_length=200)  # Field name made lowercase.
    category = models.CharField(db_column='CATEGORY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    moduletype = models.IntegerField(db_column='MODULETYPE')  # Field name made lowercase.
    imageindex = models.CharField(db_column='IMAGEINDEX', max_length=50, blank=True, null=True)  # Field name made lowercase.
    selectedimageindex = models.CharField(db_column='SELECTEDIMAGEINDEX', max_length=50, blank=True, null=True)  # Field name made lowercase.
    iconcss = models.CharField(db_column='ICONCSS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    iconurl = models.CharField(db_column='ICONURL', max_length=255, blank=True, null=True)  # Field name made lowercase.
    navigateurl = models.CharField(db_column='NAVIGATEURL', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mvcnavigateurl = models.CharField(db_column='MVCNAVIGATEURL', max_length=255, blank=True, null=True)  # Field name made lowercase.
    target = models.CharField(db_column='TARGET', max_length=100, blank=True, null=True)  # Field name made lowercase.
    formname = models.CharField(db_column='FORMNAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    assemblyname = models.CharField(db_column='ASSEMBLYNAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    permissionitemcode = models.CharField(db_column='PERMISSIONITEMCODE', max_length=50)  # Field name made lowercase.
    permissionscopetables = models.CharField(db_column='PERMISSIONSCOPETABLES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ispublic = models.IntegerField(db_column='ISPUBLIC')  # Field name made lowercase.
    ismenu = models.IntegerField(db_column='ISMENU')  # Field name made lowercase.
    expand = models.IntegerField(db_column='EXPAND')  # Field name made lowercase.
    allowedit = models.IntegerField(db_column='ALLOWEDIT')  # Field name made lowercase.
    allowdelete = models.IntegerField(db_column='ALLOWDELETE')  # Field name made lowercase.
    sortcode = models.IntegerField(db_column='SORTCODE', blank=True, null=True)  # Field name made lowercase.
    deletemark = models.IntegerField(db_column='DELETEMARK')  # Field name made lowercase.
    enabled = models.IntegerField(db_column='ENABLED')  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    createon = models.DateTimeField(db_column='CREATEON')  # Field name made lowercase.
    createuserid = models.CharField(db_column='CREATEUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createby = models.CharField(db_column='CREATEBY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedon = models.DateTimeField(db_column='MODIFIEDON')  # Field name made lowercase.
    modifieduserid = models.CharField(db_column='MODIFIEDUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.CharField(db_column='MODIFIEDBY', max_length=50, blank=True, null=True)  # Field name made lowercase.

    def toJSON(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)

        d = {}
        import datetime
        for attr in fields:
            if isinstance(getattr(self, attr), datetime.datetime):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(getattr(self, attr), datetime.date):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d')
            else:
                d[attr] = getattr(self, attr)

        import json
        return json.dumps(d)

    class Meta:
        managed = True
        db_table = 'pimodule'


class Piorganize(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=40)  # Field name made lowercase.
    parentid = models.CharField(db_column='PARENTID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    code = models.CharField(db_column='CODE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    shortname = models.CharField(db_column='SHORTNAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fullname = models.CharField(db_column='FULLNAME', max_length=200, blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(db_column='CATEGORY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    outerphone = models.CharField(db_column='OUTERPHONE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    innerphone = models.CharField(db_column='INNERPHONE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fax = models.CharField(db_column='FAX', max_length=50, blank=True, null=True)  # Field name made lowercase.
    postalcode = models.CharField(db_column='POSTALCODE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='ADDRESS', max_length=200, blank=True, null=True)  # Field name made lowercase.
    web = models.CharField(db_column='WEB', max_length=200, blank=True, null=True)  # Field name made lowercase.
    managerid = models.CharField(db_column='MANAGERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    manager = models.CharField(db_column='MANAGER', max_length=50, blank=True, null=True)  # Field name made lowercase.
    assistantmanagerid = models.CharField(db_column='ASSISTANTMANAGERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    assistantmanager = models.CharField(db_column='ASSISTANTMANAGER', max_length=50, blank=True, null=True)  # Field name made lowercase.
    layer = models.IntegerField(db_column='LAYER', blank=True, null=True)  # Field name made lowercase.
    isinnerorganize = models.IntegerField(db_column='ISINNERORGANIZE')  # Field name made lowercase.
    bank = models.CharField(db_column='BANK', max_length=50, blank=True, null=True)  # Field name made lowercase.
    bankaccount = models.CharField(db_column='BANKACCOUNT', max_length=50, blank=True, null=True)  # Field name made lowercase.
    deletemark = models.IntegerField(db_column='DELETEMARK')  # Field name made lowercase.
    enabled = models.IntegerField(db_column='ENABLED')  # Field name made lowercase.
    sortcode = models.IntegerField(db_column='SORTCODE', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    createon = models.DateTimeField(db_column='CREATEON')  # Field name made lowercase.
    createuserid = models.CharField(db_column='CREATEUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createby = models.CharField(db_column='CREATEBY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedon = models.DateTimeField(db_column='MODIFIEDON')  # Field name made lowercase.
    modifieduserid = models.CharField(db_column='MODIFIEDUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.CharField(db_column='MODIFIEDBY', max_length=50, blank=True, null=True)  # Field name made lowercase.

    def toJSON(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)

        d = {}
        import datetime
        for attr in fields:
            if isinstance(getattr(self, attr), datetime.datetime):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(getattr(self, attr), datetime.date):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d')
            else:
                d[attr] = getattr(self, attr)

        import json
        return json.dumps(d)

    class Meta:
        managed = True
        db_table = 'piorganize'


class Pipermission(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=40)  # Field name made lowercase.
    resourcecategory = models.CharField(db_column='RESOURCECATEGORY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    resourceid = models.CharField(db_column='RESOURCEID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    permissionid = models.CharField(db_column='PERMISSIONID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    permissionconstraint = models.CharField(db_column='PERMISSIONCONSTRAINT', max_length=255, blank=True, null=True)  # Field name made lowercase.
    enabled = models.IntegerField(db_column='ENABLED', blank=True, null=True)  # Field name made lowercase.
    deletemark = models.IntegerField(db_column='DELETEMARK', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    createon = models.DateTimeField(db_column='CREATEON')  # Field name made lowercase.
    createby = models.CharField(db_column='CREATEBY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createuserid = models.CharField(db_column='CREATEUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedon = models.DateTimeField(db_column='MODIFIEDON')  # Field name made lowercase.
    modifiedby = models.CharField(db_column='MODIFIEDBY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifieduserid = models.CharField(db_column='MODIFIEDUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'pipermission'


class Pipermissionitem(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=40)  # Field name made lowercase.
    parentid = models.CharField(db_column='PARENTID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    moduleid = models.CharField(db_column='MODULEID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    code = models.CharField(db_column='CODE', max_length=50)  # Field name made lowercase.
    fullname = models.CharField(db_column='FULLNAME', max_length=50)  # Field name made lowercase.
    categorycode = models.CharField(db_column='CATEGORYCODE', max_length=50, default='Application')  # Field name made lowercase.
    isscope = models.IntegerField(db_column='ISSCOPE', default=0)  # Field name made lowercase.
    ispublic = models.IntegerField(db_column='ISPUBLIC', default=0)  # Field name made lowercase.
    allowedit = models.IntegerField(db_column='ALLOWEDIT', default=1)  # Field name made lowercase.
    allowdelete = models.IntegerField(db_column='ALLOWDELETE', default=1)  # Field name made lowercase.
    jsevent = models.CharField(db_column='JSEVENT', max_length=100, blank=True, null=True)  # Field name made lowercase.
    lastcall = models.DateTimeField(db_column='LASTCALL', blank=True, null=True)  # Field name made lowercase.
    issplit = models.IntegerField(db_column='ISSPLIT', default=0)  # Field name made lowercase.
    enabled = models.IntegerField(db_column='ENABLED', default=1)  # Field name made lowercase.
    deletemark = models.IntegerField(db_column='DELETEMARK', default=0)  # Field name made lowercase.
    sortcode = models.IntegerField(db_column='SORTCODE', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    createon = models.DateTimeField(db_column='CREATEON')  # Field name made lowercase.
    createuserid = models.CharField(db_column='CREATEUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createby = models.CharField(db_column='CREATEBY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedon = models.DateTimeField(db_column='MODIFIEDON')  # Field name made lowercase.
    modifieduserid = models.CharField(db_column='MODIFIEDUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.CharField(db_column='MODIFIEDBY', max_length=50, blank=True, null=True)  # Field name made lowercase.

    def toJSON(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)

        d = {}
        import datetime
        for attr in fields:
            if isinstance(getattr(self, attr), datetime.datetime):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(getattr(self, attr), datetime.date):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d')
            else:
                d[attr] = getattr(self, attr)

        import json
        return json.dumps(d)

    class Meta:
        managed = True
        db_table = 'pipermissionitem'


class Pipermissionscope(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=40)  # Field name made lowercase.
    resourcecategory = models.CharField(db_column='RESOURCECATEGORY', max_length=50)  # Field name made lowercase.
    resourceid = models.CharField(db_column='RESOURCEID', max_length=50)  # Field name made lowercase.
    targetcategory = models.CharField(db_column='TARGETCATEGORY', max_length=50)  # Field name made lowercase.
    targetid = models.CharField(db_column='TARGETID', max_length=50)  # Field name made lowercase.
    permissionid = models.CharField(db_column='PERMISSIONID', max_length=40)  # Field name made lowercase.
    permissionconstraint = models.CharField(db_column='PERMISSIONCONSTRAINT', max_length=200, blank=True, null=True)  # Field name made lowercase.
    startdate = models.DateTimeField(db_column='STARTDATE', blank=True, null=True)  # Field name made lowercase.
    enddate = models.DateTimeField(db_column='ENDDATE', blank=True, null=True)  # Field name made lowercase.
    enabled = models.IntegerField(db_column='ENABLED', blank=True, null=True)  # Field name made lowercase.
    deletemark = models.IntegerField(db_column='DELETEMARK', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    createon = models.DateTimeField(db_column='CREATEON', blank=True, null=True)  # Field name made lowercase.
    createby = models.CharField(db_column='CREATEBY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createuserid = models.CharField(db_column='CREATEUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedon = models.DateTimeField(db_column='MODIFIEDON', blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.CharField(db_column='MODIFIEDBY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifieduserid = models.CharField(db_column='MODIFIEDUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'pipermissionscope'


class Piplatformaddin(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=40)  # Field name made lowercase.
    guid = models.CharField(db_column='GUID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    assemblyname = models.CharField(db_column='ASSEMBLYNAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    classname = models.CharField(db_column='CLASSNAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    addin = models.TextField(db_column='ADDIN', blank=True, null=True)  # Field name made lowercase.
    addinsize = models.FloatField(db_column='ADDINSIZE', blank=True, null=True)  # Field name made lowercase.
    version = models.CharField(db_column='VERSION', max_length=30, blank=True, null=True)  # Field name made lowercase.
    developer = models.CharField(db_column='DEVELOPER', max_length=255, blank=True, null=True)  # Field name made lowercase.
    downloadcount = models.IntegerField(db_column='DOWNLOADCOUNT', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    enabled = models.IntegerField(db_column='ENABLED', blank=True, null=True)  # Field name made lowercase.
    deletemark = models.IntegerField(db_column='DELETEMARK', blank=True, null=True)  # Field name made lowercase.
    createon = models.DateTimeField(db_column='CREATEON')  # Field name made lowercase.
    createuserid = models.CharField(db_column='CREATEUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createby = models.CharField(db_column='CREATEBY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedon = models.DateTimeField(db_column='MODIFIEDON')  # Field name made lowercase.
    modifieduserid = models.CharField(db_column='MODIFIEDUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.CharField(db_column='MODIFIEDBY', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'piplatformaddin'


class Pirole(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=40)  # Field name made lowercase.
    organizeid = models.CharField(db_column='ORGANIZEID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    systemid = models.CharField(db_column='SYSTEMID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(db_column='CATEGORY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    code = models.CharField(db_column='CODE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    realname = models.CharField(db_column='REALNAME', max_length=200, blank=True, null=True)  # Field name made lowercase.
    allowedit = models.IntegerField(db_column='ALLOWEDIT')  # Field name made lowercase.
    allowdelete = models.IntegerField(db_column='ALLOWDELETE')  # Field name made lowercase.
    sortcode = models.IntegerField(db_column='SORTCODE', blank=True, null=True)  # Field name made lowercase.
    deletemark = models.IntegerField(db_column='DELETEMARK')  # Field name made lowercase.
    enabled = models.IntegerField(db_column='ENABLED')  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=200, blank=True, null=True)  # Field name made lowercase.
    createon = models.DateTimeField(db_column='CREATEON')  # Field name made lowercase.
    createuserid = models.CharField(db_column='CREATEUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createby = models.CharField(db_column='CREATEBY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedon = models.DateTimeField(db_column='MODIFIEDON')  # Field name made lowercase.
    modifieduserid = models.CharField(db_column='MODIFIEDUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.CharField(db_column='MODIFIEDBY', max_length=50, blank=True, null=True)  # Field name made lowercase.

    def toJSON(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)
        try:
            getattr(self, 'users')
            fields.append('users')
        except:
            pass
        d = {}
        import datetime
        for attr in fields:
            if isinstance(getattr(self, attr), datetime.datetime):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(getattr(self, attr), datetime.date):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d')
            else:
                d[attr] = getattr(self, attr)
        import json
        return json.dumps(d)

    class Meta:
        managed = True
        db_table = 'pirole'


class Pistaff(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, default=uuid.uuid1(), max_length=40)  # Field name made lowercase.
    code = models.CharField(db_column='CODE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    userid = models.CharField(db_column='USERID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='USERNAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    realname = models.CharField(db_column='REALNAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dutyid = models.CharField(db_column='DUTYID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(db_column='GENDER', max_length=6)  # Field name made lowercase.
    birthday = models.DateTimeField(db_column='BIRTHDAY', blank=True, null=True)  # Field name made lowercase.
    age = models.CharField(db_column='AGE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    identificationcode = models.CharField(db_column='IDENTIFICATIONCODE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    idcard = models.CharField(db_column='IDCARD', max_length=50, blank=True, null=True)  # Field name made lowercase.
    bankcode = models.CharField(db_column='BANKCODE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='EMAIL', max_length=200, blank=True, null=True)  # Field name made lowercase.
    mobile = models.CharField(db_column='MOBILE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    shortnumber = models.CharField(db_column='SHORTNUMBER', max_length=50, blank=True, null=True)  # Field name made lowercase.
    telephone = models.CharField(db_column='TELEPHONE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    qicq = models.CharField(db_column='QICQ', max_length=50, blank=True, null=True)  # Field name made lowercase.
    officephone = models.CharField(db_column='OFFICEPHONE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    officezipcode = models.CharField(db_column='OFFICEZIPCODE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    officeaddress = models.CharField(db_column='OFFICEADDRESS', max_length=200, blank=True, null=True)  # Field name made lowercase.
    officefax = models.CharField(db_column='OFFICEFAX', max_length=50, blank=True, null=True)  # Field name made lowercase.
    homephone = models.CharField(db_column='HOMEPHONE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    education = models.CharField(db_column='EDUCATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    school = models.CharField(db_column='SCHOOL', max_length=50, blank=True, null=True)  # Field name made lowercase.
    degree = models.CharField(db_column='DEGREE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(db_column='TITLE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    titledate = models.DateTimeField(db_column='TITLEDATE', blank=True, null=True)  # Field name made lowercase.
    titlelevel = models.CharField(db_column='TITLELEVEL', max_length=50, blank=True, null=True)  # Field name made lowercase.
    workingdate = models.DateTimeField(db_column='WORKINGDATE', blank=True, null=True)  # Field name made lowercase.
    joinindate = models.DateTimeField(db_column='JOININDATE', blank=True, null=True)  # Field name made lowercase.
    homezipcode = models.CharField(db_column='HOMEZIPCODE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    homeaddress = models.CharField(db_column='HOMEADDRESS', max_length=200, blank=True, null=True)  # Field name made lowercase.
    homefax = models.CharField(db_column='HOMEFAX', max_length=50, blank=True, null=True)  # Field name made lowercase.
    nativeplace = models.CharField(db_column='NATIVEPLACE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    party = models.CharField(db_column='PARTY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    nation = models.CharField(db_column='NATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    nationality = models.CharField(db_column='NATIONALITY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    major = models.CharField(db_column='MAJOR', max_length=100, blank=True, null=True)  # Field name made lowercase.
    workingproperty = models.CharField(db_column='WORKINGPROPERTY', max_length=100, blank=True, null=True)  # Field name made lowercase.
    competency = models.CharField(db_column='COMPETENCY', max_length=100, blank=True, null=True)  # Field name made lowercase.
    isdimission = models.IntegerField(db_column='ISDIMISSION')  # Field name made lowercase.
    dimissiondate = models.DateTimeField(db_column='DIMISSIONDATE', blank=True, null=True)  # Field name made lowercase.
    dimissioncause = models.CharField(db_column='DIMISSIONCAUSE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    dimissionwhither = models.CharField(db_column='DIMISSIONWHITHER', max_length=100, blank=True, null=True)  # Field name made lowercase.
    enabled = models.IntegerField(db_column='ENABLED')  # Field name made lowercase.
    deletemark = models.IntegerField(db_column='DELETEMARK')  # Field name made lowercase.
    sortcode = models.IntegerField(db_column='SORTCODE', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    createon = models.DateTimeField(db_column='CREATEON')  # Field name made lowercase.
    createuserid = models.CharField(db_column='CREATEUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createby = models.CharField(db_column='CREATEBY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedon = models.DateTimeField(db_column='MODIFIEDON')  # Field name made lowercase.
    modifieduserid = models.CharField(db_column='MODIFIEDUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.CharField(db_column='MODIFIEDBY', max_length=50, blank=True, null=True)  # Field name made lowercase.

    def toJSON(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)

        d = {}
        import datetime
        for attr in fields:
            if isinstance(getattr(self, attr), datetime.datetime):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(getattr(self, attr), datetime.date):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d')
            else:
                d[attr] = getattr(self, attr)

        import json
        return json.dumps(d)

    class Meta:
        managed = True
        db_table = 'pistaff'


class Pistafforganize(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, default=uuid.uuid4(), max_length=40)  # Field name made lowercase.
    staffid = models.CharField(db_column='STAFFID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    organizeid = models.CharField(db_column='ORGANIZEID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    enabled = models.IntegerField(db_column='ENABLED', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    deletemark = models.IntegerField(db_column='DELETEMARK', blank=True, null=True)  # Field name made lowercase.
    createon = models.DateTimeField(db_column='CREATEON')  # Field name made lowercase.
    createuserid = models.CharField(db_column='CREATEUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createby = models.CharField(db_column='CREATEBY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedon = models.DateTimeField(db_column='MODIFIEDON')  # Field name made lowercase.
    modifieduserid = models.CharField(db_column='MODIFIEDUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.CharField(db_column='MODIFIEDBY', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'pistafforganize'


class Pitablepermissionscope(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=40)  # Field name made lowercase.
    parentid = models.CharField(db_column='PARENTID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    itemcode = models.CharField(db_column='ITEMCODE', max_length=40, blank=True, null=True)  # Field name made lowercase.
    itemname = models.CharField(db_column='ITEMNAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    itemvalue = models.CharField(db_column='ITEMVALUE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    enabled = models.IntegerField(db_column='ENABLED')  # Field name made lowercase.
    ispublic = models.IntegerField(db_column='ISPUBLIC')  # Field name made lowercase.
    allowedit = models.IntegerField(db_column='ALLOWEDIT')  # Field name made lowercase.
    allowdelete = models.IntegerField(db_column='ALLOWDELETE')  # Field name made lowercase.
    deletemark = models.IntegerField(db_column='DELETEMARK')  # Field name made lowercase.
    sortcode = models.IntegerField(db_column='SORTCODE', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    createon = models.DateTimeField(db_column='CREATEON', blank=True, null=True)  # Field name made lowercase.
    createuserid = models.CharField(db_column='CREATEUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createby = models.CharField(db_column='CREATEBY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedon = models.DateTimeField(db_column='MODIFIEDON', blank=True, null=True)  # Field name made lowercase.
    modifieduserid = models.CharField(db_column='MODIFIEDUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.CharField(db_column='MODIFIEDBY', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'pitablepermissionscope'


class Piuser(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=40)  # Field name made lowercase.
    #id = models.UUIDField(db_column='ID', primary_key=True, max_length=40, auto_created=True, default=uuid.uuid4, editable=False)
    code = models.CharField(db_column='CODE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='USERNAME', max_length=50)  # Field name made lowercase.
    realname = models.CharField(db_column='REALNAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    nickname = models.CharField(db_column='NICKNAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    quickquery = models.CharField(db_column='QUICKQUERY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    roleid = models.CharField(db_column='ROLEID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    companyid = models.CharField(db_column='COMPANYID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    companyname = models.CharField(db_column='COMPANYNAME', max_length=200, blank=True, null=True)  # Field name made lowercase.
    subcompanyid = models.CharField(db_column='SUBCOMPANYID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    subcompanyname = models.CharField(db_column='SUBCOMPANYNAME', max_length=200, blank=True, null=True)  # Field name made lowercase.
    departmentid = models.CharField(db_column='DEPARTMENTID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    departmentname = models.CharField(db_column='DEPARTMENTNAME', max_length=200, blank=True, null=True)  # Field name made lowercase.
    subdepartmentid = models.CharField(db_column='SUBDEPARTMENTID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    subdepartmentname = models.CharField(db_column='SUBDEPARTMENTNAME', max_length=200, blank=True, null=True)  # Field name made lowercase.
    workgroupid = models.CharField(db_column='WORKGROUPID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    workgroupname = models.CharField(db_column='WORKGROUPNAME', max_length=200, blank=True, null=True)  # Field name made lowercase.
    workcategory = models.CharField(db_column='WORKCATEGORY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    securitylevel = models.IntegerField(db_column='SECURITYLEVEL', blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(db_column='TITLE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    duty = models.CharField(db_column='DUTY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='EMAIL', max_length=200, blank=True, null=True)  # Field name made lowercase.
    lang = models.CharField(db_column='LANG', max_length=50, blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(db_column='GENDER', max_length=6, blank=True, null=True)  # Field name made lowercase.
    birthday = models.DateTimeField(db_column='BIRTHDAY', blank=True, null=True)  # Field name made lowercase.
    mobile = models.CharField(db_column='MOBILE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    telephone = models.CharField(db_column='TELEPHONE', max_length=30, blank=True, null=True)  # Field name made lowercase.
    qicq = models.CharField(db_column='QICQ', max_length=50, blank=True, null=True)  # Field name made lowercase.
    signature = models.CharField(db_column='SIGNATURE', max_length=200, blank=True, null=True)  # Field name made lowercase.
    theme = models.CharField(db_column='THEME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    isstaff = models.IntegerField(db_column='ISSTAFF')  # Field name made lowercase.
    isvisible = models.IntegerField(db_column='ISVISIBLE')  # Field name made lowercase.
    auditstatus = models.CharField(db_column='AUDITSTATUS', max_length=50, blank=True, null=True)  # Field name made lowercase.
    homeaddress = models.CharField(db_column='HOMEADDRESS', max_length=200, blank=True, null=True)  # Field name made lowercase.
    useraddress = models.CharField(db_column='USERADDRESS', max_length=200, blank=True, null=True)  # Field name made lowercase.
    isdimission = models.IntegerField(db_column='ISDIMISSION')  # Field name made lowercase.
    dimissiondate = models.DateTimeField(db_column='DIMISSIONDATE', blank=True, null=True)  # Field name made lowercase.
    dimissioncause = models.CharField(db_column='DIMISSIONCAUSE', max_length=800, blank=True, null=True)  # Field name made lowercase.
    dimissionwhither = models.CharField(db_column='DIMISSIONWHITHER', max_length=200, blank=True, null=True)  # Field name made lowercase.
    deletemark = models.IntegerField(db_column='DELETEMARK')  # Field name made lowercase.
    enabled = models.IntegerField(db_column='ENABLED')  # Field name made lowercase.
    sortcode = models.IntegerField(db_column='SORTCODE', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    createon = models.DateTimeField(db_column='CREATEON')  # Field name made lowercase.
    createuserid = models.CharField(db_column='CREATEUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createby = models.CharField(db_column='CREATEBY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedon = models.DateTimeField(db_column='MODIFIEDON', blank=True, null=True)  # Field name made lowercase.
    modifieduserid = models.CharField(db_column='MODIFIEDUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.CharField(db_column='MODIFIEDBY', max_length=50, blank=True, null=True)  # Field name made lowercase.

    def toJSON(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)

        d = {}
        import datetime
        for attr in fields:
            if isinstance(getattr(self, attr), datetime.datetime):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(getattr(self, attr), datetime.date):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d')
            else:
                d[attr] = getattr(self, attr)

        import json
        return json.dumps(d)

    class Meta:
        managed = True
        db_table = 'piuser'


class PiuserV27(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=40)  # Field name made lowercase.
    code = models.CharField(db_column='CODE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='USERNAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    realname = models.CharField(db_column='REALNAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    roleid = models.CharField(db_column='ROLEID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    userfrom = models.CharField(db_column='USERFROM', max_length=50, blank=True, null=True)  # Field name made lowercase.
    workcategory = models.CharField(db_column='WORKCATEGORY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    companyid = models.CharField(db_column='COMPANYID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    companyname = models.CharField(db_column='COMPANYNAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    departmentid = models.CharField(db_column='DEPARTMENTID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    departmentname = models.CharField(db_column='DEPARTMENTNAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    workgroupid = models.CharField(db_column='WORKGROUPID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    workgroupname = models.CharField(db_column='WORKGROUPNAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(db_column='GENDER', max_length=6, blank=True, null=True)  # Field name made lowercase.
    mobile = models.CharField(db_column='MOBILE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    telephone = models.CharField(db_column='TELEPHONE', max_length=30, blank=True, null=True)  # Field name made lowercase.
    birthday = models.DateTimeField(db_column='BIRTHDAY')  # Field name made lowercase.
    duty = models.CharField(db_column='DUTY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(db_column='TITLE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    userpassword = models.CharField(db_column='USERPASSWORD', max_length=200, blank=True, null=True)  # Field name made lowercase.
    changepassworddate = models.DateTimeField(db_column='CHANGEPASSWORDDATE')  # Field name made lowercase.
    qicq = models.CharField(db_column='QICQ', max_length=50, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='EMAIL', max_length=200, blank=True, null=True)  # Field name made lowercase.
    lang = models.CharField(db_column='LANG', max_length=50, blank=True, null=True)  # Field name made lowercase.
    theme = models.CharField(db_column='THEME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    allowstarttime = models.DateTimeField(db_column='ALLOWSTARTTIME')  # Field name made lowercase.
    allowendtime = models.DateTimeField(db_column='ALLOWENDTIME')  # Field name made lowercase.
    lockstartdate = models.DateTimeField(db_column='LOCKSTARTDATE')  # Field name made lowercase.
    lockenddate = models.DateTimeField(db_column='LOCKENDDATE')  # Field name made lowercase.
    firstvisit = models.DateTimeField(db_column='FIRSTVISIT')  # Field name made lowercase.
    previousvisit = models.DateTimeField(db_column='PREVIOUSVISIT')  # Field name made lowercase.
    lastvisit = models.DateTimeField(db_column='LASTVISIT')  # Field name made lowercase.
    logoncount = models.IntegerField(db_column='LOGONCOUNT', blank=True, null=True)  # Field name made lowercase.
    isstaff = models.IntegerField(db_column='ISSTAFF', blank=True, null=True)  # Field name made lowercase.
    auditstatus = models.CharField(db_column='AUDITSTATUS', max_length=50, blank=True, null=True)  # Field name made lowercase.
    isvisible = models.IntegerField(db_column='ISVISIBLE', blank=True, null=True)  # Field name made lowercase.
    useronline = models.IntegerField(db_column='USERONLINE', blank=True, null=True)  # Field name made lowercase.
    ipaddress = models.CharField(db_column='IPADDRESS', max_length=50, blank=True, null=True)  # Field name made lowercase.
    macaddress = models.CharField(db_column='MACADDRESS', max_length=50, blank=True, null=True)  # Field name made lowercase.
    homeaddress = models.CharField(db_column='HOMEADDRESS', max_length=200, blank=True, null=True)  # Field name made lowercase.
    openid = models.CharField(db_column='OPENID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    question = models.CharField(db_column='QUESTION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    answerquestion = models.CharField(db_column='ANSWERQUESTION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    useraddress = models.CharField(db_column='USERADDRESS', max_length=200, blank=True, null=True)  # Field name made lowercase.
    deletemark = models.IntegerField(db_column='DELETEMARK', blank=True, null=True)  # Field name made lowercase.
    enabled = models.IntegerField(db_column='ENABLED', blank=True, null=True)  # Field name made lowercase.
    sortcode = models.IntegerField(db_column='SORTCODE', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    createon = models.DateTimeField(db_column='CREATEON')  # Field name made lowercase.
    createuserid = models.CharField(db_column='CREATEUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createby = models.CharField(db_column='CREATEBY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedon = models.DateTimeField(db_column='MODIFIEDON')  # Field name made lowercase.
    modifieduserid = models.CharField(db_column='MODIFIEDUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.CharField(db_column='MODIFIEDBY', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'piuser_v27'


class Piuserlogon(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=40)  # Field name made lowercase.
    userfrom = models.CharField(db_column='USERFROM', max_length=50, blank=True, null=True)  # Field name made lowercase.
    userpassword = models.CharField(db_column='USERPASSWORD', max_length=200, blank=True, null=True)  # Field name made lowercase.
    openid = models.CharField(db_column='OPENID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    allowstarttime = models.DateTimeField(db_column='ALLOWSTARTTIME', blank=True, null=True)  # Field name made lowercase.
    allowendtime = models.DateTimeField(db_column='ALLOWENDTIME', blank=True, null=True)  # Field name made lowercase.
    lockstartdate = models.DateTimeField(db_column='LOCKSTARTDATE', blank=True, null=True)  # Field name made lowercase.
    lockenddate = models.DateTimeField(db_column='LOCKENDDATE', blank=True, null=True)  # Field name made lowercase.
    firstvisit = models.DateTimeField(db_column='FIRSTVISIT', blank=True, null=True)  # Field name made lowercase.
    previousvisit = models.DateTimeField(db_column='PREVIOUSVISIT', blank=True, null=True)  # Field name made lowercase.
    lastvisit = models.DateTimeField(db_column='LASTVISIT', blank=True, null=True)  # Field name made lowercase.
    changepassworddate = models.DateTimeField(db_column='CHANGEPASSWORDDATE', blank=True, null=True)  # Field name made lowercase.
    multiuserlogin = models.IntegerField(db_column='MULTIUSERLOGIN', blank=True, null=True)  # Field name made lowercase.
    logoncount = models.IntegerField(db_column='LOGONCOUNT', blank=True, null=True)  # Field name made lowercase.
    passworderrorcount = models.IntegerField(db_column='PASSWORDERRORCOUNT', blank=True, null=True)  # Field name made lowercase.
    useronline = models.IntegerField(db_column='USERONLINE')  # Field name made lowercase.
    checkipaddress = models.IntegerField(db_column='CHECKIPADDRESS', blank=True, null=True)  # Field name made lowercase.
    ipaddress = models.CharField(db_column='IPADDRESS', max_length=50, blank=True, null=True)  # Field name made lowercase.
    macaddress = models.CharField(db_column='MACADDRESS', max_length=50, blank=True, null=True)  # Field name made lowercase.
    question = models.CharField(db_column='QUESTION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    answerquestion = models.CharField(db_column='ANSWERQUESTION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createon = models.DateTimeField(db_column='CREATEON')  # Field name made lowercase.
    createuserid = models.CharField(db_column='CREATEUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createby = models.CharField(db_column='CREATEBY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedon = models.DateTimeField(db_column='MODIFIEDON')  # Field name made lowercase.
    modifieduserid = models.CharField(db_column='MODIFIEDUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.CharField(db_column='MODIFIEDBY', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'piuserlogon'


class Piuserorganize(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=40)  # Field name made lowercase.
    userid = models.CharField(db_column='USERID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    companyid = models.CharField(db_column='COMPANYID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    subcompanyid = models.CharField(db_column='SUBCOMPANYID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    departmentid = models.CharField(db_column='DEPARTMENTID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    subdepartmentid = models.CharField(db_column='SUBDEPARTMENTID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    workgroupid = models.CharField(db_column='WORKGROUPID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    roleid = models.CharField(db_column='ROLEID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    enabled = models.IntegerField(db_column='ENABLED')  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    deletemark = models.IntegerField(db_column='DELETEMARK', blank=True, null=True)  # Field name made lowercase.
    createon = models.DateTimeField(db_column='CREATEON')  # Field name made lowercase.
    createuserid = models.CharField(db_column='CREATEUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createby = models.CharField(db_column='CREATEBY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedon = models.DateTimeField(db_column='MODIFIEDON')  # Field name made lowercase.
    modifieduserid = models.CharField(db_column='MODIFIEDUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.CharField(db_column='MODIFIEDBY', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'piuserorganize'


class Piuserrole(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=40)  # Field name made lowercase.
    userid = models.CharField(db_column='USERID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    roleid = models.CharField(db_column='ROLEID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    enabled = models.IntegerField(db_column='ENABLED')  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    deletemark = models.IntegerField(db_column='DELETEMARK')  # Field name made lowercase.
    createon = models.DateTimeField(db_column='CREATEON')  # Field name made lowercase.
    createuserid = models.CharField(db_column='CREATEUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createby = models.CharField(db_column='CREATEBY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedon = models.DateTimeField(db_column='MODIFIEDON')  # Field name made lowercase.
    modifieduserid = models.CharField(db_column='MODIFIEDUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.CharField(db_column='MODIFIEDBY', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'piuserrole'


class Queryengine(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=40)  # Field name made lowercase.
    parentid = models.CharField(db_column='PARENTID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    code = models.CharField(db_column='CODE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fullname = models.CharField(db_column='FULLNAME', max_length=200, blank=True, null=True)  # Field name made lowercase.
    allowedit = models.IntegerField(db_column='ALLOWEDIT')  # Field name made lowercase.
    allowdelete = models.IntegerField(db_column='ALLOWDELETE')  # Field name made lowercase.
    deletemark = models.IntegerField(db_column='DELETEMARK')  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    enabled = models.IntegerField(db_column='ENABLED')  # Field name made lowercase.
    sortcode = models.IntegerField(db_column='SORTCODE', blank=True, null=True)  # Field name made lowercase.
    createon = models.DateTimeField(db_column='CREATEON')  # Field name made lowercase.
    createuserid = models.CharField(db_column='CREATEUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createby = models.CharField(db_column='CREATEBY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedon = models.DateTimeField(db_column='MODIFIEDON')  # Field name made lowercase.
    modifieduserid = models.CharField(db_column='MODIFIEDUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.CharField(db_column='MODIFIEDBY', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'queryengine'


class Queryenginedefine(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=40)  # Field name made lowercase.
    queryengineid = models.CharField(db_column='QUERYENGINEID', max_length=40, blank=True, null=True)  # Field name made lowercase.
    code = models.CharField(db_column='CODE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fullname = models.CharField(db_column='FULLNAME', max_length=200, blank=True, null=True)  # Field name made lowercase.
    databaselinkname = models.CharField(db_column='DATABASELINKNAME', max_length=200, blank=True, null=True)  # Field name made lowercase.
    datasourcetype = models.IntegerField(db_column='DATASOURCETYPE')  # Field name made lowercase.
    datasourcename = models.CharField(db_column='DATASOURCENAME', max_length=200, blank=True, null=True)  # Field name made lowercase.
    querystringkey = models.CharField(db_column='QUERYSTRINGKEY', max_length=200, blank=True, null=True)  # Field name made lowercase.
    selectedfield = models.CharField(db_column='SELECTEDFIELD', max_length=255, blank=True, null=True)  # Field name made lowercase.
    orderbyfield = models.CharField(db_column='ORDERBYFIELD', max_length=200, blank=True, null=True)  # Field name made lowercase.
    querystring = models.CharField(db_column='QUERYSTRING', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    allowedit = models.IntegerField(db_column='ALLOWEDIT')  # Field name made lowercase.
    allowdelete = models.IntegerField(db_column='ALLOWDELETE')  # Field name made lowercase.
    deletemark = models.IntegerField(db_column='DELETEMARK')  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    enabled = models.IntegerField(db_column='ENABLED')  # Field name made lowercase.
    sortcode = models.IntegerField(db_column='SORTCODE', blank=True, null=True)  # Field name made lowercase.
    createon = models.DateTimeField(db_column='CREATEON')  # Field name made lowercase.
    createuserid = models.CharField(db_column='CREATEUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createby = models.CharField(db_column='CREATEBY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedon = models.DateTimeField(db_column='MODIFIEDON')  # Field name made lowercase.
    modifieduserid = models.CharField(db_column='MODIFIEDUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.CharField(db_column='MODIFIEDBY', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'queryenginedefine'


class TbLeave(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=40)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    departmentname = models.CharField(db_column='DEPARTMENTNAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    leavetype = models.CharField(db_column='LEAVETYPE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cause = models.CharField(db_column='CAUSE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    leaveperiod = models.CharField(db_column='LEAVEPERIOD', max_length=50, blank=True, null=True)  # Field name made lowercase.
    departmentopinion = models.CharField(db_column='DEPARTMENTOPINION', max_length=200, blank=True, null=True)  # Field name made lowercase.
    leaderopinion = models.CharField(db_column='LEADEROPINION', max_length=200, blank=True, null=True)  # Field name made lowercase.
    deletemark = models.SmallIntegerField(db_column='DELETEMARK')  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=200, blank=True, null=True)  # Field name made lowercase.
    createon = models.DateTimeField(db_column='CREATEON')  # Field name made lowercase.
    createuserid = models.CharField(db_column='CREATEUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createby = models.CharField(db_column='CREATEBY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedon = models.DateTimeField(db_column='MODIFIEDON')  # Field name made lowercase.
    modifieduserid = models.CharField(db_column='MODIFIEDUSERID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.CharField(db_column='MODIFIEDBY', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'tb_leave'


class ZdNationcode(models.Model):
    code = models.CharField(db_column='CODE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=24, blank=True, null=True)  # Field name made lowercase.
    py_code = models.CharField(db_column='PY_CODE', max_length=8, blank=True, null=True)  # Field name made lowercase.
    wb_code = models.CharField(db_column='WB_CODE', max_length=8, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'zd_nationcode'
