import os
import sys
from sys import argv
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineCore import *
from PyQt5.QtWebEngineWidgets import *

class AdBlockWebEngineView(QWebEngineView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        settings = self.page().settings()
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.AutoLoadImages, True)
        settings.setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        self.page().profile().setHttpUserAgent("Your User Agent Here")
        self.page().downloadRequested.connect(MainWindow.download)
        self.page().setSpellCheckEnabled(True)

class AboutDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

class MainWindow(QMainWindow):
    def __init__(self):
        super(AboutDialog, self).__init__(*args, **kwargs)
        self.setWindowIcon(QIcon(os.path.join('resources/logos', 'icon.png'))

        self.Tab = QTabWidget()
        self.setCentralWidget(self.Tab)
        self.Tab.setDocumentMode(True)
        self.Tab.setTabsClosable(True)
        self.Tab.setMovable(True)  # Allow tab reordering

        self.Tab.tabCloseRequested.connect(self.TabClose)
        self.Tab.tabBarDoubleClicked.connect(self.DoubleClickTab)
        self.Tab.currentChanged.connect(self.CurrentTabChanged)

        self.BackButton = QAction(None, self)
        self.ForwardButton = QAction(None, self)
        self.ReloadButton = QAction(None, self)
        self.StopReloadButton = QAction(None, self)
        self.HomeButton = QAction(None, self)
        self.Security = QAction(None, self)
        self.ZoomInButton = QAction(None, self)
        self.ZoomOutButton = QAction(None, self)
        self.SetZoomLevelButton = QAction(None, self)
        self.ResetZoomLevelButton = QAction(None, self)
        self.BookmarkButton = QAction(None, self)
        self.openNewTab = QAction(None, self)
        self.DuplicateTabAction = QAction(None, self)  # Added for duplicating tabs
        self.MuteTabAction = QAction(None, self)  # Added for muting/unmuting tabs

        # ... (other actions and widgets)

    def TabClose(self, index):
        if self.Tab.count() > 1:
            widget = self.Tab.widget(index)
            widget.deleteLater()
            self.Tab.removeTab(index)
        elif self.Tab.count() == 1:
            self.Tab.setTabText(0, "New Tab")
            self.Tab.widget(0).setUrl(QUrl("about:blank"))

    def DoubleClickTab(self, index):
        self.AddNewTab()

    def AddNewTab(self, URL=None, label="New Tab"):
        if URL is None:
            URL = QUrl("about:blank")
        browser = AdBlockWebEngineView()
        browser.setUrl(URL)

        i = self.Tab.addTab(browser, label)
        self.Tab.setCurrentIndex(i)

        browser.urlChanged.connect(lambda x_url, x_browser=browser: self.UpdateURL(x_url, x_browser))
        browser.loadFinished.connect(lambda _, x_i=i, x_browser=browser: self.UpdateTabTitle(x_i, x_browser))

        # Add a pin/unpin button
        pin_button = QPushButton("Pin", browser)
        pin_button.setCheckable(True)
        pin_button.setChecked(False)
        pin_button.clicked.connect(lambda state, x_i=i, x_browser=browser: self.TogglePinTab(x_i, x_browser, state))
        self.Tab.tabBar().setTabButton(i, QTabBar.LeftSide, pin_button)

        # Add a mute/unmute button
        mute_button = QPushButton("Mute", browser)
        mute_button.setCheckable(True)
        mute_button.setChecked(False)
        mute_button.clicked.connect(lambda state, x_i=i, x_browser=browser: self.ToggleMuteTab(x_i, x_browser, state))
        self.Tab.tabBar().setTabButton(i, QTabBar.RightSide, mute_button)

    def CurrentTabChanged(self, index):
        if index >= 0 and index < self.Tab.count():
            tab = self.Tab.widget(index)
            if tab:
                self.UpdateURL(tab.url(), tab)

    def UpdateTabTitle(self, index, browser):
        if index >= 0 and index < self.Tab.count() and browser == self.Tab.widget(index):
            title = browser.page().title()
            self.Tab.setTabText(index, title)

    def DuplicateCurrentTab(self):
        current_index = self.Tab.currentIndex()
        current_tab = self.Tab.widget(current_index)
        if current_tab:
            self.AddNewTab(current_tab.url(), current_tab.page().title())

    def TogglePinTab(self, index, browser, state):
        if state:
            self.Tab.setTabText(index, "📌 " + self.Tab.tabText(index))
        else:
            self.Tab.setTabText(index, self.Tab.tabText(index)[2:])

    def ToggleMuteTab(self, index, browser, state):
        browser.setAudioMuted(state)
        if state:
            self.Tab.setTabText(index, "🔇 " + self.Tab.tabText(index))
        else:
            self.Tab.setTabText(index, self.Tab.tabText(index)[2:])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("MoniTOR")
    app.setOrganizationName("notch")
    app.setOrganizationDomain("imnotchxvi.itch.io")
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())
