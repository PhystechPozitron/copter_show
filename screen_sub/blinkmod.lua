do
local M = {}
local timer = tmr.create()
local pin = 0,light = 1

function M.blink() 
    gpio.write(pin,light)  
    light = (light == 0) and 1 or 0  
end

timer:register(500,tmr.ALARM_SINGLE,M.blink())

function M.start(interval,pin_arg)
    pin = pin_arg
    gpio.mode(pin,gpio.OUTPUT)
    timer:interval(interval)
    timer:start()      
end

function M.stop()
    timer:stop()
return M
end