import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from pandac.PandaModules import *
import urllib2
from urllib import urlencode
import cookielib
from panda3d.core import AmbientLight, DirectionalLight, LightAttrib
import json
from direct.task.Task import Task
import time

class Teest:

    def __init__(self):
    
        self.cookies = cookielib.CookieJar()
        self.cookies.clear()
        
        self.refreshparty = False
        self.refreshPartyTask = taskMgr.add(self.refreshPartyTask, 'refreshPartyTask')
        
        self.logingui()
        #self.partygui()

    def logingui(self):
        self.loginFrame = DirectFrame( color = (0, 0, 0, 0.5), frameSize = ( -.35, .35, -.25, .25 ) )
        self.loginFrame.setTransparency(True)
        self.loginFrame.setPos(0, 0, -0.33)

        self.loginEntry = DirectEntry( scale = .05, numLines = 1, focus = 1 )
        self.loginEntry.reparentTo( self.loginFrame )
        self.loginEntry.setPos(-0.25, 0, 0.1)

        self.passwordEntry = DirectEntry( scale = .05, numLines = 1, obscured = True )
        self.passwordEntry.reparentTo( self.loginFrame )
        self.passwordEntry.setPos(-0.25, 0, -0.025)

        connectButton = DirectButton( scale = .05, text  = ("Connect", "Connect", "Connect", "disabled"), command = self.login )
        connectButton.reparentTo( self.loginFrame )
        connectButton.setPos(0, 0, -0.15)

    def login(self):
        login = self.loginEntry.get()
        password = self.passwordEntry.get()
        values = { 'login': login, 'pass': password }
        try:
            opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=1), urllib2.HTTPCookieProcessor(self.cookies))
            urllib2.install_opener(opener)
            rsp = opener.open('http://localhost:3000/login', urlencode(values))
        except IOError:
            print 'fail'
        else:
            print rsp.read()
            rsp.close()
            self.loginFrame.destroy()
            self.partiesgui()

    def partiesgui(self):
        self.partiesFrame = DirectFrame( color = (0, 0, 0, 0.5), frameSize = ( -1.2, 1.2, -0.7, 0.7 ) )
        self.partiesFrame.setTransparency(True)
        self.partiesFrame.setPos(0, 0, 0.15)
        
        self.createPartyFrame = DirectFrame( color = (0, 0, 0, 0.5), frameSize = ( -1.2, 1.2, 0.1, -0.1 ) )
        self.createPartyFrame.setTransparency(True)
        self.createPartyFrame.setPos(0, 0, -0.75)
        
        partyNameLabel = DirectLabel( scale = .05, text  = ("Name", "Name", "Name", "disabled") )
        partyNameLabel.reparentTo( self.createPartyFrame  )
        partyNameLabel.setPos(-1.0, 0, 0)
        
        self.partyNameEntry = DirectEntry( scale = .05, numLines = 1, focus = 1 )
        self.partyNameEntry.reparentTo( self.createPartyFrame  )
        self.partyNameEntry.setPos(-0.8, 0, 0)
        
        mapLabel = DirectLabel( scale = .05, text  = ("Map", "Map", "Map", "disabled") )
        mapLabel.reparentTo( self.createPartyFrame  )
        mapLabel.setPos(-0.1, 0, 0)
        
        self.mapMenu = DirectOptionMenu( text = "options", scale = 0.05, 
                                         items = [ "Test City" ],
                                         highlightColor = ( 0.65, 0.65, 0.65, 1 ) )
        self.mapMenu.reparentTo( self.createPartyFrame  )
        self.mapMenu.setPos(0, 0, 0)
        
        createPartyButton = DirectButton( scale = .05, text  = ("Create", "Create", "Create", "disabled"), command = self.createparty )
        createPartyButton.reparentTo( self.createPartyFrame )
        createPartyButton.setPos(0.5, 0, 0)

    def createparty(self):
        name = self.partyNameEntry.get()
        mapname = self.mapMenu.get()
        values = { 'name': name, 'mapname': mapname }
        try:
            opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=1), urllib2.HTTPCookieProcessor(self.cookies))
            urllib2.install_opener(opener)
            rsp = opener.open('http://localhost:3000/ownparty', urlencode(values))
        except IOError:
            print 'fail'
        else:
            party = json.loads(rsp.read())
            print party
            rsp.close()
            self.partiesFrame.destroy()
            self.createPartyFrame.destroy()
            self.partygui(party)

    def partygui(self, party):

        #base.setBackgroundColor( 0.5,0.5,1 )
        
        terrain = loader.loadModel( 'models/maps/Test City.egg' )
        terrain.reparentTo( render )
        terrain.setScale( 0.5 )
        terrain.setPos( 0,0,0 )
        
        base.disableMouse()
        base.camera.lookAt(0, 0, 0)
        lens = OrthographicLens()
        lens.setFilmSize(30, 20)
        base.cam.node().setLens(lens)
        camera.setPosHpr(-20, -20, 24, -45, -35, 0)
        
        ambientLight = AmbientLight( "ambientLight" )
        ambientLight.setColor( Vec4(1, 1, 1, 1) )
        render.setLight( render.attachNewNode( ambientLight ) )
        
        self.partyFrame = DirectFrame( color = (0, 0, 0, 0.5), frameSize = ( -1, 1, -0.9, 0.9 ) )
        self.partyFrame.setTransparency(True)
        self.partyFrame.setPos(0, 0, 0)
        
        partyName = OnscreenText(text = 'Party: '+party['name'],         pos = (0, 0.8), scale = 0.07, parent = self.partyFrame)
        createdBy = OnscreenText(text = 'Created by: '+party['creator'], pos = (0, 0.7), scale = 0.05, parent = self.partyFrame)
        waitingFor = OnscreenText(text = 'Waiting for second character', pos = (0, 0.0), scale = 0.05, parent = self.partyFrame)
        
        self.refreshparty = True

    def refreshPartyTask(self, task):
        if self.refreshparty:
            time.sleep(1)
            try:
                opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=1), urllib2.HTTPCookieProcessor(self.cookies))
                urllib2.install_opener(opener)
                rsp = opener.open('http://localhost:3000/party')
            except IOError:
                print 'fail'
            else:
                party = json.loads(rsp.read())
                rsp.close()
                if party.has_key('player2'):
                    self.partyFrame.destroy()
                    self.selectchargui(party)
        return Task.cont

    def selectchargui(self, party):
        print 'selectchar'

Teest()
run()
