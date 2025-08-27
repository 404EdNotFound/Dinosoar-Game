import pygame, random #imported modules
pygame.init() #Initialises the game

LENGTH, WIDTH, FPS = 500, 500, 60 #Creates the screen and the FPS
FONTS = ["Agency FB", "Algerian", "Arial", "Arial Black", "Arial Narrow", "Arial Narrow Special", "Arial Rounded MT", "Arial Special", "Arial Unicode MS", "Bahnschrift", "Baskerville Old Face", "Bauhaus 93", "Beesknees ITC", "Bell MT", "Berlin Sans FB", "Berlin Sans FB Demi", "Bernard MT Condensed", "Blackadder ITC", "Book Antiqua", "Bradley Hand ITC", "Brush Script MT", "Calibri", "Calisto MT", "Cambria", "Candara", "Century Gothic", "Comic Sans MS", "Consolas", "Constantia", "Cooper Black", "Copperplate Gothic Bold", "Copperplate Gothic Light", "Corbel", "Courier New", "Courier Regular", "Curlz MT", "Edwardian Script ITC", "Elephant", "Engravers MT", "Eras ITC", "EucrosiaUPC", "Euphemia", "Eurostile", "Felix Titling", "Fine Hand", "Fixed Miriam Transparent", "Forte", "Franklin Gothic", "Franklin Gothic Medium", "Freestyle Script", "Gabriola", "Garamond", "Georgia", "Gill Sans", "Gill Sans MT", "Gill Sans MT Condensed", "Goudy Old Style", "Goudy Stout", "Gradl Grotesque", "Hadassah Friedlaender", "Haettenschweiler", "Harlow Solid Italic", "Harrington", "High Tower Text", "Holidays MT", "Impact", "Imprint MT Shadow", "Informal Roman", "IrisUPC", "Iskoola Pota", "JasmineUPC", "Javanese Text", "Jokerman", "Juice ITC", "KaiTi", "Kalinga", "Kartika", "Khmer UI", "Kino MT", "Kristen ITC", "Lao UI", "Latha", "Leelawadee", "Levenim MT", "Lucida Blackletter", "Lucida Bright", "Lucida Bright Math", "Lucida Calligraphy", "Lucida Console", "Lucida Fax", "Lucida Handwriting", "Lucida Sans", "Lucida Sans Typewriter", "Lucida Sans Unicode", "Magneto", "Maiandra GD", "Malgun Gothic", "Mangal", "Matura MT Script Capitals", "McZee", "Mead Bold", "Meiryo", "Mercurius Script MT Bold",  "Microsoft Sans Serif", "Mistral", "Modern Love", "Modern No. 20", "Mongolian Baiti", "Monotype.com", "Monotype Corsiva", "Monotype Sorts", "MoolBoran", "MS Gothic", "MS PMincho", "MS Reference", "News Gothic MT", "New Caledonia", "OCR A Extended", "Old English Text MT", "Onyx", "Palatino Linotype", "Papyrus", "Parchment", "Perpetua", "Perpetua Titling MT", "Playbill", "PMingLiU", "PMingLiU-ExtB", "Poor Richard", "Pristina", "Rage Italic", "Ravie", "Rockwell", "Rockwell Extra Bold", "Rod", "Sakkal Majalla", "Script MT Bold", "Segoe Print", "Segoe Script", "Segoe UI", "Segoe UI Emoji", "Segoe UI Historic", "Segoe UI Symbol", "Segoe UI Variable", "Shonar Bangla", "Showcard Gothic", "Shruti", "SimHei", "Simplified Arabic", "SimSun", "SimSun-ExtB", "Sitka", "Snap ITC", "Stencil", "Sylfaen", "Tahoma", "Tempus Sans ITC", "Times New Roman", "Trebuchet MS", "Verdana", "Viner Hand ITC", "Vivaldi", "Vladimir Script", "Wide Latin", "Yu Gothic", "Yu Gothic UI"]

#Defined the variables such as the choice of fonts, window, caption, text, clock and score
fontChoice = random.choice(FONTS)
window = pygame.display.set_mode((LENGTH, WIDTH))
caption = pygame.display.set_caption("Dinosoar game with blocks")
text = pygame.font.SysFont(fontChoice, 20, "Bold")
clock = pygame.time.Clock()
score = 0

#Loaded the files, changed it here since the original file uses a directory path
jumpSound = pygame.mixer.Sound("jump.wav")
hundredScore = pygame.mixer.Sound("point.wav")
death = pygame.mixer.Sound("die.wav")
music = pygame.mixer.music.load("Gaming Music.mp3")
pygame.mixer.music.play(-1) #repetitive loop

#Created class for the moving block
class Block(object):
    def __init__(self, x, y, length, width):
        self.x, self.y, self.length, self.width = x, y, length, width
        self.velocity, self.jumpCount = 5, 10
        self.isJump = False

    #Function for jumping
    def jumping(self):
        if self.jumpCount >= -10:
            negative = 1
            if self.jumpCount < 0:
                negative = -1
            
            self.y -= float((self.jumpCount ** 2) * 0.5 * negative)
            self.jumpCount -= 1
        
        else:
            self.jumpCount = 10
            self.isJump = False

#Class Created for oncoming obstacles (done through side scrolling)
class obstacles(object):
    def __init__(self):
        self.blocks = [pygame.Rect(x, 380, 40, 20) for x in range(500, LENGTH * 10, 500)]
        self.scrollPos = random.randint(5, 10)

    #Method used for side scrolling (moving the background with obstacles)
    def updateBlocks(self):
        for block in self.blocks:
            block.x -= self.scrollPos
        
        if self.blocks[0].x <= -100:
            value = random.randint(200, 1000)
            self.blocks.pop(0)
            self.blocks.append(pygame.Rect(self.blocks[-1].x + value, 380, 40, 20))
        self.scrollPos = random.randint(5, 10) #Randomising the velocity of the blocks coming in
            
    def draw(self):
        for block in self.blocks:
            pygame.draw.rect(window, (0, 255, 0), block)
            
def draw():
    global score
    score += 1
    
    info = f"Score: {score:05d}" #Updates the score
    
    if (score % 100) == 0:
        hundredScore.play()
    
    scoreText = text.render(info, 1, (255, 255, 255))
    
    window.fill((0, 0, 0))
    pygame.draw.rect(window, (255, 255, 255), (0, (500 - 100), LENGTH, 5))
    pygame.draw.rect(window, (255, 255, 255), (0, 95, LENGTH, 5))
    pygame.draw.rect(window, (255, 0, 0), (block.x, block.y, block.length, block.width))
    window.blit(scoreText, (LENGTH - len(info) * 15, 45))

run = True
game_over = False
deathPlayed = False
block = Block(20, (500 - 125), 25, 25)
obstacle = obstacles()

#Game Loop
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    keys = pygame.key.get_pressed()
    
    if not(game_over): #Needed help with this
        if not(block.isJump):
            
            if keys[pygame.K_SPACE] and not block.isJump:
                jumpSound.play()
                block.isJump = True
        
        else:
            block.jumping()
            
        obstacle.updateBlocks()
        draw()
        obstacle.draw()
    
    else:
        gameOverText = text.render("GAME OVER!!!", 1, (255,255,255))
        window.blit(gameOverText, (20, 45))
        
        if not deathPlayed:
            music = pygame.mixer.music.load("Game Over.mp3")
            pygame.mixer.music.play(-1)
            death.play()
            deathPlayed = True
        
    for object in obstacle.blocks:
        if object.colliderect(pygame.Rect(block.x, block.y, block.length, block.width)):
            game_over = True
    
    pygame.display.update()

pygame.quit()
