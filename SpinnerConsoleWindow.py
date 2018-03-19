import pygame
import datetime
import random
import mysql.connector


class SpinnerConsoleWindow:
    display_width = 1600  # Preferably 1920
    display_height = 900  # Preferably 1080

    def get_current_time(self):
        return time.time()

    def generateRandomAngle(self):  # Random angle to stop the wheel at
        return (random.randint(0, 360) * 20) % 360

    def getLabelClick(self, labelRect, mosx, mosy):  # To return the clicked label
        if labelRect.left < mosx < labelRect.right and labelRect.top < mosy < labelRect.bottom:
            return 1

    def displayText(self, text, font, screenSurface, center=True, posX=display_width / 2, posY=display_height / 2, color=(0, 0, 0)):  # To display label text
        label = font.render(text, True, color)
        labelRect = label.get_rect()
        if center:
            labelRect.center = ((posX, posY))
            screenSurface.blit(label, labelRect)
        else:
            screenSurface.blit(label, (posX, posY))
        return labelRect

    def __init__(self):
        pygame.init()

        cnx = mysql.connector.connect(user='root', password='password', host='127.0.0.1', database='dis_booth')
        cursor = cnx.cursor()

        self.bgImagePath = "rsc/graphics/spinner/bg_background.jpg"
        self.bg1ImagePath = "rsc/graphics/spinner/bg_background1.jpg"
        self.btnBorderPath = "rsc/graphics/nav/btnBorder.png"
        self.spinnerWheelPath = "rsc/graphics/spinner/wheel.png"
        self.pinWheelPath = "rsc/graphics/spinner/pin.png"
        self.mediumFont = pygame.font.Font("Font/Trash Zydego.ttf", 40)
        self.font1 = pygame.font.SysFont("monospace", 75)  # default
        pygame.font.Font.set_bold(self.font1, True)
        self.clock = pygame.time.Clock()
        self.angle = 0  # Init the angle as to how the spinning wheel will turn
        self.buttonClicked = False
        self.randomAngleToStop = self.generateRandomAngle()
        while self.randomAngleToStop == 360:
            self.randomAngleToStop = self.generateRandomAngle()
        self.running = 0
        self.wheelSpinCount = 0
        self.ledTravelAdapterArray = [20, 40]
        self.microfiberClothArray = [100, 120, 240, 260]
        self.rfidCaseArray = [180, 200, 320, 340]
        self.candyArray = [0, 60, 80, 220]
        self.mysteryArray = [140, 160, 280, 300]

        self.isBg1 = False

        self.screen = pygame.display.set_mode((self.display_width, self.display_height), pygame.FULLSCREEN)  # Can be set to FULLSCREEN

        # Code for Music
        pygame.mixer.music.load("rsc/audio/bgTrack.ogg")
        pygame.mixer.music.play(-1)  # Set -1 to loop background audio indefinitely

        self.bgImage = pygame.image.load(self.bgImagePath)
        self.bgImage = pygame.transform.scale(self.bgImage, (self.display_width, self.display_height))

        self.bgImage1 = pygame.image.load(self.bg1ImagePath)
        self.bgImage1 = pygame.transform.scale(self.bgImage1, (self.display_width, self.display_height))

        self.btnBorderImage = pygame.image.load(self.btnBorderPath)
        self.btnBorderImageRect = self.btnBorderImage.get_rect()
        self.btnBorderImageRect.centerx = self.display_width / 2
        self.btnBorderImageRect.y = 185

        self.pinWheelImageOrig = pygame.image.load(self.pinWheelPath)
        self.pinWheelImageOrig = pygame.transform.scale(self.pinWheelImageOrig, (50, 50))
        self.pinWheelImageOrigRect = self.pinWheelImageOrig.get_rect()
        self.pinWheelImageOrigRect.centerx = self.display_width / 2
        self.pinWheelImageOrigRect.y = 285

        self.spinnerWheelImageOrig = pygame.image.load(self.spinnerWheelPath)
        self.spinnerWheelImageOrig = pygame.transform.scale(self.spinnerWheelImageOrig, (620, 620))
        self.spinnerWheelImageRect = self.spinnerWheelImageOrig.get_rect()
        self.spinnerWheelImageRect.centerx = self.display_width / 2
        self.spinnerWheelImageRect.y = 290

        # To retrieve the amount of prizes for each category from the database
        sqlQueryTravelAdapter = ("SELECT current_inventory FROM booth_prize_inventory WHERE prize='travel_adapter'")
        cursor.execute(sqlQueryTravelAdapter)
        for current_inventory in cursor:
            self.travelAdaptersLeft = current_inventory[0]

        sqlQueryRfidCase = ("SELECT current_inventory FROM booth_prize_inventory WHERE prize='rfid_case'")
        cursor.execute(sqlQueryRfidCase)
        for current_inventory in cursor:
            self.rfidCasesLeft = current_inventory[0]

        sqlQueryMicrofiberCloth = ("SELECT current_inventory FROM booth_prize_inventory WHERE prize='microfiber_cloth'")
        cursor.execute(sqlQueryMicrofiberCloth)
        for current_inventory in cursor:
            self.microfiberClothsLeft = current_inventory[0]

        sqlQueryCandy = ("SELECT current_inventory FROM booth_prize_inventory WHERE prize='candy'")
        cursor.execute(sqlQueryCandy)
        for current_inventory in cursor:
            self.candyLeft = current_inventory[0]

        sqlQueryMysteryPrize = ("SELECT current_inventory FROM booth_prize_inventory WHERE prize='mystery'")
        cursor.execute(sqlQueryMysteryPrize)
        for current_inventory in cursor:
            self.mysteryPrizesLeft = current_inventory[0]

        print "===================================Prizes Status==================================="
        print "===  Travel Adapter |  RFID Case  |  Microfiber Cloth  |  Candy  |    Mystery   ==="
        print "===       " + str(self.travelAdaptersLeft) + "       |     " + str(self.rfidCasesLeft) + \
              "     |        " + str(self.microfiberClothsLeft) + "         |   " + str(self.candyLeft) + "   |     " + str(self.mysteryPrizesLeft) + "      ==="
        print "==================================================================================="

        self.topTierPrizeLimit = 2  # Value to limit the amount of top tier prizes available per hour

        while not self.running:
            self.screen.blit(self.bgImage, (0, 0))

            if datetime.datetime.now().minute == 00:  # Check if the minute is 00, to reset the prize limit/h
                self.topTierPrizeLimit = 2  # Need to change this value if value on line 109 is changed

            #if datetime.datetime.now().second % 2 == 0:
            #    if self.isBg1:
            #        self.screen.blit(self.bgImage, (0, 0))
            #        self.isBg1 = False
            #    else:
            #        self.screen.blit(self.bgImage1, (0, 0))
            #        self.isBg1 = True

            self.keys_pressed = pygame.mouse.get_pressed()

            # self.screen.blit(self.bgImage, (0, 0))

            self.mos_x, self.mos_y = pygame.mouse.get_pos()

            self.bgImage_top = self.screen.get_height() - self.bgImage.get_height()
            self.bgImage_left = self.screen.get_width() / 2 - self.bgImage.get_width() / 2

            self.screen.blit(self.btnBorderImage, self.btnBorderImageRect)

            self.itrmsLabelRect = self.displayText("ITRMS", self.font1, self.screen, posY=85,  color=(0, 149, 145))
            self.playlabelRect = self.displayText("Play!", self.mediumFont, self.screen, posY=224,  color=(255, 255, 255))

            if self.getLabelClick(self.playlabelRect, self.mos_x, self.mos_y):
                self.displayText("Play!", self.mediumFont, self.screen, posY=224, color=(255, 0, 0))

            self.spineerWheelImage = pygame.transform.rotate(self.spinnerWheelImageOrig, self.angle)
            self.spinnerWheelImageRect = self.spineerWheelImage.get_rect(center=self.spinnerWheelImageRect.center)

            self.screen.blit(self.spineerWheelImage, self.spinnerWheelImageRect)
            self.screen.blit(self.pinWheelImageOrig, self.pinWheelImageOrigRect)

            self.events = pygame.event.get()

            for event in self.events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click = 1
                        if self.getLabelClick(self.playlabelRect, self.mos_x, self.mos_y):
                            self.buttonClicked = True

            if self.buttonClicked:
                self.angle += 20
                if self.angle >= 360:
                    self.wheelSpinCount += 1
                    self.angle %= 360

                if self.randomAngleToStop == self.angle:
                    if self.wheelSpinCount == 5:
                        if self.randomAngleToStop in self.candyArray:
                            self.candyLeft -= 1
                            cursor.execute("""
                               UPDATE booth_prize_inventory
                               SET current_inventory = %s
                               WHERE prize=%s
                            """, (str(self.candyLeft), "candy"))
                            print "\n" + str(datetime.datetime.now()) + " : Candy awarded for this round!"

                        elif self.randomAngleToStop in self.rfidCaseArray:
                            self.rfidCasesLeft -= 1
                            cursor.execute("""
                               UPDATE booth_prize_inventory
                               SET current_inventory = %s
                               WHERE prize=%s
                                """, (str(self.rfidCasesLeft), "rfid_case"))
                            print "\n" + str(datetime.datetime.now()) + " : RFID Case awarded for this round!"

                        elif self.randomAngleToStop in self.microfiberClothArray:
                            self.microfiberClothsLeft -= 1
                            cursor.execute("""
                               UPDATE booth_prize_inventory
                               SET current_inventory = %s
                               WHERE prize=%s
                                """, (str(self.microfiberClothsLeft), "microfiber_cloth"))
                            print "\n" + str(datetime.datetime.now()) + " : Microfiber Cloth awarded for this round!"

                        elif self.randomAngleToStop in self.mysteryArray:
                            self.mysteryPrizesLeft -= 1
                            cursor.execute("""
                               UPDATE booth_prize_inventory
                               SET current_inventory = %s
                               WHERE prize=%s
                                """, (str(self.mysteryPrizesLeft), "mystery"))
                            print "\n" + str(datetime.datetime.now()) + " : Mystery Prize Awarded for this round!"

                        elif self.randomAngleToStop in self.ledTravelAdapterArray:
                            self.topTierPrizeLimit -= 1
                            self.travelAdaptersLeft -= 1
                            cursor.execute("""
                               UPDATE booth_prize_inventory
                               SET current_inventory = %s
                               WHERE prize_tier=%s
                                """, (str(self.travelAdaptersLeft), "travel_adapter"))
                            print "\n" + str(datetime.datetime.now()) + " : Travel Adapter awarded for this round!"

                        cnx.commit()

                        print "===================================Prizes Status==================================="
                        print "===  Travel Adapter |  RFID Case  |  Microfiber Cloth  |  Candy  |    Mystery   ==="
                        print "===       " + str(self.travelAdaptersLeft) + "       |     " + str(self.rfidCasesLeft) + \
                              "     |        " + str(self.microfiberClothsLeft) + "         |   " + str(
                            self.candyLeft) + "   |     " + str(self.mysteryPrizesLeft) + "      ==="
                        print "==================================================================================="

                        self.angle -= 20  # Make the spinning wheel stop

                        while True:  # Infinite loop to check if number "randomised" fits certain conditions, if not randomise again
                            self.randomAngleToStop = self.generateRandomAngle()
                            if self.randomAngleToStop == 360 or (self.topTierPrizeLimit == 0 and self.randomAngleToStop in self.ledTravelAdapterArray):
                                pass
                            elif self.randomAngleToStop in self.ledTravelAdapterArray and self.travelAdaptersLeft == 0:
                                pass
                            elif self.randomAngleToStop in self.rfidCaseArray and self.rfidCasesLeft == 0:
                                pass
                            elif self.randomAngleToStop in self.microfiberClothArray and self.microfiberClothsLeft == 0:
                                pass
                            elif self.randomAngleToStop in self.candyArray and self.candyLeft == 0:
                                pass
                            elif self.randomAngleToStop in self.mysteryArray and self.mysteryPrizesLeft == 0:
                                pass
                            else:
                                break

                        # print "======\n" + str(self.randomAngleToStop) + " will be spinned for the next round"
                        self.buttonClicked = False
                        self.wheelSpinCount = 0

            pygame.display.flip()
