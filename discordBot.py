import discord
import re
import asyncio
from discord.utils import get
from discord.ext import commands
from PIL import Image,ImageDraw
from discord import Embed
client = discord.Client()
global gameActive
gameActive = False
commands = ["$connect4"]
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
@client.event
async def on_message(message):
    global gameActive
    messagelowers = message.content
    messagelowers = messagelowers.lower()
    if messagelowers.startswith(commands[0]) and gameActive == False:
         global counterAmountY
         global counterAmountR
         global fill
         global toprowfull
         global currentTurn
         gameActive = True
         toprowfull = False
         statement = False
         noslotsleft = True
         x1 = 110
         x2 = 530
         y1 = 50
         y2 = 430
         circlestartx = 120
         circlestarty = 60
         incrementx = 47.142
         incrementy = 50
         counterAmountY = 0
         counterAmountR = 0
         fill = "red"
         img = Image.new('RGB', (640, 520), color = 'white')
         counterPlacement  = [[0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0],
                              [3, 3, 3, 3, 3, 3, 3],
                                                  ]
         draw = ImageDraw.Draw(img) 
         draw.line((x1,y1,x2,y1,x2,y2,x1,y2,x1,y1), fill="black",width=5)
         for i in range(7):
              for f in range(6):
                    draw.ellipse((circlestartx, circlestarty, circlestartx+incrementx, circlestarty + incrementy), outline ='black')
                    circlestarty = circlestarty + incrementy + 11
              circlestartx = circlestartx + incrementx + 11
              circlestarty = 60        
         img.save('GameBoard.png')
         id = '<@!%s>' % message.author.id
         id2 = message.content
         id2 = id2[10:]
         print(id2)
         currentTurn = id
         await message.channel.send("Starting a game of connect 4 with %s as YELLOW and %s as RED, Yellow goes first" % (id,id2))
         while statement != True:
            msg = await message.channel.send(file=discord.File('GameBoard.png'))
            await msg.add_reaction("1️⃣")
            await msg.add_reaction("2️⃣")
            await msg.add_reaction("3️⃣")
            await msg.add_reaction("4️⃣")
            await msg.add_reaction("5️⃣")
            await msg.add_reaction("6️⃣")
            await msg.add_reaction("7️⃣")
            def check(reaction, user):
                 global currentTurn
                 if ("<@!%s>" % user.id) == currentTurn and str(reaction.emoji) in ['1️⃣','2️⃣', '3️⃣','4️⃣','5️⃣','6️⃣','7️⃣']:
                     if currentTurn == id:
                          currentTurn = id2
                     else:
                          currentTurn = id   
                     return True
                 else:
                     return False
            def winCondition():
                     global counterAmountY
                     global counterAmountR
                     for i in range(6):
                          for f in range(7):
                               if counterPlacement[f][i] == 1:
                                    counterAmountY += 1
                                    if counterAmountY == 4:
                                         return "Yellow"
                               else:
                                    counterAmountY = 0
                               if counterPlacement[f][i] == 2:
                                    counterAmountR += 1
                                    if counterAmountR == 4:
                                         return "Red"
                               else:
                                    counterAmountR = 0      
                     for i in range(7):
                          for f in range(6):
                               if counterPlacement[i][f] == 1:
                                    counterAmountY += 1
                                    if counterAmountY == 4:
                                         return "Yellow"
                               else:
                                    counterAmountY = 0
                               if counterPlacement[i][f] == 2:
                                    counterAmountR += 1
                                    if counterAmountR == 4:
                                         return "Red"
                               else:
                                    counterAmountR = 0 
                     for i in range(4):
                          for f in range(3,6):
                               if  counterPlacement[i][f] == 1 and counterPlacement[i+1][f-1] == 1 and counterPlacement[i+2][f-2] == 1 and counterPlacement[i+3][f-3] == 1:
                                    return "Yellow"
                     for i in range(4):
                          for f in range(6-3):
                               if  counterPlacement[i][f] == 1 and counterPlacement[i+1][f+1] == 1 and counterPlacement[i+2][f+2] == 1 and counterPlacement[i+3][f+3] == 1:
                                    return "Yellow"
                     for i in range(4):
                          for f in range(3,6):
                               if  counterPlacement[i][f] == 2 and counterPlacement[i+1][f-1] == 2 and counterPlacement[i+2][f-2] == 2 and counterPlacement[i+3][f-3] == 2:
                                    return "Red"
                     for i in range(4):
                          for f in range(6-3):
                               if  counterPlacement[i][f] == 2 and counterPlacement[i+1][f+1] == 2 and counterPlacement[i+2][f+2] == 2 and counterPlacement[i+3][f+3] == 2:
                                    return "Red"                                     
            def inputnumber(numerical):
                 global fill
                 global toprowfull
                 circlestartx = 120
                 circlestarty = 60
                 for i in range(numerical - 1):
                     circlestartx = circlestartx + incrementx + 11
                 for i in range(6): 
                     if counterPlacement[0][numerical-1] == 1 or counterPlacement[0][numerical-1] == 2 or counterPlacement[0][numerical-1] == 3:
                          toprowfull = True
                          break
                     if counterPlacement[i+1][numerical-1] != 1 and counterPlacement[i+1][numerical-1] != 2 and counterPlacement[i+1][numerical-1] != 3 :
                         circlestarty = circlestarty + incrementy + 11
                     else:
                         if fill == "red":
                              fill="yellow"
                              counterPlacement[i][numerical-1] = 1  
                         else:
                              fill="red"
                              counterPlacement[i][numerical-1] = 2  
                         break
                 if(toprowfull == False):
                     draw.ellipse((circlestartx, circlestarty, circlestartx+incrementx, circlestarty + incrementy), fill =fill)
                     toprowfull = False
                 else:
                     toprowfull = False
                 img.save('GameBoard.png')     
            try:
                reaction,user = await client.wait_for('reaction_add',timeout=30,check=check)
            except asyncio.TimeoutError:
                await message.channel.send("oops the opposing team didn't respond in 30 seconds and they lost")
                gameActive = False
                return
            if winCondition() == "Red":
                     await msg.edit(content="Red is the winner")
                     gameActive = False
                     return
            if winCondition() == "Yellow":
                     await msg.edit(content="Yellow is the winner") 
                     gameActive = False
                     return         
            if reaction.emoji == '1️⃣':
                 inputnumber(1)
            if reaction.emoji == '2️⃣':
                 inputnumber(2)
            if reaction.emoji == '3️⃣':
                 inputnumber(3)
            if reaction.emoji == '4️⃣':
                 inputnumber(4)
            if reaction.emoji == '5️⃣':
                 inputnumber(5)
            if reaction.emoji == '6️⃣':
                 inputnumber(6)
            if reaction.emoji == '7️⃣':
                 inputnumber(7) 
            for i in range(7):
                for f in range(6):
                     if counterPlacement[i][f] == 0:
                          noslotsleft = False
                          break
                if noslotsleft == False:
                     break                     
            if(noslotsleft == True):
                await msg.edit(content="There are no slots left the game has ended in a tie!") 
                gameActive = False
                return
            await msg.delete()         
client.run('')