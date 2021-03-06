#-*- coding: UTF-8 -*-
__author__ = 'yuyang'

import os
from os import path
import platform
import tornado
from shutil import copyfile
from xml.dom.minidom import Document
from Gyrfalcon.configure.GlobalConfigure import *
from Gyrfalcon.configure.Urls import urlList
from service.configure.NginxSettings import NginxSetting
from service.configure.DjangoNginxSettings import DjangoNginxSetting
from service.configure.TornadoNginxSettings import TornadoNginxSetting,tornadoUpStreamString,tornadoUpStreamName

class Server:

    def startConfigure(self):
        pass

    def startServer(self):
        pass

class ReleaseServer(Server):

    def __init__(self):
        self.nginxProjectConfPath = nginx_project_conf_path
        self.superProjectVisorProjectConfPath = path.join(service_profile_path,"supervisor")
        gfMakeDirs(self.superProjectVisorProjectConfPath)
        gfMakeDirs(os.path.join(global_nginx_path, "log/error.log"), touch_file=True)
        gfMakeDirs(os.path.join(global_nginx_path, "log/access.log"), touch_file=True)
        
        if "Ubuntu" in platform.platform():
            gfMakeDirs(os.path.join(global_nginx_path, "logs/error.log"), touch_file=True)
            gfMakeDirs(os.path.join(global_nginx_path, "logs/access.log"), touch_file=True)
        else:
            replacedText = ""
            with open(nginx_conf_template_path, "r") as f:
                import getpass
                readLines = f.readlines()
                f.seek(0)
                readString = f.read()
                orgLine = ""
                newLine = ""
                extString = ""
                for line in readLines:
                    if "user" in line:
                        orgLine = line
                        newLine = "user {user} wheel;".format(user=getpass.getuser())
                        extString = readString.split(orgLine)[-1]
                        break;

                replacedText = newLine+"\n"+extString

            with open(nginx_conf_path, "w") as f:
                f.write(replacedText)

        # 配置文件生成
        self.startConfigure()

    def nginxSetSyntax(self, key,value):
        return "map $args {key} {{ default {value}; }}\n".format(key=key ,value=value)

    def nginxSettingsConfigure(self, setting):
        return "".join([self.nginxSetSyntax(key, setting[key]) for key in setting.keys()])

    def supervisorSettingsConfugre(self, ports, groupname):
        if len(ports) == 0:
            ports = [debug_tornado_port]
        confHeaderString = "[supervisord]\nlogfile_maxbytes=50MB\nlogfile_backups=10\nlogfile={supervisor_log}\n \n\n[group:{groupname}]\nprograms={tornadoes}\n\n".format(supervisor_log=path.join(log_path,"supervisor/tornado.log"),groupname=groupname,tornadoes=",".join(["tornado-"+str(port) for port in ports]))

        programsList = [["tornado-{port}".format(port=port),self.supervisorProgramDict(port)] for port in ports]
        programsString = "\n\n".join([self.supervisorProgramSyntax(programName=programes[0],programsDict=programes[1]) for programes in programsList])

        return confHeaderString+programsString

    def supervisorProgramDict(self,port):
        gfMakeDirs(path.join(log_path,"supervisor/error.log"), touch_file=True)
        gfMakeDirs(path.join(log_path,"supervisor/out.log"), touch_file=True)
        
        return {
            "command":"python3 ".format(project_path=project_path,django_path=django_path)+path.join(subproject_path,"main/main.py")+" --port="+str(port)+" --log_file_prefix="+tornado_log_path,
            "directory":project_path,
            "user":os.environ["USER"],
            "autorestart":"true",
            "redirect_stderr":"true",
            "stdout_logfile":path.join(log_path,"supervisor/out.log"),
            "stderr_logfile":path.join(log_path,"supervisor/error.log"),
            "loglevel":"info",
            "environment":"PYTHONPATH={project_path}:{django_path},DJANGO_SETTINGS_MODULE={django_project_name}.settings".format(project_path=project_path,django_path=django_path,django_project_name=django_project_name),
        }

    def supervisorProgramSyntax(self, programName,programsDict):
        headerString = "[program:{programName}]\n".format(programName=programName)
        return headerString+"\n".join(["{key}={value}".format(key=key,value=programsDict[key]) for key in list(programsDict.keys())])

    def startConfigure(self):

        # 配置nginx
        def nginxConfigure():
            settings = [
                NginxSetting,
                DjangoNginxSetting,
                TornadoNginxSetting,
            ]

            settingsString = "".join([self.nginxSettingsConfigure(setting) for setting in settings])
            
            org_tornadoConfDefaultStringPath = path.join(nginx_project_conf_path, product_name.lower()+".conf.template")
            tornadoConfDefaultStringPath = path.join(nginx_project_conf_path,product_name.lower()+".conf.template")
            global_tornadoConfDefaultStringPath = path.join(global_nginx_project_conf_path,product_name.lower()+".conf.template")
            
            org_tornadoConfStringPath = path.join(nginx_project_conf_path, project_name.lower()+".conf")
            tornadoConfStringPath = path.join(nginx_project_conf_path, product_name.lower()+".conf")
            global_tornadoConfStringPath = path.join(global_nginx_project_conf_path, product_name.lower()+".conf")
            
            org_variable_path = path.join(nginx_project_conf_path, project_name.lower()+"_variable.conf")
            variable_path = path.join(nginx_project_conf_path, product_name.lower()+"_variable.conf")
            global_variable_path = path.join(global_nginx_project_conf_path, product_name.lower()+"_variable.conf")
            try:
                os.rename(org_tornadoConfStringPath, tornadoConfStringPath)
                os.rename(org_variable_path, variable_path)

                if os.path.exists(global_tornadoConfDefaultStringPath):
                    os.remove(global_tornadoConfDefaultStringPath)

                if os.path.exists(global_tornadoConfStringPath):
                    os.remove(global_tornadoConfStringPath)

                if os.path.exists(global_variable_path):
                    os.remove(global_variable_path)
                
                if os.path.exists(global_nginx_conf_path):
                    os.remove(global_nginx_conf_path)
                
            except:
                pass

            with open(tornadoConfDefaultStringPath,"r") as f:
                f.seek(0)
                tornadoConfDefaultString = f.read()

            with open(tornadoConfStringPath,"w") as f:
                tornadoConfString = tornadoConfDefaultString + tornadoUpStreamString
                f.write(tornadoConfString)

            with open(variable_path, "w") as f:
                f.write(settingsString)

            copyfile(tornadoConfStringPath, global_tornadoConfStringPath)
            copyfile(variable_path, global_variable_path)
            
            osname = platform.uname()[0]

            conf_string = ""
            with open(nginx_conf_path, 'r') as f:
                f.seek(0)
                conf_string = f.read()

            if conf_string != None and len(conf_string) > 0:
                if osname == "Darwin":
                    conf_string = conf_string.replace('epoll', 'kqueue')
                else:
                    conf_string = conf_string.replace('kqueue', 'epoll')

            with open(nginx_conf_path, 'w') as f:
                f.write(conf_string)

            copyfile(nginx_conf_path, global_nginx_conf_path)
            gfMakeDirs("{global_nginx_path}/nginx_params".format(global_nginx_path=global_nginx_path))
            os.system("cp -rf {nginx_path}/nginx_params/* {global_nginx_path}/nginx_params/".format(nginx_path=nginx_path, global_nginx_path=global_nginx_path))


        # 配置supervisor
        def supervisorConfigure():
            with open(path.join(self.superProjectVisorProjectConfPath,"supervisor.conf"),"w") as f:
                f.write(self.supervisorSettingsConfugre(tornado_ports,tornadoUpStreamName))

        def adminConfigure():
            admingXmlPath = os.path.join(service_profile_path, "uwsgi/"+django_project_name+"_profile.xml")
            host = django_ip
            port = release_django_port
            listen = 80
            pythonpath1 = project_path  # Gyrfalcon
            pythonpath2 = subproject_path
            pythonpath3 = subproject_path+"/main/"+django_project_name+"/"+django_project_name+"/"
            pythonpath4 = subproject_path+"/main/"+django_project_name+"/"
            pidfile = path.join(nginx_pid_path,"nginx.pid")
            limit_as = 512
            daemonize = log_path + "/django/django.log"   # logpath
            gfMakeDirs(daemonize, touch_file=True)
            childrenNodes = {
                "py-programname":"python3",
                "chdir":django_path,
                "socket":host+":"+str(port),
                "listen":str(listen),
                "master":"true",
                "pidfile":pidfile,
                "processes":"8",
                "plugin":"/usr/local/lib/uwsgi/py35_plugin.so",
                "pythonpath1":pythonpath1,
                # "pythonpath2":pythonpath2,
                "pythonpath3":pythonpath3,
                "pythonpath4":pythonpath4,
                "module":"wsgi",
                "profiler":"true",
                "memory-report":"true",
                "enable-threads":"true",
                "logdate":"true",
                "limit-as":str(limit_as),
                "daemonize":daemonize,
                }

            def adminXmlBuilder(nodes={}, rootNodeName="", xmlpath=""):

                doc = Document()
                rootNode = doc.createElement(rootNodeName)
                doc.appendChild(rootNode)
                for keyName in list(nodes.keys()):
                    if "pythonpath" in keyName:
                        keyNode = doc.createElement("pythonpath")
                        valueNode = doc.createTextNode(nodes[keyName])
                        keyNode.appendChild(valueNode)
                        rootNode.appendChild(keyNode)
                    else:
                        keyNode = doc.createElement(keyName)
                        valueNode = doc.createTextNode(nodes[keyName])
                        keyNode.appendChild(valueNode)
                        rootNode.appendChild(keyNode)

                f = open(xmlpath,'w')
                f.write(doc.toprettyxml())
                f.close()

            adminXmlBuilder(childrenNodes, "uwsgi", admingXmlPath)

        nginxConfigure()
        # supervisor配置初始化:supervisor-tornado
        supervisorConfigure()
        # admin 配置初始化:uwsgi-django
        adminConfigure()

    def startSupervisorMonitor(self):
        os.system("supervisord -c {conf_path};".format(conf_path=path.join(self.superProjectVisorProjectConfPath,"supervisor.conf")))
        # os.system("sudo supervisorctl reload")

    def startNginxService(self):

        os.system("uwsgi -x {uwsgi_conf_path};".format(uwsgi_conf_path=path.join(service_profile_path,"uwsgi/{project_name}_profile.xml".format(project_name=django_project_name))))
        # print("self.nginxConfPath:{np},nginx_path:{nginx_path}".format(np=self.nginxConfPath, nginx_path=nginx_path))
        os.system("sudo nginx -c {conf_path} -p {nginx_path}".format(conf_path=global_nginx_conf_path, nginx_path=global_nginx_path))


    def killServices(self):
        pass

    def startServer(self):
        # shell脚本启动服务
        self.killServices()
        DatabaseServer().startServer()
        self.startSupervisorMonitor()
        self.startNginxService()


class DebugServer(Server):

    def tornadoServerStart(self,port):
        application = tornado.web.Application(urlList, static_path = static_path, template_path=template_path, debug=debug)
        application.listen(port)
        tornado.ioloop.IOLoop.current().start()

    def djangoServerStart(self,port):
        manage_path = path.join(django_path, "manage.py")
        os.system("python3 {manage_path} runserver 0.0.0.0:{debug_django_port} &".format(project_path=project_path,django_path=django_path,manage_path=manage_path,debug_django_port=port))

    def startServer(self):
        #启动配置，
        DatabaseServer().startServer()
        print("============开启django测试服务============\n")
        self.djangoServerStart(debug_django_port)
        print("========http://127.0.0.1:{port}=========\n".format(port=debug_django_port))

        print("============开启tornado测试服务============\n")
        print("========http://127.0.0.1:{port}=========\n".format(port=debug_tornado_port))
        self.tornadoServerStart(debug_tornado_port)


class DatabaseServer(Server):

    def startConfigure(self):
        manage_path = path.join(django_path, "manage.py")
        os.system("python3 {manage_path} makemigrations;".format(project_path=project_path,django_path=django_path,manage_path=manage_path))
        migrateid=os.system("python3 {manage_path} migrate;".format(project_path=project_path,django_path=django_path,manage_path=manage_path))
        if migrateid != 0:
            print("输入mysql中root用户密码:")
            script = "mysql -h {dbhost} -u root -Bse \"insert into mysql.user(Host,User,Password) values('{dbhost}','{dbuser}',password('{dbpassword}'));grant all on *.* to {dbuser}@{dbhost};flush privileges;\" -p 2>/dev/null".format(dbhost=dbhost,dbname=dbname,dbuser=dbuser,dbpassword=dbpassword)
            userexist = os.system(script)
            createDBSQL = "mysql -h {dbhost} -u root -Bse \"create database if not exists {dbname} default character set utf8;grant all privileges on {dbname}.* to {dbuser}@{dbhost} identified by '{dbpassword}';flush privileges;\" -p".format(dbhost=dbhost,dbname=dbname,dbuser=dbuser,dbpassword=dbpassword)
            dbCreate = os.system(createDBSQL)
            os.system("python3 {manage_path} makemigrations;".format(project_path=project_path,django_path=django_path,manage_path=manage_path))
            makemigrateid=os.system("python3 {manage_path} migrate;".format(project_path=project_path,django_path=django_path,manage_path=manage_path))

    def startServer(self):
        self.startConfigure()

class Service:

    def start(self):
        if debug == True:
            print(" DevelopMode:  [  debug   ] ")
            DebugServer().startServer()
        else:
            print(" DevelopMode: [  release  ] ")
            ReleaseServer().startServer()
