local selectedport = "8765" --must match server port, keep as is
local local_ip = "192.168.12.34" --server ipv4 (you can find this in task manager,more details, performance, Wi-Fi, ipv4 address or use the .bat)
--REPLACE THE IP WITH YOUR SERVER IPV4 IP, USE THE GETLOCALIP.BAT TO GET IT, DONT INCLUDE SPACE.
--example: local local_ip = "12.34.56.78"
--example: local local_ip = "123.456.78.90"

local localPlayer = "replace_me" -- replace this with the roblxo account username (no display name) you want to use it on aka, your main acc or whatever (cap sensitive btw)

local ws = WebSocket.connect("ws://" .. local_ip .. ":" .. selectedport)

ws.OnMessage:Connect(function(message)
    print("received")
end)

ws.OnClose:Connect(function()
    print("Disconnected")
end)



localPlayer = game.Players[localPlayer]
while task.wait(0.01) do
    local players = {}
    pcall(function()

    local localCharacter = localPlayer.Character
    local localPosition = localCharacter and localCharacter.Head and localCharacter.Head.Position
    local localCFrame = localCharacter and localCharacter.PrimaryPart and localCharacter.PrimaryPart.CFrame

    -- Apply a -90 degree rotation around the Y-axis, default 0 is nto good
    
    
    
    local offsetCFrame = localCFrame * CFrame.Angles(0, math.rad(-90), 0)
    local localLookVector = offsetCFrame.LookVector

    for _, v in pairs(game.Players:GetChildren()) do
        pcall(function()
            if v.Character and v.Character.Head then
                local head = v.Character.Head
                local position = head.Position


                if localPosition and localLookVector then
                    local relX = position.X - localPosition.X
                    local relY = position.Y - localPosition.Y
                    local relZ = position.Z - localPosition.Z


                    local relVector = Vector3.new(relX, relY, relZ)
                    local adjustedRelX = relVector:Dot(Vector3.new(localLookVector.X, 0, localLookVector.Z))
                    local adjustedRelZ = relVector:Dot(Vector3.new(-localLookVector.Z, 0, localLookVector.X))

                    table.insert(players, {
                        name = v.Name,
                        pos = {x = adjustedRelX, y = relY, z = adjustedRelZ}, 
                        lookY = head.Rotation.Y
                    })
                end
            end
        end)
    end

    -- now we put all data together, neatly for the server.py! 
    local output = "["

    for i, player in ipairs(players) do
        print(player.lookY)
        output = output .. string.format('{"name": "%s", "pos": {"x": %f, "y": %f, "z": %f}, "lookY": %f}', 
            player.name, 
            player.pos.x, player.pos.y, player.pos.z, 
            player.lookY)

        if i < #players then
            output = output .. ","  
        end
    end

    output = output .. "]"


    ws:Send(output)
    end)
end
