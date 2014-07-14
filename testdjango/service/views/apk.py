# -*- coding: utf-8 -*-

from provisionadmin.utils.json import json_response_error, json_response_ok
from django.http import HttpResponse, HttpResponseNotFound
from django.core.servers.basehttp import FileWrapper
from provisionadmin.settings import STATIC_ROOT, CUS_TEMPLATE_DIR, HOST
from provisionadmin.utils.qrcode_generator import make_qr
import time
import os
import subprocess
import traceback


def upload(request):
    try:
        if request.method == "GET":
            return HttpResponse(file(
                os.path.join(CUS_TEMPLATE_DIR, "upload.html")).read())
        cur_time = int(time.time())
        apkfile = request.FILES['apkfile']
        xmlfile = request.FILES['xmlfile']
        apkfilepath = os.path.join(STATIC_ROOT, "apk_%s.apk" % cur_time)
        xmlfilepath = os.path.join(STATIC_ROOT, "xml_%s.zip" % cur_time)
        apkoutputfile = open(apkfilepath, "wb")
        for chunk in apkfile.chunks():
            apkoutputfile.write(chunk)
        apkoutputfile.close()
        xmloutputfile = open(xmlfilepath, "wb")
        for chunk in xmlfile.chunks():
            xmloutputfile.write(chunk)
        xmloutputfile.close()
        apkfiledir = os.path.splitext(apkfilepath)[0]
        xmlfiledir = os.path.splitext(xmlfilepath)[0]
        os.mkdir(apkfiledir)
        os.mkdir(xmlfiledir)
        print "start to un-compress the xml files"
        subprocess.call(
            "cd %s && unzip %s" % (xmlfiledir, xmlfilepath), shell=True)
        print "start to de-compile"
        subprocess.call(
            "apktool d -s -f %s %s" % (apkfilepath, apkfiledir), shell=True)
        print "start to cp&overwrite the xml files of apk dir"
        subprocess.call(
            "cd %s && cp -rf * %s" % (xmlfiledir, os.path.join(
                apkfiledir, 'res')), shell=True)
        new_apkfilepath = os.path.join(
            STATIC_ROOT, "apk_%s_new.apk" % cur_time)
        print "start to re-compile apk"
        subprocess.call(
            "apktool b %s %s" % (apkfiledir, new_apkfilepath), shell=True)
        apk_url_filepath = "/tmp/apk_url_%s.txt" % cur_time
        print "start to re-sign the new apk"
        subprocess.call(
            "curl -F \"apkfile=@%s\" "
            "http://172.16.7.25:1234/handle_sign_redirect "
            "-o %s" % (new_apkfilepath, apk_url_filepath), shell=True)
        new_apkfilepath_withsign = os.path.join(
            STATIC_ROOT, "apk_%s_new_withsign.apk" % cur_time)
        time.sleep(2)
        print "start to fetch the re-signed apk"
        subprocess.call(
            "curl -o %s " % new_apkfilepath_withsign +
            "`awk '{printf \"http://172.16.7.25:1234%s\", $1}' " +
            "%s`" % apk_url_filepath, shell=True)
        res_url = "/admin/download?file=%s" % os.path.basename(
            new_apkfilepath_withsign)
        res_img_path = os.path.join(
            STATIC_ROOT,
            os.path.splitext(os.path.basename(new_apkfilepath_withsign))[0]
            + '.jpg')
        res_img_url = "/admin/download?file=%s" % \
            os.path.basename(res_img_path)
        print "start to generate qrcode image for this new re-asigned apk"
        make_qr("%s%s" % (HOST, res_url), res_img_path)
        return HttpResponse(
            """
            下载链接： <a href="%s">here</a>
            </br>
            <image src="%s"></image>
            """ % (res_url, res_img_url)
        )
    except Exception as e:
        print e
        print traceback.format_exc()
        raise e
    # if request.FILES:
    #     print 'got upload file'
    #     for file_name in request.FILES.keys():
    #         file_obj = request.FILES[file_name]
    #         file_data = file_obj.read()
    #         print 'upload xml file %s' % file_name
    #         upload_apk(file_data)
    # else:
    #     print 'not found upload FILES!'

    return json_response_ok({})


def download(request):
    print 'into download'
    if request.method == "GET" and 'file' in request.GET:
        requested_file = os.path.join(STATIC_ROOT, request.GET['file'])
        is_apk = requested_file.endswith('.apk')
        response = HttpResponse(
            FileWrapper(file(requested_file)),
            content_type="application/vnd.android.package-archive" if is_apk
            else "image/jpeg")
        if is_apk:
            response["Content-Disposition"] = \
                "attachment; filename=\"output.apk\""
        return response
    else:
        return HttpResponseNotFound('<h1>Not Found Apk</h1>')
