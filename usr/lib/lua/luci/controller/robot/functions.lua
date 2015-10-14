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

function action_move()
            os.execute("echo '"..luci.http.formvalue("com").."' > /tmp/command & sync")
	    
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
        local data_file = io.open('/tmp/data','r')
        if data_file~=nil then
            raw_data = data_file:read()
            data = raw_data
            --data = split(raw_data, ",")
        end
        luci.http.prepare_content("application/json")

        luci.http.write_json(data)
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
	os.execute('wget "http://localhost:8080/?action=snapshot" -O /tmp/mounts/Disc-A1/pic_$(date +%S-%M-%H_%d-%m-%y).jpg')
end	