do
--variables
local m_sizeX = 16
local m_sizeY = 16
local intensity = 20

--functions
local function setFrame(frame)
    -- fill buffer
    local buffer = ws2812.newBuffer(m_sizeX*m_sizeY,3)
    buffer:fill(0,0,0)
    buffer:replace(frame,1)
    -- set intensity
    buffer:mix(intensity, buffer)
    -- write to matrix
    ws2812.write(buffer)
    buffer = nil
end

local function playShow(fname)
    if file.open(fname,"r") then
        -- read N,fps,sizeX,sizeY
        local N = string.byte(file.read(2):reverse())
        local fps = string.byte(file.read(2):reverse())
        local sizeX = string.byte(file.read(2):reverse()) 
        local sizeY = string.byte(file.read(2):reverse())
        if (sizeX == m_sizeX)and(sizeY == m_sizeY) then
            -- calculate time from timer and start timer
            local time,cnt = 1000/fps,1
            tmr.create():alarm(time,tmr.ALARM_AUTO,function()
                setFrame(file.read(3*sizeX*sizeY))
                if cnt == N then file.seek("set",8) end
                cnt = (cnt == N) and 1 or cnt + 1
            end)              
        else
            file.close()
            print("Wrong size of frame")
            return -1    
        end       
    else
        print("Unable to open file "..fname)
        return -1 
    end
end

--initialization
ws2812.init()
playShow("esp.show")      
end
