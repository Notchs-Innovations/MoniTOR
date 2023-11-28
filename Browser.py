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

        self.page().profile().setHttpUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")

        self.page().profile().downloadRequested.connect(self.downloadRequested)
        self.page().profile().setSpellCheckEnabled(True)

        self.setContextMenuPolicy(Qt.DefaultContextMenu)

    def downloadRequested(self, item):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", item.path(), "All Files (*);;Text Files (*.txt)", options=options)

        if file_path:
            item.setPath(file_path)
            item.accept()

class AdBlockProfile(QWebEngineProfile):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def requestInterceptor(self, info):
        url = info.requestUrl().toString()
        blocked_domains = ["ad.google.com"]

        for domain in blocked_domains:
            if domain in url:
                info.block(True)


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.setWindowTitle("Browser Settings")
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()

        search_engine_label = QLabel("Search Engine:")
        self.search_engine_combobox = QComboBox()
        self.search_engine_combobox.addItems(["Google", "DuckDuckGo", "Bing", "Custom"])
        layout.addWidget(search_engine_label)
        layout.addWidget(self.search_engine_combobox)

        new_tab_label = QLabel("New Tab Page:")
        self.new_tab_edit = QLineEdit()
        layout.addWidget(new_tab_label)
        layout.addWidget(self.new_tab_edit)

        home_page_label = QLabel("Home Page:")
        self.home_page_edit = QLineEdit()
        layout.addWidget(home_page_label)
        layout.addWidget(self.home_page_edit)

        save_button = QPushButton("Save")
        cancel_button = QPushButton("Cancel")
        save_button.clicked.connect(self.save_settings)
        cancel_button.clicked.connect(self.close)
        button_layout = QHBoxLayout()
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def save_settings(self):
        search_engine = self.search_engine_combobox.currentText()
        new_tab_page = self.new_tab_edit.text()
        home_page = self.home_page_edit.text()

        self.accept()

    def ShowSettings(self):
        dialog = SettingsDialog(self)
        result = dialog.exec()
        if result == QDialog.Accepted:
            search_engine = dialog.search_engine_combobox.currentText()
            new_tab_page = dialog.new_tab_edit.text()
            home_page = dialog.home_page_edit.text()

class AboutDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

        QBtn = QDialogButtonBox()
        self.buttonBox = QDialogButtonBox(QBtn)

        layout = QVBoxLayout()

        title = QLabel("MoniTOR")
        font = title.font()
        font.setPointSize(20)
        title.setFont(font)

        layout.addWidget(title)
        layout.addWidget(QLabel("Version 0.2.2"))
        layout.addWidget(QLabel("MoniTOR is a project in progress, with many features to modern browser features being developed."))
        layout.addWidget(QLabel("Copyright 2023 Notch_XVI"))

        layout.addWidget(self.buttonBox)

        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowIcon(QIcon(os.path.join('src/logos', 'icon.ico')))
        self.setGeometry(250, 100, 1350, 900)

        ToolBar = self.addToolBar("File")
        self.addToolBar(ToolBar)
        ToolBar.setMovable(False)

        self.Tab = QTabWidget()
        self.Tab.setTabsClosable(True)
        self.Tab.setMovable(True)
        self.Tab.setDocumentMode(True)
        self.setCentralWidget(self.Tab)

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
        self.DuplicateTabAction = QAction(None, self)
        self.MuteTabAction = QAction(None, self)

        self.Exit = QAction("Exit Browser", self)
        self.FullScreen = QAction("Toggle Fullscreen", self)

        self.Exit.setShortcut("Ctrl+Q")
        self.FullScreen.setShortcut("F11")
        self.openNewTab.setShortcut("CTRL+N")
        self.ZoomInButton.setShortcut('Ctrl++')
        self.ZoomOutButton.setShortcut('Ctrl+-')
        self.ResetZoomLevelButton.setShortcut('Ctrl+G')
        self.StopReloadButton.setShortcut('Esc')

        self.UrlField = QLineEdit()
        self.UrlField.setTextMargins(10, 0, 0, 0)
        self.UrlField.setPlaceholderText("Search or insert a URL...")
        self.UrlField.setClearButtonEnabled(True)
        self.UrlField.setFixedHeight(32.5)

        self.TextField = QLineEdit()
        self.TextField.setTextMargins(10, 0, 0, 0)
        self.TextField.setPlaceholderText("Search..")
        self.TextField.setClearButtonEnabled(True)
        self.TextField.setFixedSize(500, 32.5)

        ToolBar.addAction(self.BackButton)
        ToolBar.addAction(self.ForwardButton)
        ToolBar.addAction(self.ReloadButton)
        ToolBar.addAction(self.HomeButton)

        ToolBar.addSeparator()
        ToolBar.addAction(self.Security)
        ToolBar.addWidget(self.UrlField)
        ToolBar.addWidget(self.TextField)

        ToolBar.addAction(self.ZoomInButton)
        ToolBar.addAction(self.ZoomOutButton)
        ToolBar.addAction(self.SetZoomLevelButton)
        ToolBar.addAction(self.BookmarkButton)
        ToolBar.addAction(self.openNewTab)
        ToolBar.addAction(self.StopReloadButton)

        self.BackButton.triggered.connect(lambda: self.Tab.currentWidget().back)
        self.ForwardButton.triggered.connect(lambda:self.Tab.currentWidget().forward)
        self.ReloadButton.triggered.connect(lambda: self.Tab.currentWidget().reload)
        self.StopReloadButton.triggered.connect(lambda: self.Tab.currentWidget().stop)

        self.HomeButton.triggered.connect(self.GoHome)
        self.Security.triggered.connect(self.about)
        self.ZoomInButton.triggered.connect(self.ZoomIn)
        self.ZoomOutButton.triggered.connect(self.ZoomOut)
        self.SetZoomLevelButton.triggered.connect(self.SetZoomLevel)
        self.ResetZoomLevelButton.triggered.connect(self.ResetZoomLevel)

        self.openNewTab.triggered.connect(self.OpenNewTab)
        self.FullScreen.triggered.connect(self.toggleFullscreen)
        self.Exit.triggered.connect(self.close)

        self.NewTabShortcut = QShortcut(QKeySequence.AddTab, self)
        self.BackShortcut = QShortcut(QKeySequence.Back, self)
        self.ForwardShortcut = QShortcut(QKeySequence.Forward, self)
        self.FullScreen = QShortcut(QKeySequence.FullScreen, self)
        self.RefreshShortcut = QShortcut(QKeySequence.Refresh, self)

        self.NewTabShortcut.activated.connect(self.AddNewTab)
        self.UrlField.returnPressed.connect(self.Go2URL)
        self.TextField.returnPressed.connect(self.navigate_to_search)

        self.BackShortcut.activated.connect(lambda: self.Tab.currentWidget().back())
        self.ForwardShortcut.activated.connect(lambda: self.Tab.currentWidget().forward())
        self.RefreshShortcut.activated.connect(lambda: self.Tab.currentWidget().reload())

        self.OpenNewTab()
        self.changeAppareance("dark")
        self.EnableBetaFeature(0)

    def ActiveTab(self):
        return self.tabs.currentWidget().widget() if self.tabs.count() > 0 else None

    def UpdateApplicationIcon(self, icon):
        if icon and not icon.isNull():
            self.setWindowIcon(QIcon(icon))
        else:
            self.setWindowIcon(QIcon(os.path.join('images', 'icon.png')))

    def changeAppareance(self, mode):
        if mode == "light":
            self.loadStyleSheet(os.path.join("src\styles", "light_mode.css"))
            self.Security.setIcon(QIcon(os.path.join("src\images\lightmode_images", "lock.png")))
            self.BookmarkButton.setIcon(QIcon(os.path.join("src\images\lightmode_images", "bookmark.png")))
            self.HomeButton.setIcon(QIcon(os.path.join("src\images\lightmode_images", "home.png")))
            self.BackButton.setIcon(QIcon(os.path.join("src\images\lightmode_images", "left.png")))
            self.ReloadButton.setIcon(QIcon(os.path.join("src\images\lightmode_images", "refresh.png")))
            self.ForwardButton.setIcon(QIcon(os.path.join("src\images\lightmode_images", "right.png")))
            self.ZoomOutButton.setIcon(QIcon(os.path.join("src\images\lightmode_images", "zoom_out.png")))
            self.ZoomInButton.setIcon(QIcon(os.path.join("src\images\lightmode_images", "zoom_in.png")))
            self.SetZoomLevelButton.setIcon(QIcon(os.path.join("src\images\lightmode_images", "search.png")))

        elif mode == "dark":
            self.loadStyleSheet(os.path.join("src\styles", "dark_mode.css"))
            self.Security.setIcon(QIcon(os.path.join("src\images\darkmode_images", "lock.png")))
            self.BookmarkButton.setIcon(QIcon(os.path.join("src\images\darkmode_images", "bookmark.png")))
            self.SetZoomLevelButton.setIcon(QIcon(os.path.join("src\images\darkmode_images", "search.png")))
            self.HomeButton.setIcon(QIcon(os.path.join("src\images\darkmode_images", "home.png")))
            self.BackButton.setIcon(QIcon(os.path.join("src\images\darkmode_images", "left.png")))
            self.ReloadButton.setIcon(QIcon(os.path.join("src\images\darkmode_images", "refresh.png")))
            self.ForwardButton.setIcon(QIcon(os.path.join("src\images\darkmode_images", "right.png")))
            self.ZoomInButton.setIcon(QIcon(os.path.join("src\images\darkmode_images", "zoom_in.png")))
            self.ZoomOutButton.setIcon(QIcon(os.path.join("src\images\darkmode_images", "zoom_out.png")))

    def EnableBetaFeature(self, mode):
        if mode > 0:
            self.Tab.currentWidget().iconChanged.connect(self.UpdateApplicationIcon)
        else:
            return

    def OpenNewTab(self):
        self.AddNewTab("")
        self.goToSpecificUrl("https://search.brave.com/")

    def AudioToggle(self, state):
        AdBlockWebEngineView.page().setAudioMuted(state)

    def GoHome(self):
        self.Tab.currentWidget().setUrl(QUrl("https://search.brave.com/"))

    def goToSpecificUrl(self, url):
        self.Tab.currentWidget().setUrl(QUrl(url))

    def Go2URL(self):
        address = QUrl(self.UrlField.text())

        if address.scheme() == "":
            address.setScheme("https")

        self.Tab.currentWidget().setUrl(address)

    def UpdateURL(self, x, browser=None):
        if browser != self.Tab.currentWidget():
            return

        self.UrlField.setText(x.toString())
        url = self.Tab.currentWidget().url().toString()
        title = self.Tab.currentWidget().page().title()

    def toggleFullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def TabClose(self, i):
        if self.Tab.count() < 2:
            return
        self.Tab.removeTab(i)

    def DoubleClickTab(self, i):
        if i == -1:
            self.OpenNewTab()

    def AddNewTab(self, URL=None, label="New Tab"):
        if URL is None:
            URL = QUrl("")
        browser = AdBlockWebEngineView()
        browser.setUrl(QUrl(URL))
        i = self.Tab.addTab(browser, label)
        self.Tab.setCurrentIndex(i)
        browser.urlChanged.connect(lambda x_url, x_browser=browser: self.UpdateURL(x_url, x_browser))
        browser.loadFinished.connect(lambda _, x_i=i, x_browser=browser: self.Tab.setTabText(x_i, x_browser.page().title()))
        browser.iconChanged.connect(lambda icon, x_i=i: self.Tab.setTabIcon(x_i, QIcon(icon)))

    def DuplicateCurrentTab(self):
        current_index = self.Tab.currentIndex()
        current_tab = self.Tab.widget(current_index)
        if current_tab:
                self.AddNewTab(current_tab.url(), current_tab.page().title())

    def CurrentTabChanged(self):
        q_url = self.Tab.currentWidget().url()
        self.UpdateURL(q_url, self.Tab.currentWidget())
        self.UpdateTitle(self.Tab.currentWidget())

    def UpdateTitle(self, browser):
        if browser != self.Tab.currentWidget():
            return
        title = self.Tab.currentWidget().page().title()
        self.setWindowTitle(title)

    def ZoomIn(self):
        self.Tab.currentWidget().setZoomFactor(self.Tab.currentWidget().zoomFactor() + 0.1)

    def ZoomOut(self):
        self.Tab.currentWidget().setZoomFactor(self.Tab.currentWidget().zoomFactor() - 0.1)

    def SetZoomLevel(self):
        zoom, ok = QInputDialog.getDouble(self, "Set Zoom Level", "Zoom Level:", self.Tab.currentWidget().zoomFactor(), 0, 10, 1)
        if ok:
            self.Tab.currentWidget().setZoomFactor(zoom)

    def ResetZoomLevel(self):
        self.Tab.currentWidget().setZoomFactor(1)

    def loadStyleSheet(self, path):
        with open(path) as StyleSheet:
            self.setStyleSheet(StyleSheet.read())

    def about(self):
        Dialog = SettingsDialog()
        Dialog.exec()

    def ShowBookmarks(self):
        BookmarksDialog = BookmarksWidget()
        BookmarksDialog.exec_()

    def ShowHistory(self):
        HistoryDialog = HistoryWidget()
        HistoryDialog.exec_()

    def OpenFile(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Hypertext Markup Language (*.htm *.html)")

        with open(filename, 'r') as f:
            html = f.read()
            self.Tab.currentWidget().setHtml(html)
            self.UrlField.setText(filename)

    def ToggleFullscreenAction(self):
        action = QAction('Fullscreen', self, checkable=True)
        action.setStatusTip('Toggle fullscreen mode')
        action.setShortcut('F11')
        action.setChecked(False)
        action.toggled.connect(self.ToggleFullscreen)
        return action

    def ToggleFullscreen(self, state):
        if state:
            self.showFullScreen()
        else:
            self.showNormal()

    def ToggleInspectorAction(self):
        action = QAction('Toggle Web Inspector', self, checkable=True)
        action.setStatusTip('Toggle web inspector')
        action.setShortcut('Ctrl+Shift+I')
        action.setChecked(False)
        action.toggled.connect(self.ToggleInspector)
        return action

    def ToggleInspector(self, state):
        self.tabs.currentWidget().page().settings().setAttribute(QWebEngineSetting, state)

    def ClearHistory(self):
        reply = QMessageBox.question(self, 'Clear History', 'Are you sure you want to clear your history?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.browser.page().profile().clearAllVisitedLinks()

    def handle_pdf(self, data):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file, _ = QFileDialog.getSaveFileName(self, 'Save PDF', '', 'PDF Files (*.pdf);;All Files (*)', options=options)

        if file:
            with open(file, 'wb') as f:
                f.write(data)

    def navigate_to_search(self):
        query = self.TextField.text()

        #if QUrl.fromUserInput(query).isValid():
        #    self.Go2URL()
        #else:
        url = QUrl('https://search.brave.com/search?q=' + query)
        self.Tab.currentWidget().setUrl(url)