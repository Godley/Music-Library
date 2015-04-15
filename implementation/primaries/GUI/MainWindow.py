from PyQt4 import QtCore, QtGui, uic
from popplerqt4 import Poppler
import sys
import threading

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent):
        self.parent = parent

        #somewhere in constructor:
        QtGui.QMainWindow.__init__(self)
        uic.loadUi('designer_files/MainWindow.ui', self)

        #self.progressBarRendering.hide()
        options = ["title","composer","lyricist"]
        self.scoreSortCombo.addItems(options)


        autoSort = ["all", "time signatures","clefs","instruments","keys","tempos"]
        self.AutoSortCombo.addItems(autoSort)
        self.AutoSortCombo.show()

        # button handlers
        self.refreshScoreBtn.clicked.connect(self.refreshScores)
        self.refreshAutoBtn.clicked.connect(self.refreshPlaylists)
        self.AddPlaylistButton.clicked.connect(self.addPlaylist)
        self.searchInput.textChanged.connect(self.updateOptions)

        # search handlers
        self.searchInput.returnPressed.connect(self.searchDb)
        self.searchInput.editingFinished.connect(self.onInactiveSearchBar)
        self.searchBtn.clicked.connect(self.searchDb)

        # sorting of myScorebook and of the auto generated playlists box
        self.AutoSortCombo.currentIndexChanged.connect(self.onAutoSortMethodChange)
        self.scoreSortCombo.currentIndexChanged.connect(self.onSortMethodChange)

        # callbacks for loading pieces from autocomplete, from the scorebook or from a loaded playlist
        self.autoCompleteBox.itemDoubleClicked.connect(self.onAutoCompleteDoubleClicked)
        self.scoreListWidget.itemDoubleClicked.connect(self.onItemDoubleClicked)
        self.playlistTable.itemDoubleClicked.connect(self.onItemInPlaylistDoubleClicked)

        # playlist callbacks - these load the playlist into the main render window, or else show the delete button
        # in the case of my playlists
        self.autoPlaylistsView.itemDoubleClicked.connect(self.onAutoPlaylistDoubleClicked)
        self.myPlaylistsWidget.itemDoubleClicked.connect(self.onPlaylistDoubleClicked)
        self.myPlaylistsWidget.itemClicked.connect(self.deletePlaylistBtn.show)
        self.deletePlaylistBtn.clicked.connect(self.deletePlaylist)
        self.playlistList.itemDoubleClicked.connect(self.onItemDoubleClicked)

        # actions to show and hide various widgets
        self.actionMy_Scorebook.triggered.connect(self.onScorebookClicked)
        self.actionMy_Playlists.triggered.connect(self.onMyPlaylistsClicked)
        self.actionAuto_Playlists.triggered.connect(self.onAutoPlaylistsClicked)
        self.actionPiece_Information.triggered.connect(self.PieceInfoClicked)
        self.actionFeatured_in.triggered.connect(self.FeaturedInClicked)
        self.actionPlaylist_Browser.triggered.connect(self.PlaylistBrowserClicked)
        self.actionImport.triggered.connect(self.parent.importPopup)
        self.actionNew_Collection.triggered.connect(self.parent.makeNewCollection)

        # theme actions
        self.actionLight.triggered.connect(self.lightTheme)
        self.actionDark.triggered.connect(self.darkTheme)

        # on startup hide various widgets that aren't needed
        self.autoCompleteFrame.hide()
        self.pieceInfoWidget.hide()
        self.featuredInWidget.hide()
        self.playlistBrowserWidget.hide()
        self.playlistViewer.hide()
        self.noResultsLabel.hide()
        self.noResultsSmiley.hide()
        self.playBtn.hide()
        self.zoomInBtn.hide()
        self.zoomOutBtn.hide()
        self.deletePlaylistBtn.hide()

        # functionality for editing user generated playlists
        self.editPlaylistTitle.hide()
        self.playlistTitleLineEdit.hide()
        self.editPlaylistTitle.clicked.connect(self.onPlaylistEditClicked)
        self.playlistTitleLineEdit.returnPressed.connect(self.updatePlaylistTitle)

        # functionality for zooming in or out on a loaded piece
        self.zoomInBtn.clicked.connect(self.zoomIn)
        self.zoomOutBtn.clicked.connect(self.zoomOut)

    def runLoadingProcedure(self):
        self.parent.loadPieces()
        self.scoreListWidget.show()
        self.loadPlaylists()
        self.loadMyPlaylists()

    def onPlaylistReady(self, playlist_summaries):
        self.autoPlaylistsView.clear()
        for i in playlist_summaries:
            item = QtGui.QListWidgetItem(i)
            self.autoPlaylistsView.addItem(item)
            for j in playlist_summaries[i]:
                item = QtGui.QListWidgetItem(j)
                item.setData(1, playlist_summaries[i][j])
                item.setData(3, i+j)
                self.autoPlaylistsView.addItem(item)
        self.autoPlaylistsView.show()

    def onMyPlaylistsReady(self, myPlaylists):
        self.myPlaylistsWidget.clear()
        for entry in myPlaylists:
            item = QtGui.QListWidgetItem(entry)
            item.setData(1, myPlaylists[entry])
            item.setData(3, entry)
            self.myPlaylistsWidget.addItem(item)
        self.myPlaylistsWidget.show()

    def loadPlaylists(self, select_method="all"):
        self.parent.getPlaylists(select_method=select_method)


    def loadMyPlaylists(self):
        self.parent.getCreatedPlaylists()




    def onAutoPlaylistLoad(self):
        pass

    def onMyPlaylistLoad(self):
        pass

    def onScorebookLoad(self, pieces):
        self.scoreListWidget.clear()
        for i in pieces:
            item = QtGui.QListWidgetItem(i[0])
            item.setData(32, i[1])
            self.scoreListWidget.addItem(item)

    def darkTheme(self):
        file = open("themes/dark.qss",'r')
        fstring = file.readlines()
        self.setStyleSheet("".join(fstring))
        file.close()
        self.parent.theme = "light"
        self.repaint()

    def lightTheme(self):

        file = open("themes/light.qss",'r')
        fstring = file.readlines()
        self.setStyleSheet("".join(fstring))
        file.close()
        self.parent.theme = "light"
        self.repaint()


    def onScorebookClicked(self):
        self.scoreWidget.setHidden(not self.scoreWidget.isHidden())
        if not self.scoreWidget.isHidden():
            if not self.playlistWidget.isHidden():
                self.playlistWidget.move(0, 250)
                if not self.autoPlaylistWidget.isHidden():
                    self.autoPlaylistWidget.move(0,500)
            elif not self.autoPlaylistWidget.isHidden():
                self.autoPlaylistWidget.move(0,250)
        else:
            if not self.playlistWidget.isHidden():
                self.playlistWidget.move(0, 0)
                if not self.autoPlaylistWidget.isHidden():
                    self.autoPlaylistWidget.move(0,250)
            elif not self.autoPlaylistWidget.isHidden():
                self.autoPlaylistWidget.move(0,0)

    def onMyPlaylistsClicked(self):
        self.playlistWidget.setHidden(not self.playlistWidget.isHidden())
        yval=0
        if not self.playlistWidget.isHidden():
            if not self.scoreWidget.isHidden():
                yval=250
            self.playlistWidget.move(0, yval)
            if not self.autoPlaylistWidget.isHidden():
                self.autoPlaylistWidget.move(0, yval+250)
        else:
            if not self.autoPlaylistWidget.isHidden():
                yval=0
                if not self.scoreWidget.isHidden():
                    yval=250
                self.autoPlaylistWidget.move(0, yval)

    def onAutoPlaylistsClicked(self):
        self.autoPlaylistWidget.setHidden(not self.autoPlaylistWidget.isHidden())
        yval=0
        if not self.autoPlaylistWidget.isHidden():
            if not self.scoreWidget.isHidden():
                yval+=250
            if not self.playlistWidget.isHidden():
                yval += 250
            self.autoPlaylistWidget.move(0, yval)

    def PieceInfoClicked(self):
        self.pieceInfoWidget.setHidden(not self.pieceInfoWidget.isHidden())
        if not self.pieceInfoWidget.isHidden():
            if not self.featuredInWidget.isHidden():
                self.featuredInWidget.move(0, 250)
                if not self.playlistBrowserWidget.isHidden():
                    self.playlistBrowserWidget.move(0,500)
            elif not self.playlistBrowserWidget.isHidden():
                self.playlistBrowserWidget.move(0,250)
        else:
            if not self.featuredInWidget.isHidden():
                self.featuredInWidget.move(0, 0)
                if not self.playlistBrowserWidget.isHidden():
                    self.playlistBrowserWidget.move(0,250)
            elif not self.playlistBrowserWidget.isHidden():
                self.playlistBrowserWidget.move(0,0)


    def FeaturedInClicked(self):
        self.featuredInWidget.setHidden(not self.featuredInWidget.isHidden())
        yval=0
        if not self.featuredInWidget.isHidden():
            if not self.pieceInfoWidget.isHidden():
                yval=250
            self.featuredInWidget.move(0, yval)
            if not self.playlistBrowserWidget.isHidden():
                self.playlistBrowserWidget.move(0, yval+250)
        else:
            if not self.playlistBrowserWidget.isHidden():
                yval=0
                if not self.pieceInfoWidget.isHidden():
                    yval=250
                self.playlistBrowserWidget.move(0, yval)


    def PlaylistBrowserClicked(self):
        self.playlistBrowserWidget.setHidden(not self.playlistBrowserWidget.isHidden())
        yval=0
        if not self.playlistBrowserWidget.isHidden():
            if not self.pieceInfoWidget.isHidden():
                yval+=250
            if not self.featuredInWidget.isHidden():
                yval += 250
            self.playlistBrowserWidget.move(0, yval)

    def deletePlaylist(self):
        items = self.myPlaylistsWidget.selectedItems()
        names = [item.data(2) for item in items]
        self.parent.removePlaylists(names)
        [self.myPlaylistsWidget.takeItem(self.myPlaylistsWidget.row(thing)) for thing in items]
        self.myPlaylistsWidget.show()

    def updatePlaylistTitle(self):
        text = self.playlistTitleLineEdit.text()
        old_value = self.musicTitle.text()
        self.parent.updatePlaylistTitle(text, old_value)
        self.musicTitle.setText(text)
        self.musicTitle.repaint()
        self.playlistTitleLineEdit.hide()
        self.editPlaylistTitle.show()
        self.loadMyPlaylists()

    def closeEvent(self, event):
        self.parent.startUp()
        event.accept()


    def onPlaylistEditClicked(self):
        title = self.musicTitle.text()
        self.playlistTitleLineEdit.setText(title)
        self.playlistTitleLineEdit.show()
        self.editPlaylistTitle.hide()

    def onItemInPlaylistDoubleClicked(self, current_item):
        playlist = current_item.data(4)
        index_in_playlist = current_item.data(3)
        data = self.parent.getPlaylistFileInfo(playlist)
        if self.playlistList.rowCount() != 0:
            self.playlistList.clear()
            self.playlistList.setHorizontalHeaderItem(0, QtGui.QTableWidgetItem("Title"))
            self.playlistList.setHorizontalHeaderItem(1, QtGui.QTableWidgetItem("Composer"))
            self.playlistList.setHorizontalHeaderItem(2, QtGui.QTableWidgetItem("Filename"))
        self.playlistList.setRowCount(len(data))
        for i in range(len(data)):
            if "composer" in data[i]:
                item = QtGui.QTableWidgetItem(data[i]["composer"])
                item.setData(1,data[i]["filename"])
                self.playlistList.setItem(i, 1, item)
            else:
                item = QtGui.QTableWidgetItem("")
                item.setData(1, data[i]["filename"])
                self.playlistList.setItem(i, 1, item)

            if "title" in data[i]:
                item = QtGui.QTableWidgetItem(data[i]["title"])
                item.setData(1,data[i]["filename"])
                self.playlistList.setItem(i, 0, item)
            else:
                item = QtGui.QTableWidgetItem("")
                item.setData(1, data[i]["filename"])
                self.playlistList.setItem(i, 0, item)

            if "filename" in data[i]:
                item = QtGui.QTableWidgetItem(data[i]["filename"])
                item.setData(1, data[i]["filename"])
                self.playlistList.setItem(i, 2, item)
            else:
                item = QtGui.QTableWidgetItem("")
                item.setData(1, data[i]["filename"])
                self.playlistList.setItem(i, 2, item)

        self.playlistList.selectRow(index_in_playlist)
        self.playlistList.show()
        self.playlistBrowserWidget.show()
        self.onItemDoubleClicked(current_item)
        self.actionPlaylist_Browser.setChecked(True)


    def showToolbarBtns(self):
        self.playBtn.show()
        self.zoomInBtn.show()
        self.zoomOutBtn.show()

    def hideToolbarBtns(self):
        self.playBtn.hide()
        self.zoomInBtn.hide()
        self.zoomOutBtn.hide()

    def setUpDataItems(self, playlist_fnames, playlist_data, start_index, end_index):
        items = []
        for i in range(start_index, end_index):
            file = playlist_data[i]
            row = []
            item = QtGui.QTableWidgetItem(file["title"])
            item.setData(1, file["filename"])
            item.setData(3, i)
            item.setData(4, playlist_fnames)
            row.append(item)
            if "composer" in file:
                item = QtGui.QTableWidgetItem(file["composer"])
                item.setData(1, file["filename"])
                item.setData(3, i)
                item.setData(4, playlist_fnames)
                row.append(item)

            else:
                item = QtGui.QTableWidgetItem("")
                item.setData(1, file["filename"])
                item.setData(3, i)
                item.setData(4, playlist_fnames)
                row.append(item)

            if "lyricist" in file:
                item = QtGui.QTableWidgetItem(file["lyricist"])
                item.setData(1, file["filename"])
                item.setData(3, i)
                item.setData(4, playlist_fnames)
                row.append(item)

            else:
                item = QtGui.QTableWidgetItem("")
                item.setData(1, file["filename"])
                item.setData(3, i)
                item.setData(4, playlist_fnames)
                row.append(item)

            if "instruments" in file:
                item = QtGui.QTableWidgetItem(", ".join([data["name"] for data in file["instruments"]]))
                item.setData(1, file["filename"])
                item.setData(3, i)
                item.setData(4, playlist_fnames)
                row.append(item)

            else:
                item = QtGui.QTableWidgetItem("")
                item.setData(1, file["filename"])
                item.setData(3, i)
                item.setData(4, playlist_fnames)
                row.append(item)
            item = QtGui.QTableWidgetItem(file["filename"])
            item.setData(1, file["filename"])
            item.setData(3, i)
            item.setData(4, playlist_fnames)
            row.append(item)
            if "clefs" in file:
                result = ""
                for instrument in file["clefs"]:
                    result += ", ".join(file["clefs"][instrument])
                item = QtGui.QTableWidgetItem(result)
                item.setData(3, i)
                item.setData(4, playlist_fnames)
                item.setData(1, file["filename"])
                row.append(item)

            else:
                item = QtGui.QTableWidgetItem("")
                item.setData(1, file["filename"])
                item.setData(3, i)
                item.setData(4, playlist_fnames)
                row.append(item)
            if "keys" in file:
                result = ""
                for instrument in file["keys"]:
                    result += ", ".join(file["keys"][instrument])
                item = QtGui.QTableWidgetItem(result)
                item.setData(1, file["filename"])
                item.setData(3, i)
                item.setData(4, playlist_fnames)
                row.append(item)

            else:
                item = QtGui.QTableWidgetItem("")
                item.setData(1, file["filename"])
                item.setData(3, i)
                item.setData(4, playlist_fnames)
                row.append(item)

            if "tempos" in file:
                item = QtGui.QTableWidgetItem(", ".join(file["tempos"]))
                item.setData(1, file["filename"])
                item.setData(3, i)
                item.setData(4, playlist_fnames)
                row.append(item)

            else:
                item = QtGui.QTableWidgetItem("")
                item.setData(1, file["filename"])
                item.setData(3, i)
                item.setData(4, playlist_fnames)
                row.append(item)

            if "time_signatures" in file:
                item = QtGui.QTableWidgetItem(", ".join(file["time_signatures"]))
                item.setData(1, file["filename"])
                item.setData(3, i)
                item.setData(4, playlist_fnames)
                row.append(item)

            else:
                item = QtGui.QTableWidgetItem("")
                item.setData(1, file["filename"])
                item.setData(3, i)
                item.setData(4, playlist_fnames)
                row.append(item)
            items.append(row)
        return items


    def onAutoPlaylistDoubleClicked(self, current_item):
        self.onPlaylistDoubleClicked(current_item)
        self.editPlaylistTitle.hide()

    def onPlaylistDoubleClicked(self, current_item):
        self.scoreWindow.hide()
        playlist_to_load = current_item.data(1)
        length = len(playlist_to_load)
        playlist_title = current_item.data(3)
        self.playlistTable.setRowCount(length)
        file_data = self.parent.getPlaylistFileInfo(playlist_to_load)
        data_items = self.setUpDataItems(playlist_to_load, file_data, 0, len(file_data))
        for i in range(len(data_items)):
            for j in range(len(data_items[i])):
                self.playlistTable.setItem(i, j, data_items[i][j])
        self.musicTitle.setText(playlist_title)
        self.editPlaylistTitle.show()
        self.playlistTable.show()
        self.playlistViewer.show()
        self.hideToolbarBtns()
        self.clearUnusedWidgets()


    def onInactiveSearchBar(self):
        if self.searchInput.text() == "" or self.searchInput.text() == " " or self.autoCompleteBox.topLevelItemCount() == 0\
                or self.focusWidget() != self.autoCompleteBox:
            self.autoCompleteBox.clear()
            self.autoCompleteFrame.hide()
            self.autoCompleteBox.hide()

    def onAutoCompleteDoubleClicked(self, current_item):
        self.scoreWindow.show()
        #self.progressBarRendering.show()
        #self.progressBarRendering.setRange(0, 100)
        self.autoCompleteFrame.hide()
        self.editPlaylistTitle.hide()
        file_to_load = current_item.data(0,32)
        self.loadPiece(file_to_load)

    def onItemDoubleClicked(self, current_item):
        self.scoreWindow.show()
        #self.progressBarRendering.show()
        #self.progressBarRendering.setRange(0, 100)
        self.editPlaylistTitle.hide()
        file_to_load = current_item.data(1)
        self.loadPiece(file_to_load)

    def onPieceLoaded(self, filename, split_file):
        """
        :param filename: the fully qualified filename location including folder
        :param split_file: the filename with no folder location
        :return:
        """
        file_to_load = split_file.split(".")[0]+".xml"
        self.showToolbarBtns()
        self.loadPieceData(file_to_load)
        self.pdf_view(filename)
        self.musicTitle.setText(file_to_load)
        self.musicTitle.repaint()
        self.loadFeaturedIn(file_to_load)
        self.playlistViewer.hide()
        self.pieceInfoWidget.show()

    def loadPiece(self, file_to_load):
        self.parent.loadFile(file_to_load)


    def updateProgressBar(self):
        bar_value = self.progressBarRendering.value()
        self.progressBarRendering.setValue(bar_value+1)
        self.progressBarRendering.repaint()

    def loadFeaturedIn(self, filename):
        data = self.parent.loadUserPlaylistsForAGivenFile(filename)
        self.featuredListWidget.clear()
        for item in data:
            widget = QtGui.QListWidgetItem(item)
            widget.setData(1, data[item])
            self.featuredListWidget.addItem(widget)
        self.featuredListWidget.show()
        self.featuredInWidget.show()
        self.actionFeatured_in.setChecked(True)

    def clearUnusedWidgets(self):
        self.featuredListWidget.clear()
        self.featuredInWidget.hide()
        self.pieceInfoView.clear()
        self.pieceInfoWidget.hide()
        self.playlistList.clear()
        self.playlistList.setHorizontalHeaderItem(0, QtGui.QTableWidgetItem("Title"))
        self.playlistList.setHorizontalHeaderItem(1, QtGui.QTableWidgetItem("Composer"))
        self.playlistList.setHorizontalHeaderItem(2, QtGui.QTableWidgetItem("Filename"))
        self.playlistList.setRowCount(0)
        self.playlistBrowserWidget.hide()

    def loadPieceData(self, filename):
        self.pieceInfoView.clear()
        data = self.parent.getFileInfo(filename)[0]

        datastring = "title: "+data["title"]
        title = QtGui.QListWidgetItem(datastring)
        self.pieceInfoView.addItem(title)
        if "composer" in data and data["composer"] != -1:
            datastring = "composer: "+data["composer"]
            composer = QtGui.QListWidgetItem(datastring)
            self.pieceInfoView.addItem(composer)
        if "lyricist" in data and data["lyricist"] != -1:
            datastring = "lyricist: "+data["lyricist"]
            lyricist = QtGui.QListWidgetItem(datastring)
            self.pieceInfoView.addItem(lyricist)
        if "instruments" in data:
            datastring = "instruments: "+", ".join([d["name"] for d in data["instruments"]])
            instruments = QtGui.QListWidgetItem(datastring)
            self.pieceInfoView.addItem(instruments)
        if "clefs" in data:
            datastring = "clefs: "
            clef_list = []
            for instrument in data["clefs"]:
                for clef in data["clefs"][instrument]:
                    if clef not in clef_list:
                        clef_list.append(clef)
            datastring += ", ".join(clef_list)
            clefs = QtGui.QListWidgetItem(datastring)
            self.pieceInfoView.addItem(clefs)
        if "keys" in data:
            datastring = "keys: "
            key_list = []
            for instrument in data["keys"]:
                for key in data["keys"][instrument]:
                    if key_list not in key_list:
                        key_list.append(key)
            datastring += ", ".join(key_list)
            keys = QtGui.QListWidgetItem(datastring)
            self.pieceInfoView.addItem(keys)

        if "tempos" in data:
            datastring = "tempos: "
            tempo_list = []
            for tempo in data["tempos"]:
                datastring += tempo
                datastring += ", "
            tempos = QtGui.QListWidgetItem(datastring)
            self.pieceInfoView.addItem(tempos)

        if "time_signatures" in data:
            datastring = "time signatures: "
            tempo_list = []
            for tempo in data["time_signatures"]:
                datastring += tempo
                datastring += ", "
            tempos = QtGui.QListWidgetItem(datastring)
            self.pieceInfoView.addItem(tempos)

        self.pieceInfoView.show()
        self.pieceInfoWidget.show()
        self.actionPiece_Information.setChecked(True)

    def zoomIn(self):
        '''
        callback for zoom in button
        :return:
        '''
        self.scoreWindow.scale(1.1, 1.1)

    def zoomOut(self):
        '''
        callback for zoom out button
        :return:
        '''
        self.scoreWindow.scale(0.9, 0.9)

    def pdf_view(self, filename):
        """Return a Scrollarea showing the first page of the specified PDF file."""

        scene = QtGui.QGraphicsScene()
        scene.setBackgroundBrush(QtGui.QColor('darkGray'))
        layout = QtGui.QGraphicsLinearLayout(QtCore.Qt.Vertical)
        doc = Poppler.Document.load(filename)
        doc.setRenderHint(Poppler.Document.Antialiasing)
        doc.setRenderHint(Poppler.Document.TextAntialiasing)


        pageNum = doc.numPages()
        for number in range(pageNum):
            page = doc.page(number)
            image = page.renderToImage(100, 100)
            pixmap = QtGui.QPixmap.fromImage(image)
            container = QtGui.QLabel()
            container.setFixedSize(page.pageSize())
            container.setStyleSheet("Page { background-color : transparent}")
            container.setContentsMargins(0, 0, 0, 0)
            container.setScaledContents(True)
            container.setPixmap(pixmap)
            label = scene.addWidget(container)
            opacity = QtGui.QGraphicsOpacityEffect(self)
            opacity.setOpacity(0.5)
            label.setGraphicsEffect(opacity)
            layout.addItem(label)

        graphicsWidget = QtGui.QGraphicsWidget()
        graphicsWidget.setLayout(layout)
        scene.addItem(graphicsWidget)
        #self.view = View(scene)
        #self.scoreWindow.scale(1,1)
        #self.scoreWindow.scale(1.4,1.4)
        self.scoreWindow.setScene(scene)


    def onAutoSortMethodChange(self):
        sort_method = self.AutoSortCombo.currentText()
        self.loadPlaylists(select_method=sort_method)

    def onSortMethodChange(self):
        sort_method = self.scoreSortCombo.currentText()
        self.parent.loadPieces(method=sort_method)
        self.scoreListWidget.show()

    def refreshScores(self):
        self.parent.updateDb()
        self.onSortMethodChange()


    def refreshPlaylists(self):
        self.parent.updateDb()
        self.loadPlaylists()

    def addPlaylist(self):
        self.parent.PlaylistPopup()
        self.loadMyPlaylists()

    def searchDb(self):
        print("finding thing")

    def onQueryReturned(self, results):
        root = self.autoCompleteBox.invisibleRootItem()
        child_count = root.childCount()
        children = [(i, root.child(i).text(0)) for i in range(child_count)]
        names = [child[1] for child in children]
        for location_type in results:
            item = QtGui.QTreeWidgetItem(location_type)
            item.setData(0,0,location_type)
            if location_type in names:
                index = [child[0] for child in children if child[1] == location_type]
                item = root.child(index[0])
                for i in range(item.childCount()):
                    child = item.child(i)
                    item.removeChild(child)

            else:
                self.autoCompleteBox.addTopLevelItem(item)
            for key in results[location_type]:
                sub_item = QtGui.QTreeWidgetItem(key)
                sub_item.setData(0,0,key)
                item.addChild(sub_item)
                for file in results[location_type][key]:
                    fitem = QtGui.QTreeWidgetItem(file[0])
                    fitem.setData(0, 0, file[0])
                    fitem.setData(0, 32, file[1])
                    sub_item.addChild(fitem)
        if len(results) == 0:
            self.noResultsSmiley.show()
            self.noResultsLabel.show()
        else:
            self.noResultsSmiley.hide()
            self.noResultsLabel.hide()

        self.autoCompleteBox.show()
        self.autoCompleteFrame.show()

    def updateOptions(self):
        text = self.searchInput.text()
        self.autoCompleteBox.clear()
        self.parent.query(text)
        self.autoCompleteBox.show()
        self.autoCompleteFrame.show()



class View(QtGui.QGraphicsView):

    def __init__(self, parent = None):
        QtGui.QGraphicsView.__init__(self, parent)


    def zoomIn(self):
        self.scale(1.1, 1.1)

    def zoomOut(self):
        self.scale(0.9, 0.9)

