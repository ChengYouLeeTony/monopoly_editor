"use strict";

class AudioManager {
    constructor(music_setting_info) {
        let audioList = [{
            key: "background",
            path: this.makeAudioPath(music_setting_info["background"], "background"),
            loop: true,
            volume: parseInt(music_setting_info["volume_background"], 10) / 100
        }, {
            key: "money_deduction",
            path: this.makeAudioPath(music_setting_info["money_deduction"], "cash"),
            loop: false,
            volume: parseInt(music_setting_info["volume_money_deduction"], 10) / 100
        }, {
            key: "money_addition",
            path: this.makeAudioPath(music_setting_info["money_addition"], "coin"),
            loop: false,
            volume: parseInt(music_setting_info["volume_money_addition"], 10) / 100
        }, {
            key: "dice",
            path: this.makeAudioPath(music_setting_info["dice"], "dice"),
            loop: false,
            volume: parseInt(music_setting_info["volume_dice"], 10) / 100
        }, {
            key: "hover_button",
            path: this.makeAudioPath(music_setting_info["hover_button"], "hover"),
            loop: false,
            volume: parseInt(music_setting_info["volume_hover_button"], 10) / 100
        }, {
            key: "build",
            path: this.makeAudioPath(music_setting_info["build"], "build"),
            loop: false,
            volume: parseInt(music_setting_info["volume_build"], 10) / 100
        }, {
            key: "player_move",
            path: this.makeAudioPath(music_setting_info["player_move"], "move"),
            loop: false,
            volume: parseInt(music_setting_info["volume_player_move"], 10) / 100
        }, {
            key: "player_teleport",
            path: this.makeAudioPath(music_setting_info["player_teleport"], "teleport"),
            loop: false,
            volume: parseInt(music_setting_info["volume_player_teleport"], 10) / 100
        }, {
            key: "player_turn_over",
            path: this.makeAudioPath(music_setting_info["player_turn_over"], "turnover"),
            loop: false,
            volume: parseInt(music_setting_info["volume_player_turn_over"], 10) / 100
        }, {
            key: "wrong_answer",
            path: this.makeAudioPath(music_setting_info["wrong_answer"], "wrong_answer"),
            loop: false,
            volume: parseInt(music_setting_info["volume_wrong_answer"], 10) / 100
        }, {
            key: "user_define_1",
            path: this.makeAudioPath(music_setting_info["user_define_1"], "user_define"),
            loop: false,
            volume: parseInt(music_setting_info["volume_user_define_1"], 10) / 100
        }, {
            key: "user_define_2",
            path: this.makeAudioPath(music_setting_info["user_define_2"], "user_define"),
            loop: false,
            volume: parseInt(music_setting_info["volume_user_define_2"], 10) / 100
        }, {
            key: "user_define_3",
            path: this.makeAudioPath(music_setting_info["user_define_3"], "user_define"),
            loop: false,
            volume: parseInt(music_setting_info["volume_user_define_3"], 10) / 100
        }, {
            key: "scoreboard_bgm",
            path: this.makeAudioPath(music_setting_info["scoreboard_bgm"], null),
            loop: true,
            volume: 0.6
        }];
        
        this.audioPlayers = {};
        for (let audio of audioList) {
            this.audioPlayers[audio.key] = new Audio(audio.path);
            if (audio.loop) this.audioPlayers[audio.key].loop = true;
            if (audio.volume) this.audioPlayers[audio.key].volume = audio.volume;
            if (audio.muted) this.audioPlayers[audio.key].muted = audio.muted;
        }
        this.backgroundVolume = this.audioPlayers["background"].volume;

        this.playing = true;
    }

    play(audio) {
        console.log(this.audioPlayers);
        if (!this.playing) return;
        this.audioPlayers[audio].play();
    }

    play_url(url) {
        if (!this.playing) return;
        let audio_url = new Audio(url);
        audio_url.play();
    }

    change_background_sound_to(url) {
        if (!this.playing) return;
        this.stop("background");
        this.audioPlayers["background"] = new Audio(url);
        this.audioPlayers["background"].loop = true;
        this.audioPlayers["background"].volume = 0.6;
        this.audioPlayers["background"].play();
    }

    stop(audio) {
        if (!this.playing) return;
        this.audioPlayers[audio].pause();
        this.audioPlayers[audio].currentTime = 0;
    }

    mute() {
        this.playing = !this.playing;
        this.audioPlayers["background"].volume = this.backgroundVolume * this.playing;
    }

    isAudioLink(url) {
        if(typeof url !== 'string') return false;
        return(url.match(/^http[^\?]*.(mp3|ogg|wav)(\?(.*))?$/gmi) != null);
    }

    isUserDataAudio(url) {
        if(typeof url !== 'string') return false;
        return(url.match(/.(mp3|ogg|wav)(\?(.*))?$/gmi) != null);
    }

    isGoogleDriveDownload(url) {
        if(typeof url !== 'string') return false;
        return(url.match(/https:\/\/docs\.google\.com\//) != null);
    }

    makeAudioPath(path, key) {
        let audio_path;
        if (path === "預設") {
            if (key === "user_define") {
                audio_path = "";
            } else if (key === "background") {
                audio_path = 'https://monopolyuserupload.blob.core.windows.net/userdata/music/default/bgm/background.mp3';
            } else {
                audio_path = 'https://monopolyuserupload.blob.core.windows.net/userdata/music/default/se/' + key + '.mp3';
            }
        } else if (this.isAudioLink(path)) {
            audio_path = path;
        } else if (this.isUserDataAudio(path)) {
            audio_path = 'https://monopolyuserupload.blob.core.windows.net/userdata/music/' + path;
        } else if (this.isGoogleDriveDownload(path)) {
            audio_path = path;
        } else if (path === "") {
            audio_path = "";
        }
        return audio_path
    }
}