"use strict";

class Player {

    constructor(options) {
        const {index, modelUrl, scene, initPos, initTileId, initDirection} = options;

        this.scene = scene;
        this.index = index;

        this.modelUrl = modelUrl;
        this.initPos = initPos;
        this.tileId = initTileId;
        this.initDirection = initDirection;
    }

    load() {
        return new Promise((resolve => {
            new THREE.ObjectLoader().load(
                this.modelUrl,

                (obj) => {
                    // Add the loaded object to the scene
                    this.model = obj;
                    this.model.position.set(this.initPos[0], Player.ELEVATION[this.index], this.initPos[2]);
                    this.model.scale.set(...Player.SCALES[this.index]);
                    if (this.initDirection === "clockwise") {
                        if (this.tileId <= 9 && this.tileId >= 0) {
                            this.rotate(90);
                        } else if (this.tileId <= 19 && this.tileId >= 10) {
                            this.rotate(0);
                        } else if (this.tileId <= 29 && this.tileId >= 20) {
                            this.rotate(-90);
                        } else if (this.tileId <= 39 && this.tileId >= 30) {
                            this.rotate(180);
                        }
                    } else if (this.initDirection === "counterClockwise") {
                        if (this.tileId <= 10 && this.tileId >= 1) {
                            this.rotate(-90);
                        } else if (this.tileId <= 20 && this.tileId >= 11) {
                            this.rotate(180);
                        } else if (this.tileId <= 30 && this.tileId >= 21) {
                            this.rotate(90);
                        } else if (this.tileId === 0 || this.tileId >= 31) {
                            this.rotate(0);
                        }
                    }
                    this.scene.add(this.model);
                    resolve();
                },

                // onProgress callback
                (xhr) => {
                    if (xhr.loaded === xhr.total) {
                        console.log(this.modelUrl + " loaded!");
                        resolve();
                    }
                },

                // onError callback
                (err) => {
                    console.error(err);
                });
        }))
    }

    rotate(degree) {
        this.model.rotation.y = THREE.Math.degToRad( degree );
    }

    advanceTo(newTileId, newPos) {
        this.model.position.set(newPos[0], Player.ELEVATION[this.index], newPos[2]);
        this.tileId = newTileId;
    }

    getTileId() {
        return this.tileId;
    }
}

Player.SCALES = [
    [0.04, 0.04, 0.04],
    [1.5, 1.5, 1.5],
    [0.03, 0.03, 0.03],
    [0.03, 0.03, 0.03]
];

Player.ELEVATION = [2.5, 2.0, 0, 0];