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
            key: "score_board_bgm_0",
            loop: true,
            volume: 0.3,
            format: "mp3",
            type: "bgm"
        }, {
            key: "score_board_bgm_1",
            loop: true,
            volume: 0.3,
            format: "mp3",
            type: "bgm"
        }];

        this.audioPlayers = {};
        for (let audio of audioList) {
            if (audio.key === "background") {
                let background_music_setting = document.getElementById('background_music_setting').value;
                console.log(background_music_setting);
                if (background_music_setting === "預設") {
                    this.audioPlayers[audio.key] = new Audio(`https://monopolyuserupload.blob.core.windows.net/userdata/music/default/bgm/background.mp3`);
                } else if(this.isGoogleDriveDownload(background_music_setting)) {
                    this.audioPlayers[audio.key] = new Audio(background_music_setting);
                } else {
                    this.audioPlayers[audio.key] = new Audio(`https://monopolyuserupload.blob.core.windows.net/userdata/music/${background_music_setting}`);
                }
            }
            else {
                this.audioPlayers[audio.key] = new Audio(`https://monopolyuserupload.blob.core.windows.net/userdata/music/default/${audio.type}/${audio.key}.${audio.format}`);
            }
            if (audio.loop) this.audioPlayers[audio.key].loop = true;
            if (audio.volume) this.audioPlayers[audio.key].volume = audio.volume;
        }

        this.playing = true;
    }

    isGoogleDriveDownload(url) {
        if(typeof url !== 'string') return false;
        return(url.match(/https:\/\/docs\.google\.com\//) != null);
    }

    play(audio) {
        if (!this.playing) return;
        this.audioPlayers[audio].play();
    }

    stop(audio) {
        this.audioPlayers[audio].pause();
        this.audioPlayers[audio].currentTime = 0;
    }

    mute() {
        this.playing = !this.playing;
        this.audioPlayers["background"].volume = 0.6 * this.playing;
    }
}