"use strict";

class AudioManager {
    constructor() {
        const audioList = [{
            key: "background",
            loop: true,
            volume: 0.6,
            format: "mp3",
            type: "bgm"
        }, {
            key: "hover",
            loop: false,
            volume: 1.0,
            format: "mp3",
            type: "se"
        }, {
            key: "dice",
            loop: false,
            volume: 1.0,
            format: "mp3",
            type: "se"
        }, {
            key: "move",
            loop: false,
            volume: 1.0,
            format: "mp3",
            type: "se"
        }, {
            key: "build",
            loop: false,
            volume: 1.0,
            format: "mp3",
            type: "se"
        }, {
            key: "cash",
            loop: false,
            volume: 1.0,
            format: "mp3",
            type: "se"
        }, {
            key: "teleport",
            loop: false,
            volume: 1.0,
            format: "mp3",
            type: "se"
        }, {
            key: "turnover",
            loop: false,
            volume: 1.0,
            format: "mp3",
            type: "se"
        }, {
            key: "coin",
            loop: false,
            volume: 1.0,
            format: "mp3",
            type: "se"
        }, {
            key: "game_win",
            loop: false,
            volume: 1.0,
            format: "wav",
            type: "se"
        }, {
            key: "score_board_bgm_0",
            loop: true,
            volume: 1.0,
            format: "mp3",
            type: "bgm"
        }];

        this.audioPlayers = {};
        for (let audio of audioList) {
            this.audioPlayers[audio.key] = new Audio(`https://monopolyuserupload.blob.core.windows.net/userdata/music/default/${audio.type}/${audio.key}.${audio.format}`);
            if (audio.loop) this.audioPlayers[audio.key].loop = true;
            if (audio.volume) this.audioPlayers[audio.key].volume = audio.volume;
        }

        this.playing = true;
    }

    play(audio) {
        if (!this.playing) return;
        this.audioPlayers[audio].play();
    }

    mute() {
        this.playing = !this.playing;
        this.audioPlayers["background"].volume = 0.6 * this.playing;
    }
}