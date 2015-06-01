module("luci.controller.robot.functions", package.seeall)

function index()
      entry({"admin", "robot"}, firstchild(), "robot", 20).index=true
      
      dash = entry({"admin", "robot", "index"},template("robot/index"), _("Dashboard"), 1)
      --dash.sysauth = false
      distance = entry({"admin", "robot", "distance"},template("robot/distance"), _("Driving"), 2)
      --distance.sysauth = false
      entry({"admin", "robot", "distance","move"}, call("action_move"))
      entry({"admin", "robot", "distance","read"}, call("action_read"))
      entry({"admin", "robot", "distance","write"}, call("action_write"))
      entry({"admin", "robot", "distance","serial"}, call("serial_test"))
      entry({"admin", "robot", "distance","wifi"}, call("wifi_status"))
      entry({"admin", "robot", "distance","heartbeat"}, call("heartbeat"))
      entry({"admin", "robot", "distance","picture"}, call("take_picture"))        

      mycontrols = entry({"admin", "robot", "mycontrols"},template("robot/mycontrols"), _("Mycontrols"), 3)
      --mycontrols.sysauth = false
      editcontrols = entry({"admin", "robot", "edit-controls"},template("robot/edit-controls"), _("Edit Controls"), 4)
      --editcontrols.sysauth = false
      help = entry({"admin", "robot", "help"},template("robot/help-manual"), _("Help"), 5)
      --help.sysauth = false
      settings = entry({"admin", "robot", "settings"},template("robot/settings"), _("Settings"), 6)
      --settings.sysauth = false
      test = entry({"admin", "robot", "editor"},template("robot/editor"), _("Editor"), 7)
      --test.sysauth = false
      entry({"admin", "robot", "editor","save"}, call("action_save"))
      entry({"admin", "robot", "editor","run"}, call("action_run"))
      entry({"admin", "robot", "editor","load"}, call("action_load"))

      test = entry({"admin", "robot", "test"},template("robot/test"), _("Test"), 8)
      --test.sysauth = false
      popup_form = entry({"admin", "robot", "form"},template("robot/form"), _("ADD"), 9)
      popup_form.sysauth = false
end

function start_webcam()

	 --os.execute(' mjpg_streamer -i "input_uvc.so -q 80 -f 24 -r 320x240" -o "output_http.so" ')
	 --os.execute('^C')
	 luci.template.render("robot/distance")
	 
end

function setup_camera()
        local device = "0"
	local resolution = "320x240"
	local fps = "10"
	local quality = "80"
	local port = "8080"
        local mjpg = io.open("/etc/config/mjpg-streamer","w")
        mjpg:write( "config mjpg-streamer 'core'"+"\n")
	mjpg:write( "    option enable 'true''"+"\n")
	mjpg:write( "    option input 'uvc''"+"\n")
	mjpg:write( "    option output 'http''"+"\n")
	mjpg:write( "    option device '/dev/video"+device+"''"+"\n")
	mjpg:write( "    option resolution '"+resolution+"''"+"\n")
	mjpg:write( "    option fps '"+fps+"''"+"\n")
	mjpg:write( "    option quality '"+quality+"''"+"\n")
	mjpg:write( "    option port '"+port+"''"+"\n")
	mjpg:close()
end 

function heartbeat(direction)
	--local python_serial = io.popen("python /usr/lib/lua/luci/controller/robot/serialcom.py "+direction,"r")
	luci.http.prepare_content("application/json")
        luci.http.write_json(python_serial)
end
 
function file_open(name)
   local f=io.open(name,"w")
   if f~=nil then io.close(f) return nil else return f end
end


function action_move()

	    if luci.http.formvalue("dir") == "forward" then
		io.popen("echo '#mov(80)' > /home/command")
	    elseif luci.http.formvalue("dir") == "back" then
	        io.popen("echo '#mov(-80)' > /home/command")	
	    elseif luci.http.formvalue("dir") == "left" then
	        io.popen("echo '#mov(80,-90)' > /home/command")
	    elseif luci.http.formvalue("dir") == "right" then
	        io.popen("echo '#mov(80,90)' > /home/command")
	    else 
                io.popen("echo '#mov(0)' > /home/command")
	    end
	
end

function serial_test()
	local test = "success"
        --os.execute('python /usr/lib/lua/luci/controller/robot/testSerial.py')
end

function wifi_status()
        local wifi = io.popen("iw dev wlan0 station dump","r")
        luci.http.prepare_content("application/json")
        signal = "0"
        while true do
                 ln = wifi:read("*l")
                 if not ln then break end
                 ln_write = string.sub(ln:gsub("%s+",""),1,6)
                 if ln_write=="signal" then
                     signal = ln:match("%[(.*)%]") 
                     signal = signal:sub(2,-1) 
                 end
        end
        luci.http.write_json(signal)
end 

function action_read()
        data = {"0","0","0","0","0","0"}
        local data_file = io.open('/home/data','r')
        if data_file~=nil then
            raw_data = data_file:read()
            data = raw_data
            --data = split(raw_data, ",")
        end
        luci.http.prepare_content("application/json")

        luci.http.write_json(data)
	--tcp:close()
end

function action_load()
        code = ""
	local user_code = io.open('/home/user-script.py','r')
        if user_code~=nil then
            code = user_code:read("*all")
        end
	user_code:close()
        luci.http.write_json(code)
end

function magiclines(s)
	if s:sub(-1)~="\n" then s=s.."\n" end
        return s:gmatch("(.-)\n")
end

function action_save()
        local lines = luci.http.formvalue("lines")
    
        lines = tonumber(lines)
	for i = 1, lines do
		line = luci.http.formvalue(tostring(i))
                if i == 1 then
			os.execute("echo '"..line.."' > '/home/user-script.py'")
		else
			os.execute("echo '"..line.."' >> '/home/user-script.py'")
		end
	end

end	

function action_run()
	os.execute('python /home/user-script.py')
end	

function take_picture()
	os.execute('wget -P /tmp/mounts/Disc-A1/ "http://localhost:8080/?action=snapshot"')
end	

function action_write()
        
        local commandStr = luci.http.formvalue("command")
        local commandServo = luci.http.formvalue("commandSer")
        	
        
        wserial=io.open("/dev/ttyACM0","w")
        
       if string.len(commandServo) ~= 0 then
        	local commandSer = {}
        	seri = 0
        	for serj in string.gmatch( commandServo, "(%d+),") do
        		commandSer[seri] = serj
        		seri = seri + 1
        	end
        	wserial:write(string.char(255,2,commandSer[0],commandSer[1],0,commandSer[2],commandSer[3],254))
        	wserial:flush()
        end
        
        if string.len(commandStr) ~= 0 then
        
        	if commandStr == "STOP" then
        		for motNum=1,4 do
        	
        			wserial:write(string.char(255,1,motNum,0,0,0,0,254))	
        	
        		end
        	
        		wserial:flush()	
        	
        	else
        	
        		local command = {}
        	
       		
       			inti =0
        		for i in string.gmatch( commandStr, "(%d+,%d+,%d+,%d+,%d+,)'''") do
        	
        			tempStr = i
        			intj =0
        
        			command[inti] = {}
        			for j in string.gmatch( tempStr, "(%d+),") do
        
        				command[inti][intj] = j
        				intj = intj+1
        			end
        
       		 		inti = inti+ 1
        		end
        
        		inti = inti-1
        	
        		for x=0,inti do 
        	
        			wserial:write(string.char(255,1,command[x][0],command[x][1],command[x][2],command[x][3],command[x][4],254))
			end
			wserial:flush()        
		end
	
	end
end


