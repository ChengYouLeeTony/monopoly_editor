"use strict";
CameraControls.install( { THREE: THREE } );

class BoardController {

    constructor(options) {
        this.containerEl = options.containerEl;
        this.assetsUrl = options.assetsUrl;
        this.userDataUrl = options.userDataUrl;
        this.mapID = document.getElementById("map-id").value;
        this.lands_image_url = document.getElementById("lands-image-url").value;

        this.board = new Board();
        this.players = [];
    }

    drawBoard(callback) {
        this.initEngine();
        this.initLights();
        this.initMaterials();

        this.initObjects(() => {
            this.onAnimationFrame();

            callback();
        });
    }

    drawPlayers(number, initPos, initDirection) {
        let promiseList = [];
        return new Promise((resolve => {
            for (let i = 0; i < number; i++) {
                let player = new Player({
                    index: i,
                    modelUrl: `${this.assetsUrl}/players/${i}/model.json`,
                    scene: this.scene,
                    initTileId: initPos[i],
                    initPos: this.boardToWorld({
                        tileId: initPos[i],
                        type: BoardController.MODEL_PLAYER,
                        total: number,
                        index: i
                    }),
                    initDirection: initDirection[i],
                });

                this.board.updateTileInfo(initPos[i], {
                    type: BoardController.MODEL_PLAYER,
                    action: "add",
                    playerIndex: i
                });
                this.players.push(player);
                promiseList.push(player.load());
            }

            Promise.all(promiseList).then(() => {
                resolve();
            })
        }))
    }

    movePlayer(index, newTileId) {
        let currTileId = this.players[index].getTileId();
        console.log("index and new tile id is: " + currTileId.toString() + " " + newTileId.toString());

        // Remove previous player position
        this.board.updateTileInfo(currTileId, {
            type: BoardController.MODEL_PLAYER,
            action: "remove",
            playerIndex: index
        });

        // Register new player position
        this.board.updateTileInfo(newTileId, {
            type: BoardController.MODEL_PLAYER,
            action: "add",
            playerIndex: index
        });

        // Animation: move the player
        return new Promise((resolve => {
            let playerMovementInterval = setInterval(() => {
                currTileId += 1;
                currTileId %= BoardController.TILE_MAX + 1;
                const tileInfo = this.board.getTileInfo(currTileId);
                const tilePlayerCount = tileInfo.players.reduce((a, b) => a + b, 0);

                // this.cameraControls.setPosition( player_pos_world[0] - BoardController.SQUARE_SIZE * 3, 50, player_pos_world[2], true )
                // this.cameraControls.setTarget(player_pos_world[0], player_pos_world[1], player_pos_world[2], true);
                // console.log(this.cameraControls.getPosition());

                this.players[index].advanceTo(currTileId, this.boardToWorld({
                    tileId: currTileId,
                    type: BoardController.MODEL_PLAYER,
                    total: tilePlayerCount + 1,
                    index: tilePlayerCount
                }));

                let angle = THREE.Math.degToRad( -90 );
                if (currTileId === 10) {
                    this.players[index].rotate(0);                    
                    this.cameraControls.rotate( angle, 0, true );
                } else if (currTileId === 20) {
                    this.players[index].rotate(-90);
                    this.cameraControls.rotate( angle, 0, true );
                } else if (currTileId === 30) {
                    this.players[index].rotate(180);
                    this.cameraControls.rotate( angle, 0, true );
                } else if (currTileId === 0) {
                    this.players[index].rotate(90);
                    this.cameraControls.rotate( angle, 0, true );
                }

                if (currTileId === newTileId) {
                    clearInterval(playerMovementInterval);
                    resolve();
                }
            }, 200);
        }));
    }

    movePlayerBack(index, newTileId) {
        let currTileId = this.players[index].getTileId();
        console.log("index and new tile id is: " + currTileId.toString() + " " + newTileId.toString());

        // Remove previous player position
        this.board.updateTileInfo(currTileId, {
            type: BoardController.MODEL_PLAYER,
            action: "remove",
            playerIndex: index
        });

        // Register new player position
        this.board.updateTileInfo(newTileId, {
            type: BoardController.MODEL_PLAYER,
            action: "add",
            playerIndex: index
        });
        //rotate back at first
        if (currTileId <= 10 && currTileId >= 1) {
            this.players[index].rotate(-90);
        } else if (currTileId <= 20 && currTileId >= 11) {
            this.players[index].rotate(180);
        } else if (currTileId <= 30 && currTileId >= 21) {
            this.players[index].rotate(90);
        } else if (currTileId === 0 || currTileId >= 31) {
            this.players[index].rotate(0);
        }

        // Animation: move the player
        return new Promise((resolve => {
            let playerMovementInterval = setInterval(() => {
                currTileId -= 1;
                if (currTileId < 0) {
                    currTileId += BoardController.TILE_MAX + 1;
                }
                const tileInfo = this.board.getTileInfo(currTileId);
                const tilePlayerCount = tileInfo.players.reduce((a, b) => a + b, 0);

                this.players[index].advanceTo(currTileId, this.boardToWorld({
                    tileId: currTileId,
                    type: BoardController.MODEL_PLAYER,
                    total: tilePlayerCount + 1,
                    index: tilePlayerCount
                }));

                let angle = THREE.Math.degToRad( 90 );
                if (currTileId === 10) {
                    this.players[index].rotate(-90);
                    this.cameraControls.rotate( angle, 0, true );
                } else if (currTileId === 20) {
                    this.players[index].rotate(180);
                    this.cameraControls.rotate( angle, 0, true );
                } else if (currTileId === 30) {
                    this.players[index].rotate(90);
                    this.cameraControls.rotate( angle, 0, true );
                } else if (currTileId === 0) {
                    this.players[index].rotate(0);
                    this.cameraControls.rotate( angle, 0, true );
                }

                if (currTileId === newTileId) {
                    //rotate back at last
                    if (currTileId <= 9 && currTileId >= 0) {
                        this.players[index].rotate(90);
                    } else if (currTileId <= 19 && currTileId >= 10) {
                        this.players[index].rotate(0);
                    } else if (currTileId <= 29 && currTileId >= 20) {
                        this.players[index].rotate(-90);
                    } else if (currTileId <= 39 && currTileId >= 30) {
                        this.players[index].rotate(180);
                    }
                    clearInterval(playerMovementInterval);
                    resolve();
                }
            }, 200);
        }));
    }

    movePlayerCounterclockwise(index, newTileId) {
        let currTileId = this.players[index].getTileId();
        console.log("index and new tile id is: " + currTileId.toString() + " " + newTileId.toString());

        // Remove previous player position
        this.board.updateTileInfo(currTileId, {
            type: BoardController.MODEL_PLAYER,
            action: "remove",
            playerIndex: index
        });

        // Register new player position
        this.board.updateTileInfo(newTileId, {
            type: BoardController.MODEL_PLAYER,
            action: "add",
            playerIndex: index
        });

        // Animation: move the player
        return new Promise((resolve => {
            let playerMovementInterval = setInterval(() => {
                currTileId -= 1;
                if (currTileId < 0) {
                    currTileId += BoardController.TILE_MAX + 1;
                }
                const tileInfo = this.board.getTileInfo(currTileId);
                const tilePlayerCount = tileInfo.players.reduce((a, b) => a + b, 0);

                this.players[index].advanceTo(currTileId, this.boardToWorld({
                    tileId: currTileId,
                    type: BoardController.MODEL_PLAYER,
                    total: tilePlayerCount + 1,
                    index: tilePlayerCount
                }));
                let angle = THREE.Math.degToRad( 90 );
                if (currTileId === 10) {
                    this.players[index].rotate(-90);
                    this.cameraControls.rotate( angle, 0, true );
                } else if (currTileId === 20) {
                    this.players[index].rotate(180);
                    this.cameraControls.rotate( angle, 0, true );
                } else if (currTileId === 30) {
                    this.players[index].rotate(90);
                    this.cameraControls.rotate( angle, 0, true );
                } else if (currTileId === 0) {
                    this.players[index].rotate(0);
                    this.cameraControls.rotate( angle, 0, true );
                }

                if (currTileId === newTileId) {
                    clearInterval(playerMovementInterval);
                    resolve();
                }
            }, 200);
        }));
    }

    movePlayerBackClockwise(index, newTileId) {
        let currTileId = this.players[index].getTileId();
        console.log("index and new tile id is: " + currTileId.toString() + " " + newTileId.toString());

        // Remove previous player position
        this.board.updateTileInfo(currTileId, {
            type: BoardController.MODEL_PLAYER,
            action: "remove",
            playerIndex: index
        });

        // Register new player position
        this.board.updateTileInfo(newTileId, {
            type: BoardController.MODEL_PLAYER,
            action: "add",
            playerIndex: index
        });

        //rotate back at first
        if (currTileId <= 9 && currTileId >= 0) {
            this.players[index].rotate(90);
        } else if (currTileId <= 19 && currTileId >= 10) {
            this.players[index].rotate(0);
        } else if (currTileId <= 29 && currTileId >= 20) {
            this.players[index].rotate(-90);
        } else if (currTileId <= 39 && currTileId >= 30) {
            this.players[index].rotate(180);
        }

        // Animation: move the player
        return new Promise((resolve => {
            let playerMovementInterval = setInterval(() => {
                currTileId += 1;
                currTileId %= BoardController.TILE_MAX + 1;
                const tileInfo = this.board.getTileInfo(currTileId);
                const tilePlayerCount = tileInfo.players.reduce((a, b) => a + b, 0);

                this.players[index].advanceTo(currTileId, this.boardToWorld({
                    tileId: currTileId,
                    type: BoardController.MODEL_PLAYER,
                    total: tilePlayerCount + 1,
                    index: tilePlayerCount
                }));

                let angle = THREE.Math.degToRad( 90 );
                if (currTileId === 10) {
                    this.players[index].rotate(0);
                    this.cameraControls.rotate( angle, 0, true );
                } else if (currTileId === 20) {
                    this.players[index].rotate(-90);
                    this.cameraControls.rotate( angle, 0, true );
                } else if (currTileId === 30) {
                    this.players[index].rotate(180);
                    this.cameraControls.rotate( angle, 0, true );
                } else if (currTileId === 0) {
                    this.players[index].rotate(90);
                    this.cameraControls.rotate( angle, 0, true );
                }

                if (currTileId === newTileId) {
                    //rotate back at last
                    if (currTileId <= 10 && currTileId >= 1) {
                        this.players[index].rotate(-90);
                    } else if (currTileId <= 20 && currTileId >= 11) {
                        this.players[index].rotate(180);
                    } else if (currTileId <= 30 && currTileId >= 21) {
                        this.players[index].rotate(90);
                    } else if (currTileId === 0 || currTileId >= 31) {
                        this.players[index].rotate(0);
                    }
                    clearInterval(playerMovementInterval);
                    resolve();
                }
            }, 200);
        }));
    }

    teleportPlayer(index, newTileId, isTurnOver) {
        let currTileId = this.players[index].getTileId();
        console.log("index and new tile id is: " + currTileId.toString() + " " + newTileId.toString());

        // Remove previous player position
        this.board.updateTileInfo(currTileId, {
            type: BoardController.MODEL_PLAYER,
            action: "remove",
            playerIndex: index
        });

        // Register new player position
        this.board.updateTileInfo(newTileId, {
            type: BoardController.MODEL_PLAYER,
            action: "add",
            playerIndex: index
        });
        const tileInfo = this.board.getTileInfo(newTileId);
        const tilePlayerCount = tileInfo.players.reduce((a, b) => a + b, 0);
        this.players[index].advanceTo(newTileId, this.boardToWorld({
            tileId: newTileId,
            type: BoardController.MODEL_PLAYER,
            total: tilePlayerCount + 1,
            index: tilePlayerCount
        }));
        //change the player direction
        if (isTurnOver == "false") {
            if (newTileId <= 9 && newTileId >= 0) {
                this.players[index].rotate(90);
            } else if (newTileId <= 19 && newTileId >= 10) {
                this.players[index].rotate(0);
            } else if (newTileId <= 29 && newTileId >= 20) {
                this.players[index].rotate(-90);
            } else if (newTileId <= 39 && newTileId >= 30) {
                this.players[index].rotate(180);
            }
        } else {
            if (newTileId <= 10 && newTileId >= 1) {
                this.players[index].rotate(-90);
            } else if (newTileId <= 20 && newTileId >= 11) {
                this.players[index].rotate(180);
            } else if (newTileId <= 30 && newTileId >= 21) {
                this.players[index].rotate(90);
            } else if (newTileId === 0 || newTileId >= 31) {
                this.players[index].rotate(0);
            }
        }
    }

    turnOverPlayer(index, isTurnOver) {
        let currTileId = this.players[index].getTileId();
        if (isTurnOver === "false") {
            if (currTileId <= 10 && currTileId >= 1) {
                this.players[index].rotate(-90);
            } else if (currTileId <= 20 && currTileId >= 11) {
                this.players[index].rotate(180);
            } else if (currTileId <= 30 && currTileId >= 21) {
                this.players[index].rotate(90);
            } else if (currTileId === 0 || currTileId >= 31) {
                this.players[index].rotate(0);
            }
        } else {
            if (currTileId <= 9 && currTileId >= 0) {
                this.players[index].rotate(90);
            } else if (currTileId <= 19 && currTileId >= 10) {
                this.players[index].rotate(0);
            } else if (currTileId <= 29 && currTileId >= 20) {
                this.players[index].rotate(-90);
            } else if (currTileId <= 39 && currTileId >= 30) {
                this.players[index].rotate(180);
            }
        }
        //change the camera position
        if (isTurnOver === "false") {
            if (currTileId === 10) {
               this.cameraControls.setPosition( 40.0015, 100, 160, true );
            } else if (currTileId === 20) {
                this.cameraControls.setPosition( -79.997, 100, 40.0015, true );
            } else if (currTileId === 30) {
                this.cameraControls.setPosition( 40.0015, 100, -80, true );
            } else if (currTileId === 0) {
                this.cameraControls.setPosition( 160, 100, 40.0015, true );
            }
        } else {
            if (currTileId === 10) {
                this.cameraControls.setPosition( -79.997, 100, 40.0015, true );
            } else if (currTileId === 20) {
                 this.cameraControls.setPosition( 40.0015, 100, -80, true );
            } else if (currTileId === 30) {
                this.cameraControls.setPosition( 160, 100, 40.0015, true );
            } else if (currTileId === 0) {
                this.cameraControls.setPosition( 40.0015, 100, 160, true );
            }

        }        
    }

    changeCameraPosition(nextPlayerPos, nextPlayerIsTurnOver) {
        //change camera position
        if (nextPlayerIsTurnOver == "false") {
            if (nextPlayerPos <= 9 && nextPlayerPos >= 0) {
                this.cameraControls.setPosition( 40.0015, 100, 160, false );
            } else if (nextPlayerPos <= 19 && nextPlayerPos >= 10) {
                this.cameraControls.setPosition( -79.997, 100, 40.0015, false );
            } else if (nextPlayerPos <= 29 && nextPlayerPos >= 20) {
                this.cameraControls.setPosition( 40.0015, 100, -80, false );
            } else if (nextPlayerPos <= 39 && nextPlayerPos >= 30) {
                this.cameraControls.setPosition( 160, 100, 40.0015, false );
            }
        } else {
            if (nextPlayerPos <= 10 && nextPlayerPos >= 1) {
                this.cameraControls.setPosition( 40.0015, 100, 160, false );
            } else if (nextPlayerPos <= 20 && nextPlayerPos >= 11) {
                this.cameraControls.setPosition( -79.997, 100, 40.0015, false );
            } else if (nextPlayerPos <= 30 && nextPlayerPos >= 21) {
                this.cameraControls.setPosition( 40.0015, 100, -80, false );
            } else if (nextPlayerPos === 0 || nextPlayerPos >= 31) {
                this.cameraControls.setPosition( 160, 100, 40.0015, false );
            }
        }
        this.cameraControls.saveState();
    }

    rotateCameraTheta(degree) {
        let rad = THREE.Math.degToRad( degree );
        this.cameraControls.rotate( rad, 0, true );
    }

    rotateCameraPhi(degree) {
        let rad = THREE.Math.degToRad( degree );
        this.cameraControls.rotate( 0, rad, true );
    }

    dollyCamera(value) {
        this.cameraControls.dolly( value, true );
    }

    resetCamera() {
        this.cameraControls.reset( true);
    }

    saveCameraState() {
        this.cameraControls.saveState();
    }

    enableMouse( enabled ) {
        this.cameraControls.enabled = enabled;
    }

    addProperty(type, tileId) {
        let tileInfo = this.board.getTileInfo(tileId);
        const tilePropertyCount = tileInfo.propertyManager.getPropertyCount();

        if (type === PropertyManager.PROPERTY_HOUSE) {
            tileInfo.propertyManager.buildHouse(this.boardToWorld({
                tileId: tileId,
                type: BoardController.MODEL_PROPERTY,
                total: tilePropertyCount + 2
            }), tileId);
        } else if (type === PropertyManager.PROPERTY_HOTEL) {
            tileInfo.propertyManager.buildHotel(this.boardToWorld({
                tileId: tileId,
                type: BoardController.MODEL_PROPERTY,
                total: 2
            }), tileId);
        }
    }

    addLandMark(playerIndex, tileId) {
        let tileInfo = this.board.getTileInfo(tileId);
        this.board.updateTileInfo(tileId, {
            type: BoardController.MODEL_PROPERTY,
            options: {
                loadedHouseJson: this.houseModelJson,
                loadedHotelJson: this.hotelModelJson,
                scene: this.scene
            }
        });

        tileInfo.propertyManager.buyLand(this.boardToWorld({
            tileId: tileId,
            type: BoardController.MODEL_PROPERTY,
            total: 1
        }), tileId, playerIndex);
    }

    initEngine() {
        let viewWidth = this.containerEl.offsetWidth;
        let viewHeight = this.containerEl.offsetHeight;

        // instantiate the WebGL this.renderer
        this.renderer = new THREE.WebGLRenderer({
            antialias: true,
            alpha: true
        });
        this.renderer.setSize(viewWidth, viewHeight);
        this.renderer.setPixelRatio(window.devicePixelRatio);
        // create the this.scene
        this.scene = new THREE.Scene();

        // create this.camera
        this.camera = new THREE.PerspectiveCamera(25, viewWidth / viewHeight, 1, 1000);
        this.camera.position.set(BoardController.SQUARE_SIZE * Board.SIZE / 2, 100, 160);
        this.clock = new THREE.Clock();
        this.cameraControls = new CameraControls( this.camera, this.renderer.domElement );
        this.cameraControls.setTarget( BoardController.SQUARE_SIZE * Board.SIZE / 2, -6, BoardController.SQUARE_SIZE * Board.SIZE / 2, false );
        this.cameraControls.saveState();
        this.cameraControls.enabled = false;

        this.scene.add(this.camera);

        this.containerEl.appendChild(this.renderer.domElement);
         
    
    }

    initLights() {
        this.lights = {};

        // top light
        this.lights.topLight = new THREE.PointLight();
        this.lights.topLight.position.set(BoardController.SQUARE_SIZE * Board.SIZE / 2, 150, BoardController.SQUARE_SIZE * Board.SIZE / 2);
        this.lights.topLight.intensity = 0.4;

        // white's side light
        this.lights.whiteSideLight = new THREE.SpotLight();
        this.lights.whiteSideLight.position.set(BoardController.SQUARE_SIZE * Board.SIZE / 2, 100, BoardController.SQUARE_SIZE * Board.SIZE / 2 - 300);
        this.lights.whiteSideLight.intensity = 1;
        this.lights.whiteSideLight.shadow.camera.Fov = 55;

        // black's side light
        this.lights.blackSideLight = new THREE.SpotLight();
        this.lights.blackSideLight.position.set(BoardController.SQUARE_SIZE * Board.SIZE / 2, 100, BoardController.SQUARE_SIZE * Board.SIZE / 2 + 300);
        this.lights.blackSideLight.intensity = 1;
        this.lights.blackSideLight.shadow.camera.Fov = 55;

        // light that will follow the this.camera position
        this.lights.movingLight = new THREE.PointLight(0xf9edc9);
        this.lights.movingLight.position.set(0, 20, 0);
        this.lights.movingLight.intensity = 0.5;
        this.lights.movingLight.distance = 500;

        // add the this.lights in the this.scene
        this.scene.add(this.lights.topLight);
        this.scene.add(this.lights.whiteSideLight);
        this.scene.add(this.lights.blackSideLight);
        this.scene.add(this.lights.movingLight);
    }

    initMaterials() {
        this.materials = {};

        // board material
        this.materials.boardMaterial = new THREE.MeshLambertMaterial({
            map: new THREE.TextureLoader().load(`${this.assetsUrl}/board_texture.jpg`)
        });

        // ground material
        this.materials.groundMaterial = new THREE.MeshBasicMaterial({
            transparent: true,
            map: new THREE.TextureLoader().load(`${this.assetsUrl}/ground.png`)
        });
         // tile material
        var lands_image_url_list = this.lands_image_url.split(",")
        for(let i = 0; i < lands_image_url_list.length; i++) {
            if (i == 0) {
                lands_image_url_list[i] = lands_image_url_list[i].replaceAll("[", "");
            }
            if (i == lands_image_url_list.length-1) {
                lands_image_url_list[i] = lands_image_url_list[i].replaceAll("]", "");
            }
            lands_image_url_list[i] = lands_image_url_list[i].replaceAll("\"", "");
        }
        const defaultTileMaterial = new THREE.MeshLambertMaterial({
            map: new THREE.TextureLoader().load(lands_image_url_list[lands_image_url_list.length - 1])
        });

       
        this.materials.tileMaterial = [];
        for (let row = 0; row < Board.SIZE; row++) {
            let rowMaterial = [];
            for (let col = 0; col < Board.SIZE; col++) {
                const tileModelIndex = Board.posToTileId(row, col);
                var tileUrl = (tileModelIndex != -1) ? lands_image_url_list[tileModelIndex] : null;

                const tileMaterial = (tileModelIndex === -1) ? defaultTileMaterial : new THREE.MeshLambertMaterial({
                    // map: new THREE.TextureLoader().load(`${this.assetsUrl}/tiles/${tileModelIndex}.png`)
                    // map: new THREE.TextureLoader().load(`${this.userDataUrl}/map/${this.mapID}/${tileModelIndex}.png`)
                    map: new THREE.TextureLoader().load(tileUrl)
                });
                rowMaterial.push(tileMaterial);
            }
            this.materials.tileMaterial.push(rowMaterial);
        }
    }

    initObjects(callback) {
        let loader = new THREE.JSONLoader();
        let totalObjectsToLoad = 3; // board
        let loadedObjects = 0;

        const checkLoading = () => {
            loadedObjects += 1;
            if (loadedObjects === totalObjectsToLoad && callback) {
                callback();
            }
        };

        // load board
        loader.load(`${this.assetsUrl}/board.js`, (geom) => {
            this.boardModel = new THREE.Mesh(geom, this.materials.boardMaterial);
            this.boardModel.position.y = -0.02;

            this.scene.add(this.boardModel);

            checkLoading();
        });


        // add ground
        this.groundModel = new THREE.Mesh(new THREE.PlaneGeometry(100, 100, 1, 1), this.materials.groundMaterial);
        this.groundModel.position.set(BoardController.SQUARE_SIZE * Board.SIZE / 2, -1.52, BoardController.SQUARE_SIZE * Board.SIZE / 2);
        this.groundModel.rotation.x = -90 * Math.PI / 180;
        this.scene.add(this.groundModel);

        for (let row = 0; row < Board.SIZE; row++) {
            for (let col = 0; col < Board.SIZE; col++) {
                let square = new THREE.Mesh(new THREE.PlaneGeometry(BoardController.SQUARE_SIZE, BoardController.SQUARE_SIZE, 1, 1), this.materials.tileMaterial[row][col]);

                square.position.x = col * BoardController.SQUARE_SIZE + BoardController.SQUARE_SIZE / 2;
                square.position.z = row * BoardController.SQUARE_SIZE + BoardController.SQUARE_SIZE / 2;
                square.position.y = -0.01;

                square.rotation.x = -90 * Math.PI / 180;

                this.scene.add(square);
            }
        }

        // pre-load house model
        let requestModelJson = (type) => {
            let request = new XMLHttpRequest();
            request.open("GET", `${this.assetsUrl}/${type}/model.json`, false);
            request.send(null);

            checkLoading();
            return JSON.parse(request.responseText);
        };

        this.houseModelJson = requestModelJson("house");
        this.hotelModelJson = requestModelJson("hotel");
    }

    onAnimationFrame() {

        const delta = this.clock.getDelta();
        const hasControlsUpdated = this.cameraControls.update( delta );
        // this.cameraController.update();

        // update moving light position
        this.lights.movingLight.position.x = this.camera.position.x;
        this.lights.movingLight.position.z = this.camera.position.z;
        requestAnimationFrame(() => this.onAnimationFrame());

        this.renderer.render(this.scene, this.camera);
    }

    resize() {
        this.camera.aspect = window.innerWidth / window.innerHeight;
        this.camera.updateProjectionMatrix();

        this.renderer.setSize(window.innerWidth, window.innerHeight);
    }

    boardToWorld(options) {
        const {tileId, type, total, index} = options;
        const pos = Board.tileIdToPos(tileId);
        let x = 0.5 + pos[1];
        let z = 0.5 + pos[0];

        const side = Board.tileIdToSide(tileId);

        if (type === BoardController.MODEL_PLAYER) {
            if (total === 1) {
                return [x * BoardController.SQUARE_SIZE, 0, z * BoardController.SQUARE_SIZE];
            } else {
                switch (side) {
                    case Board.SIDE_TOP:
                        z -= BoardController.MODEL_PLAYER_MARGIN;
                        x = (index % 2 === 0) ? x + BoardController.MODEL_PLAYER_OFFSET : x - BoardController.MODEL_PLAYER_OFFSET;
                        if (total > 2) z = (index < 2) ? z + BoardController.MODEL_PLAYER_OFFSET : z - BoardController.MODEL_PLAYER_OFFSET;
                        break;
                    case Board.SIDE_BOTTOM:
                        z += BoardController.MODEL_PLAYER_MARGIN;
                        x = (index % 2 === 0) ? x - BoardController.MODEL_PLAYER_OFFSET : x + BoardController.MODEL_PLAYER_OFFSET;
                        if (total > 2) z = (index < 2) ? z - BoardController.MODEL_PLAYER_OFFSET : z + BoardController.MODEL_PLAYER_OFFSET;
                        break;
                    case Board.SIDE_LEFT:
                        x -= BoardController.MODEL_PLAYER_MARGIN;
                        z = (index % 2 === 0) ? z - BoardController.MODEL_PLAYER_OFFSET : z + BoardController.MODEL_PLAYER_OFFSET;
                        if (total > 2) x = (index < 2) ? x + BoardController.MODEL_PLAYER_OFFSET : x - BoardController.MODEL_PLAYER_OFFSET;
                        break;
                    case Board.SIDE_RIGHT:
                        x += BoardController.MODEL_PLAYER_MARGIN;
                        z = (index % 2 === 0) ? z + BoardController.MODEL_PLAYER_OFFSET : z - BoardController.MODEL_PLAYER_OFFSET;
                        if (total > 2) x = (index < 2) ? x - BoardController.MODEL_PLAYER_OFFSET : x + BoardController.MODEL_PLAYER_OFFSET;
                        break;
                }
            }
        } else if (type === BoardController.MODEL_PROPERTY) {
            switch (side) {
                case Board.SIDE_TOP:
                    z += BoardController.MODEL_PROPERTY_TOP_MARGIN;
                    x += BoardController.MODEL_PROPERTY_LEFT_MARGIN;
                    x -= (total - 1) * BoardController.MODEL_PROPERTY_MARGIN + BoardController.MODEL_PROPERTY_LEFT_OFFSET * (total > 1);
                    break;
                case Board.SIDE_BOTTOM:
                    z -= BoardController.MODEL_PROPERTY_TOP_MARGIN;
                    x -= BoardController.MODEL_PROPERTY_LEFT_MARGIN;
                    x += (total - 1) * BoardController.MODEL_PROPERTY_MARGIN + BoardController.MODEL_PROPERTY_LEFT_OFFSET * (total > 1);
                    break;
                case Board.SIDE_LEFT:
                    x += BoardController.MODEL_PROPERTY_TOP_MARGIN;
                    z -= BoardController.MODEL_PROPERTY_LEFT_MARGIN;
                    z += (total - 1) * BoardController.MODEL_PROPERTY_MARGIN + BoardController.MODEL_PROPERTY_LEFT_OFFSET * (total > 1);
                    break;
                case Board.SIDE_RIGHT:
                    x -= BoardController.MODEL_PROPERTY_TOP_MARGIN;
                    z += BoardController.MODEL_PROPERTY_LEFT_MARGIN;
                    z -= (total - 1) * BoardController.MODEL_PROPERTY_MARGIN + BoardController.MODEL_PROPERTY_LEFT_OFFSET * (total > 1);
                    break;
            }
        }
        return [x * BoardController.SQUARE_SIZE, 0, z * BoardController.SQUARE_SIZE];
    }
}

BoardController.SQUARE_SIZE = 7.273;
BoardController.MODEL_PLAYER = 0;
BoardController.MODEL_PROPERTY = 1;
BoardController.MODEL_PLAYER_OFFSET = 0.2;
BoardController.MODEL_PLAYER_MARGIN = 0.1;
BoardController.MODEL_PROPERTY_TOP_MARGIN = 0.39;
BoardController.MODEL_PROPERTY_LEFT_MARGIN = 0.37;
BoardController.MODEL_PROPERTY_MARGIN = 0.24;
BoardController.MODEL_PROPERTY_LEFT_OFFSET = 0.05;
BoardController.TILE_MAX = 39;
