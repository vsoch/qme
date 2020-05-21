Search.setIndex({docnames:["changelog","index","source/modules","source/qme","source/qme.app","source/qme.app.views","source/qme.client","source/qme.logger","source/qme.main","source/qme.main.config","source/qme.main.database","source/qme.main.executor","source/qme.utils"],envversion:{"sphinx.domains.c":1,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":1,"sphinx.domains.javascript":1,"sphinx.domains.math":2,"sphinx.domains.python":1,"sphinx.domains.rst":1,"sphinx.domains.std":1,"sphinx.ext.intersphinx":1,"sphinx.ext.todo":2,"sphinx.ext.viewcode":1,sphinx:56},filenames:["changelog.md","index.rst","source/modules.rst","source/qme.rst","source/qme.app.rst","source/qme.app.views.rst","source/qme.client.rst","source/qme.logger.rst","source/qme.main.rst","source/qme.main.config.rst","source/qme.main.database.rst","source/qme.main.executor.rst","source/qme.utils.rst"],objects:{"":{qme:[3,0,0,"-"]},"qme.app":{config:[4,0,0,"-"],server:[4,0,0,"-"],views:[5,0,0,"-"]},"qme.app.server":{QueueMeServer:[4,1,1,""],start:[4,2,1,""]},"qme.app.views":{executors:[5,0,0,"-"],main:[5,0,0,"-"]},"qme.app.views.executors":{shell_executor:[5,2,1,""]},"qme.app.views.main":{delete_row:[5,2,1,""],index:[5,2,1,""],rerun_row:[5,2,1,""],update_connect:[5,2,1,""],update_database:[5,2,1,""],update_disconnect:[5,2,1,""]},"qme.client":{clear:[6,0,0,"-"],config:[6,0,0,"-"],get:[6,0,0,"-"],get_parser:[6,2,1,""],listing:[6,0,0,"-"],main:[6,2,1,""],run:[6,0,0,"-"],start:[6,0,0,"-"]},"qme.client.clear":{main:[6,2,1,""]},"qme.client.config":{main:[6,2,1,""]},"qme.client.get":{main:[6,2,1,""]},"qme.client.listing":{main:[6,2,1,""]},"qme.client.run":{rerun:[6,2,1,""],run:[6,2,1,""]},"qme.client.start":{main:[6,2,1,""]},"qme.defaults":{getenv:[3,2,1,""]},"qme.logger":{message:[7,0,0,"-"],namer:[7,0,0,"-"],progress:[7,0,0,"-"],spinner:[7,0,0,"-"]},"qme.logger.message":{QueueMeMessage:[7,1,1,""],convert2boolean:[7,2,1,""],get_logging_level:[7,2,1,""],get_user_color_preference:[7,2,1,""]},"qme.logger.message.QueueMeMessage":{abort:[7,3,1,""],addColor:[7,3,1,""],critical:[7,3,1,""],custom:[7,3,1,""],debug:[7,3,1,""],emit:[7,3,1,""],emitError:[7,3,1,""],emitOutput:[7,3,1,""],error:[7,3,1,""],exit:[7,3,1,""],exit_info:[7,3,1,""],failure:[7,3,1,""],get_logs:[7,3,1,""],info:[7,3,1,""],isEnabledFor:[7,3,1,""],is_quiet:[7,3,1,""],log:[7,3,1,""],newline:[7,3,1,""],show_progress:[7,3,1,""],spinner:[7,4,1,""],success:[7,3,1,""],table:[7,3,1,""],useColor:[7,3,1,""],verbose1:[7,3,1,""],verbose2:[7,3,1,""],verbose3:[7,3,1,""],verbose:[7,3,1,""],warning:[7,3,1,""],write:[7,3,1,""]},"qme.logger.namer":{RobotNamer:[7,1,1,""],main:[7,2,1,""]},"qme.logger.namer.RobotNamer":{generate:[7,3,1,""]},"qme.logger.progress":{ProgressBar:[7,1,1,""],bar:[7,2,1,""]},"qme.logger.progress.ProgressBar":{done:[7,3,1,""],format_time:[7,3,1,""],show:[7,3,1,""]},"qme.logger.spinner":{Spinner:[7,1,1,""]},"qme.logger.spinner.Spinner":{balloons_cursor:[7,3,1,""],changing_arrows:[7,3,1,""],delay:[7,4,1,""],run:[7,3,1,""],select_generator:[7,3,1,""],spinning:[7,4,1,""],spinning_cursor:[7,3,1,""],start:[7,3,1,""],stop:[7,3,1,""]},"qme.main":{Queue:[8,1,1,""],config:[9,0,0,"-"],database:[10,0,0,"-"],executor:[11,0,0,"-"]},"qme.main.Queue":{clear:[8,3,1,""],get:[8,3,1,""],initdb:[8,3,1,""],list:[8,3,1,""],rerun:[8,3,1,""],run:[8,3,1,""]},"qme.main.config":{Config:[9,1,1,""]},"qme.main.config.Config":{get:[9,3,1,""],read:[9,3,1,""],save:[9,3,1,""],update:[9,3,1,""]},"qme.main.database":{base:[10,0,0,"-"],filesystem:[10,0,0,"-"],init_db:[10,2,1,""],models:[10,0,0,"-"],relational:[10,0,0,"-"],sqlite:[10,0,0,"-"]},"qme.main.database.base":{Database:[10,1,1,""]},"qme.main.database.base.Database":{add_task:[10,3,1,""],clear:[10,3,1,""],database:[10,4,1,""],delete_executor:[10,3,1,""],delete_task:[10,3,1,""],get_task:[10,3,1,""],iter_executors:[10,3,1,""],list_tasks:[10,3,1,""],update_task:[10,3,1,""]},"qme.main.database.filesystem":{FileSystemDatabase:[10,1,1,""],FileSystemTask:[10,1,1,""]},"qme.main.database.filesystem.FileSystemDatabase":{add_task:[10,3,1,""],clear:[10,3,1,""],create_database:[10,3,1,""],database:[10,4,1,""],delete_executor:[10,3,1,""],delete_task:[10,3,1,""],get_task:[10,3,1,""],iter_executors:[10,3,1,""],list_tasks:[10,3,1,""],update_task:[10,3,1,""]},"qme.main.database.filesystem.FileSystemTask":{"export":[10,3,1,""],create:[10,3,1,""],executor_dir:[10,3,1,""],filename:[10,3,1,""],load:[10,3,1,""],save:[10,3,1,""],summary:[10,3,1,""],update:[10,3,1,""]},"qme.main.database.models":{Task:[10,1,1,""],TaskData:[10,1,1,""]},"qme.main.database.models.Task":{"export":[10,3,1,""],command:[10,4,1,""],data:[10,4,1,""],executor_name:[10,4,1,""],load:[10,3,1,""],summary:[10,3,1,""],taskid:[10,4,1,""],timestamp:[10,4,1,""]},"qme.main.database.models.TaskData":{data:[10,4,1,""],id:[10,4,1,""],task:[10,4,1,""],taskid:[10,4,1,""],timestamp:[10,4,1,""]},"qme.main.database.relational":{RelationalDatabase:[10,1,1,""]},"qme.main.database.relational.RelationalDatabase":{add_task:[10,3,1,""],clear:[10,3,1,""],create_database:[10,3,1,""],delete_executor:[10,3,1,""],delete_task:[10,3,1,""],get_task:[10,3,1,""],iter_executors:[10,3,1,""],list_tasks:[10,3,1,""],update_task:[10,3,1,""]},"qme.main.database.sqlite":{SqliteDatabase:[10,1,1,""]},"qme.main.database.sqlite.SqliteDatabase":{database:[10,4,1,""]},"qme.main.executor":{base:[11,0,0,"-"],get_executor:[11,2,1,""],get_named_executor:[11,2,1,""],shell:[11,0,0,"-"]},"qme.main.executor.base":{Capturing:[11,1,1,""],ExecutorBase:[11,1,1,""]},"qme.main.executor.base.Capturing":{cleanup:[11,3,1,""],err:[11,3,1,""],out:[11,3,1,""],set_stderr:[11,3,1,""],set_stdout:[11,3,1,""]},"qme.main.executor.base.ExecutorBase":{"export":[11,3,1,""],command:[11,3,1,""],execute:[11,3,1,""],get_error:[11,3,1,""],get_output:[11,3,1,""],name:[11,4,1,""],summary:[11,3,1,""]},"qme.main.executor.shell":{ShellExecutor:[11,1,1,""]},"qme.main.executor.shell.ShellExecutor":{"export":[11,3,1,""],command:[11,3,1,""],decode:[11,3,1,""],execute:[11,3,1,""],get_error:[11,3,1,""],get_output:[11,3,1,""],name:[11,4,1,""],reset:[11,3,1,""],set_command:[11,3,1,""],summary:[11,3,1,""]},"qme.utils":{command:[12,0,0,"-"],file:[12,0,0,"-"],prompt:[12,0,0,"-"],regex:[12,0,0,"-"]},"qme.utils.command":{Capturing:[12,1,1,""],QueueMeCommand:[12,1,1,""]},"qme.utils.command.Capturing":{cleanup:[12,3,1,""],err:[12,3,1,""],out:[12,3,1,""],set_stderr:[12,3,1,""],set_stdout:[12,3,1,""]},"qme.utils.command.QueueMeCommand":{decode:[12,3,1,""],execute:[12,3,1,""],get_error:[12,3,1,""],get_output:[12,3,1,""],returnCode:[12,3,1,""],set_command:[12,3,1,""]},"qme.utils.file":{get_latest_modified:[12,2,1,""],get_tmpdir:[12,2,1,""],get_tmpfile:[12,2,1,""],get_user:[12,2,1,""],get_userhome:[12,2,1,""],mkdir_p:[12,2,1,""],read_file:[12,2,1,""],read_json:[12,2,1,""],recursive_find:[12,2,1,""],save_pickle:[12,2,1,""],write_json:[12,2,1,""]},"qme.utils.prompt":{confirm:[12,2,1,""]},qme:{app:[4,0,0,"-"],client:[6,0,0,"-"],defaults:[3,0,0,"-"],logger:[7,0,0,"-"],main:[8,0,0,"-"],utils:[12,0,0,"-"],version:[3,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","class","Python class"],"2":["py","function","Python function"],"3":["py","method","Python method"],"4":["py","attribute","Python attribute"]},objtypes:{"0":"py:module","1":"py:class","2":"py:function","3":"py:method","4":"py:attribute"},terms:{"95m":7,"boolean":7,"char":7,"class":[4,7,8,9,10,11,12],"default":[0,1,2,7,8,9,10,11,12],"export":[10,11],"function":[4,5,7,8,10,11,12],"import":[11,12],"int":[7,12],"new":[10,11,12],"public":[3,4,5,6,7,8,9,10,11,12],"return":[3,7,8,10,11,12],"static":7,"true":[3,4,7,9,12],"try":12,And:[11,12],The:[0,1,9,10,11,12],Used:12,Will:7,__main__:4,_execut:11,_export_common:11,abort:7,accord:11,action:[1,11],add:[4,7],add_task:10,addcolor:7,added:[7,11],alert:8,all:[7,10,12],allow:10,alreadi:10,also:[8,10],ani:[10,11,12],anyth:10,api:[2,3,10],app:[1,2,3],appropri:[10,11,12],arg:[4,6,7],arguent:12,argument:[3,7,8,10,12],asci:7,ask:8,associ:10,assum:[7,10],attempt:[3,12],attribut:11,authent:9,back:[9,12],backend:10,backward:0,balloons_cursor:7,bar:7,base:[1,3,4,7,8,9,12],baseexecutor:11,basic:[0,11],behaviour:0,being:[7,10],below:[4,12],beyond:10,blob:7,bool:[3,12],call:[7,11,12],can:[1,3,4,5,6,7,8,9,10,11,12],cancel:11,captur:[11,12],carriage_return:7,cascad:10,chang:0,changelog:1,changing_arrow:7,charact:7,check:[7,10,11,12],child:10,cleanup:[11,12],clear:[2,3,8,10],client:[1,2,3,9,10,11,12],clint:3,close:[11,12],cmd:[11,12],code:[3,4,5,6,7,8,9,10,11,12],coincid:0,col_width:7,color:7,column:7,com:[7,11,12],command:[0,1,2,3,8,10,11],common:10,complet:[7,11],config:[2,3,8],config_dir:[8,9,10],configfil:9,configur:[7,8,9],confirm:[8,12],connect:10,content:[1,2],control:10,convert2boolean:7,copi:[3,4,5,6,7,8,9,10,11,12],copyright:[3,4,5,6,7,8,9,10,11,12],core:8,correct:11,could:10,count:7,creat:[7,8,10,11,12],create_databas:10,creation:10,credit:7,critic:[0,7],current:[7,11],custom:[7,10],dash:10,dashboard:[0,1,11],data:[9,10,11],data_bas:10,databas:[0,3,5,8,11],database_str:10,databsa:10,datbas:10,debug:[3,4,7],declar:10,decod:[11,12],defin:10,delai:7,delet:[5,10,11,12],delete_executor:10,delete_row:5,delete_task:10,delim:7,delimit:7,depend:[1,7,11],deprec:0,deriv:[7,12],desir:1,determin:[7,10,11],dict:12,dictionari:[7,10],directli:9,directori:[8,12],distribut:[3,4,5,6,7,8,9,10,11,12],doe:10,doesn:[10,11,12],don:[11,12],done:7,each:[0,10],effect:12,either:10,emit:7,emiterror:7,emitoutput:7,empti:[11,12],empty_char:7,enabl:7,encod:7,enhanc:0,ensur:[10,11,12],entiti:[1,10],entri:[7,8],entrypoint:6,environ:[3,7,11,12],environment:7,err:[11,12],error:[3,7,8,10,11,12],etc:[8,11],everi:7,everyth:8,execut:[4,11,12],executor:[1,3,4,8,10],executor_dir:10,executor_nam:10,executorbas:11,exist:[10,11,12],exit:[3,7,8,10,11,12],exit_info:7,expect:[11,12],expected_s:7,expos:[10,11,12],express:11,ext:10,extra:[6,10],extract:12,fail:12,failur:7,fall:12,fallback:12,fals:[3,7,8,9,10,12],field:11,file:[2,3,4,5,6,7,8,9,10,11],filenam:[10,12],filesystem:[3,8],filesystemdatabas:10,filesystemtask:10,filled_char:7,find:12,first:[0,7,10,11,12],flask:4,flat:10,folder:[10,12],form:[3,4,5,6,7,8,9,10,11,12],format:10,format_tim:7,found:[3,8,9],from:[7,8,11,12],fullpath:10,gener:[0,1,7,10,11],get:[2,3,8,9,10,11,12],get_error:[11,12],get_executor:11,get_latest_modifi:12,get_log:7,get_logging_level:7,get_named_executor:11,get_output:[11,12],get_pars:6,get_task:10,get_tmpdir:12,get_tmpfil:12,get_us:12,get_user_color_prefer:7,get_userhom:12,getenv:3,github:[7,11,12],given:[7,8,10,11,12],global:10,goe:7,green:7,gridtest:[11,12],gui:[2,3],guidanc:0,haikun:7,handl:10,has:[7,10],have:[10,11,12],header:0,here:[8,11],hide:7,histori:7,hold:10,home:[8,10,12],http:[3,4,5,6,7,8,9,10,11,12],ids:10,implement:[0,7],improv:10,includ:[0,7,10],incompat:0,index:[1,5],indic:[7,8],info:7,inform:3,init:[10,11,12],init_db:10,initdb:8,initi:[8,10,11,12],input:12,input_fil:12,inspir:[7,12],instanti:10,instead:[10,11],intend:11,interact:[1,9,10],interpret:7,interv:5,introduc:7,invok:[4,12],is_quiet:7,isenabledfor:7,item:0,iter:7,iter_executor:10,job:[1,8,11],join:7,join_newlin:7,json:[5,10,11,12],json_obj:12,just:[8,10,11,12],kei:[7,9],kennethreitz:7,kill:11,know:0,kwarg:[4,10],label:7,last:[8,10],latest:12,length:7,level:[7,12],librari:[1,8],licens:[1,3,4,5,6,7,8,9,10,11,12],like:[11,12],line:[1,11,12],list:[2,3,5,7,8,10,11,12],list_task:[8,10],liter:10,load:[9,10],log:[0,7],logger:[1,2,3],look:[11,12],main:[1,2,3,4,6,7],manual:0,master:7,match:[11,12],maximum:7,mean:[8,10,11,12],merg:0,messag:[2,3],messagelevel:7,method:12,might:[11,12],migrat:0,min_level:7,mkdir:12,mkdir_p:12,mkdtemp:12,model:[3,8],modifi:[11,12],modul:[1,2],more:[7,10,11],most:11,mozilla:[3,4,5,6,7,8,9,10,11,12],mpl:[1,3,4,5,6,7,8,9,10,11,12],much:7,must:[7,10,11],mysql:10,name:[3,7,8,10,11,12],namer:[2,3],need:11,newlin:7,none:[3,4,7,8,9,10,11,12],noprompt:8,notimpl:10,number:7,obj:12,object:[7,8,9,10,11,12],obtain:[3,4,5,6,7,8,9,10,11,12],occur:[11,12],off:[11,12],one:[3,4,5,6,7,8,9,10,11,12],onli:[1,7,9],open:12,oper:[8,12],option:[7,8,11,12],org:[3,4,5,6,7,8,9,10,11,12],origin:9,other:11,otherwis:[8,10,12],out:[7,11,12],outer:10,output:[11,12],own:10,packag:[1,2],param:12,paramet:7,parent:10,pars:[8,10,11,12],particular:[5,9,10],path:[10,11,12],pattern:12,perman:9,pickl:12,pip:0,poorli:7,popen:[11,12],port:4,possibl:10,postgresql:10,prefix:[7,10,12],pretti:12,print:[3,7,10,12],process:[11,12],programmat:4,progress:[2,3],progressbar:7,prompt:[2,3,7],properli:12,properti:[10,11,12],provid:[8,10,11,12],pull:0,pwd:12,pysq:10,python:12,qme:1,qme_hom:[8,10],quasi:9,queri:10,queue:[1,4,8],queuem:10,queuemecommand:12,queuememessag:7,queuemeserv:4,quiet:7,raw:[10,12],read:[9,10,11,12],read_fil:12,read_json:12,readlin:12,recurs:12,recursive_find:12,red:7,refresh:11,regex:[2,3],regular:[11,12],relat:[3,8],relationaldatabas:10,releas:0,reliabl:10,remov:[0,10],renam:0,repositori:0,repres:10,request:[0,5],requir:[1,3,8,10,11,12],rerun:[6,8],rerun_row:5,reset:11,respons:12,result:10,retri:11,retriev:[11,12],return_cod:7,returncod:[11,12],robot:7,robotnam:7,robust:10,row:[5,7,10],rtype:[11,12],run:[1,2,3,5,7,8,10,11],runtim:[11,12],same:12,save:[9,10,11,12],save_pickl:12,scif:12,search:12,second:7,secret:9,section:[0,9],see:4,select:7,select_gener:7,self:[9,10,11],server:[2,3],set:[7,8,11,12],set_command:[11,12],set_stderr:[11,12],set_stdout:[11,12],setup:8,share:10,shell:[3,8,12],shell_executor:5,shellexecutor:11,should:[0,7,9,10,11],should_exist:10,show:[7,8],show_progress:7,shown:11,silent:3,similar:[9,10],sinc:[10,11],skeleton:0,sochat:[3,4,5,6,7,8,9,10,11,12],some:[5,11],sourc:[3,4,5,6,7,8,9,10,11,12],specif:[8,10],specifi:[1,7,8],spin:7,spinner:[2,3],spinning_cursor:7,split:10,sqlalchemi:10,sqlite:[3,8],sqlitedatabas:10,sregistry_tmpdir:12,standard:7,start:[2,3,4,7],statu:[8,11],stderr:[7,11,12],stdout:[7,11,12],still:10,stop:7,store:[8,11],str:[3,7,8,10,11,12],stream:[7,11,12],string:[7,8,10,11,12],structur:9,subfold:10,subject:[3,4,5,6,7,8,9,10,11,12],submodul:[1,2],subpackag:[1,2],subprocess:[11,12],success:7,suffix:7,suggest:[10,11],summari:[10,11],support:[7,12],symbol:7,system:[11,12],tabl:7,take:[8,10,11],target:8,task:[5,8,10,11],taskdata:10,taskid:[5,8,10,11],tempfil:12,temporari:[11,12],term:[3,4,5,6,7,8,9,10,11,12],termin:[7,11],text:7,textui:3,thei:[11,12],them:1,thi:[0,3,4,5,6,7,8,9,10,11,12],thing:12,timestamp:[8,10],token:9,tokenchar:7,tokenlength:7,tool:1,total:7,track:0,translat:11,two:12,type:[10,12],uid:[10,12],under:[1,7,10],uniqu:10,updat:[5,9,10],update_connect:5,update_databas:5,update_disconnect:5,update_task:10,usag:[11,12],use:[1,9,11,12],usecolor:7,used:[1,4,7,8,9,10,11],user:[8,12],uses:10,using:[1,11,12],usual:7,util:[1,2,3],valu:9,vanessa:[3,4,5,6,7,8,9,10,11,12],variabl:[3,7,12],variable_kei:3,verbos:7,verbose1:7,verbose2:7,verbose3:7,version:[0,1,2,7],via:[1,4],view:[3,4],vsoch:[11,12],warn:7,web:1,what:10,when:[4,11,12],where:8,whether:10,which:7,whole:8,width:7,window:12,without:10,work:11,would:12,wrap:7,wrapper:[8,9,10],write:[7,10,11,12],write_fil:12,write_json:12,written:[11,12],x1b:7,yes:12,yet:10,yield:12,you:[1,3,4,5,6,7,8,9,10,11,12],your:7},titles:["CHANGELOG","Welcome to QueueMe Python documentation!","qme","qme package","qme.app package","qme.app.views package","qme.client package","qme.logger package","qme.main package","qme.main.config package","qme.main.database package","qme.main.executor package","qme.utils package"],titleterms:{"default":3,api:4,app:[4,5],base:[10,11],changelog:0,clear:6,client:6,clint:7,command:12,config:[4,6,9],content:[3,4,5,6,7,8,9,10,11,12],databas:10,document:1,executor:[5,11],file:12,filesystem:10,get:6,gui:8,indic:1,list:6,logger:7,main:[5,8,9,10,11],messag:7,model:10,modul:[3,4,5,6,7,8,9,10,11,12],namer:7,packag:[3,4,5,6,7,8,9,10,11,12],progress:7,prompt:12,python:1,qme:[2,3,4,5,6,7,8,9,10,11,12],queuem:1,regex:12,relat:10,run:6,server:4,shell:11,spinner:7,sqlite:10,start:6,submodul:[3,4,5,6,7,8,10,11,12],subpackag:[3,4,8],tabl:1,textui:7,util:12,version:3,view:5,welcom:1}})