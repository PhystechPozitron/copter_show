do
function color(i)
    if i % 70 <= 35 then 
        return i % 70
    else
        return 70 - (i % 70)
    end    
end

ws2812.init()
local length = 45
local i = -length + 1
local buffer = ws2812.newBuffer(256,3)

tmr.create():alarm(10,tmr.ALARM_AUTO,function ()
    if i >= 1 then
        buffer:set(i,0,0,0)
    end
    if i + length <= buffer:size() then
        buffer:set(i + length,color(i),50 - color(i),50 - color(i))
    end
    ws2812.write(buffer)
    i = (i < buffer:size()) and i + 1 or -length + 1     
end)
end
