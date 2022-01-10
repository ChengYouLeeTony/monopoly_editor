"use strict";

class GameController {

    constructor(options) {
        this.initGame(options);
    }

    initGame(options) {
        const {containerEl, assetsUrl, userDataUrl, onBoardPainted} = options;

        this.boardController = new BoardController({
            containerEl: containerEl,
            assetsUrl: assetsUrl,
            userDataUrl: userDataUrl
        });

        this.boardController.drawBoard(onBoardPainted);
    }

    addPlayer(count, initPos, initDirection) {
        return this.boardController.drawPlayers(count, initPos, initDirection);
    }

    movePlayer(playerIndex, newTileId) {
        this.boardController.movePlayer(playerIndex, newTileId);
    }
    movePlayerCounterclockwise(playerIndex, newTileId) {
        this.boardController.movePlayerCounterclockwise(playerIndex, newTileId);
    }

    movePlayerBack(playerIndex, newTileId) {
        this.boardController.movePlayerBack(playerIndex, newTileId);
    }

    movePlayerBackClockwise(playerIndex, newTileId) {
        this.boardController.movePlayerBackClockwise(playerIndex, newTileId);
    }

    teleportPlayer(playerIndex, newTileId, isTurnOver) {
        this.boardController.teleportPlayer(playerIndex, newTileId, isTurnOver);
    }

    turnOverPlayer(playerIndex, isTurnOver) {
        this.boardController.turnOverPlayer(playerIndex, isTurnOver);
    }

    swapPlayer(playerIndex1, playerIndex2, playerPos1, playerPos2, playerIsTurnOver1, playerIsTurnOver2) {
        this.boardController.teleportPlayer(playerIndex1, playerPos2, playerIsTurnOver1);
        this.boardController.teleportPlayer(playerIndex2, playerPos1, playerIsTurnOver2);
    }

    swapAllPlayer(swapAllEventInfo) {
        for (let i = 0; i < swapAllEventInfo.length; i++) {
            let playerIndex = swapAllEventInfo[i][0];
            let playerNewPos = swapAllEventInfo[i][1];
            let playerIsTurnOver = swapAllEventInfo[i][2];
            this.boardController.teleportPlayer(playerIndex, playerNewPos, playerIsTurnOver);
        }
    }

    teleportAllPlayer(teleportAllRandomEventInfo) {
        for (let i = 0; i < teleportAllRandomEventInfo.length; i++) {
            let playerIndex = teleportAllRandomEventInfo[i][0];
            let playerNewPos = teleportAllRandomEventInfo[i][1];
            let playerIsTurnOver = teleportAllRandomEventInfo[i][2];
            this.boardController.teleportPlayer(playerIndex, playerNewPos, playerIsTurnOver);
        }
    }

    changeCameraPosition(nextPlayerPos, nextPlayerIsTurnOver) {
        this.boardController.changeCameraPosition(nextPlayerPos, nextPlayerIsTurnOver);
    }

    rotateCameraTheta(degree) {
        this.boardController.rotateCameraTheta(degree);
    }

    rotateCameraPhi(degree) {
        this.boardController.rotateCameraPhi(degree);
    }

    dollyCamera(value) {
        this.boardController.dollyCamera(value);
    }

    resetCamera() {
        this.boardController.resetCamera();
    }

    saveCameraState() {
        this.boardController.saveCameraState();
    }

    enableMouse( enabled ) {
        this.boardController. enableMouse( enabled );
    }

    addProperty(type, tileId, playerIndex) {
        if (type === PropertyManager.PROPERTY_OWNER_MARK) {
            this.boardController.addLandMark(playerIndex, tileId);
        } else {
            this.boardController.addProperty(type, tileId);
        }
    }

    resizeBoard() {
        this.boardController.resize();
    }
}
