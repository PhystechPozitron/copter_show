do
ws2812.init()
local buffer = ws2812.newBuffer(256,3)
buffer:fill(0,0,0)
ws2812.write(buffer)
file.remove("action_check.bmp")
end
