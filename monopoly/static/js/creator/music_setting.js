$("#music-setting-form input").attr("placeholder", "請輸入音樂網址或從音樂庫中複製");
$("#music-setting-form input").after('<button type="button" class="w3-button w3-black preview-button"><i class="fas fa-play"></i>聽聽看</button>');
$("#id_background").after(`<span class="w3-button w3-black volume-control-button" style="height:32px;"><span>音量: </span><input type="range" id="vol_id_background" name="vol_id_background" min="0" max="100" value="${volume_setting_info['volume_background']}"></span>`);
$("#id_money_deduction").after(`<span class="w3-button w3-black volume-control-button" style="height:32px;"><span>音量: </span><input type="range" id="vol_id_money_deduction" name="vol_id_money_deduction" min="0" max="100" value="${volume_setting_info['volume_money_deduction']}"></span>`);
$("#id_money_addition").after(`<span class="w3-button w3-black volume-control-button" style="height:32px;"><span>音量: </span><input type="range" id="vol_id_money_addition" name="vol_id_money_addition" min="0" max="100" value="${volume_setting_info['volume_money_addition']}"></span>`);
$("#id_dice").after(`<span class="w3-button w3-black volume-control-button" style="height:32px;"><span>音量: </span><input type="range" id="vol_id_dice" name="vol_id_dice" min="0" max="100" value="${volume_setting_info['volume_dice']}"></span>`);
$("#id_build").after(`<span class="w3-button w3-black volume-control-button" style="height:32px;"><span>音量: </span><input type="range" id="vol_id_build" name="vol_id_build" min="0" max="100" value="${volume_setting_info['volume_hover_button']}"></span>`);
$("#id_hover_button").after(`<span class="w3-button w3-black volume-control-button" style="height:32px;"><span>音量: </span><input type="range" id="vol_id_hover_button" name="vol_id_hover_button" min="0" max="100" value="${volume_setting_info['volume_build']}"></span>`);
$("#id_player_move").after(`<span class="w3-button w3-black volume-control-button" style="height:32px;"><span>音量: </span><input type="range" id="vol_id_player_move" name="vol_id_player_move" min="0" max="100" value="${volume_setting_info['volume_player_move']}"></span>`);
$("#id_player_teleport").after(`<span class="w3-button w3-black volume-control-button" style="height:32px;"><span>音量: </span><input type="range" id="vol_id_player_teleport" name="vol_id_player_teleport" min="0" max="100" value="${volume_setting_info['volume_player_teleport']}"></span>`);
$("#id_player_turn_over").after(`<span class="w3-button w3-black volume-control-button" style="height:32px;"><span>音量: </span><input type="range" id="vol_id_player_turn_over" name="vol_id_player_turn_over" min="0" max="100" value="${volume_setting_info['volume_player_turn_over']}"></span>`);
$("#id_wrong_answer").after(`<span class="w3-button w3-black volume-control-button" style="height:32px;"><span>音量: </span><input type="range" id="vol_id_wrong_answer" name="vol_id_wrong_answer" min="0" max="100" value="${volume_setting_info['volume_wrong_answer']}"></span>`);
$("#id_user_define_1").after(`<span class="w3-button w3-black volume-control-button" style="height:32px;"><span>音量: </span><input type="range" id="vol_id_user_define_1" name="vol_id_user_define_1" min="0" max="100" value="${volume_setting_info['volume_user_define_1']}"></span>`);
$("#id_user_define_2").after(`<span class="w3-button w3-black volume-control-button" style="height:32px;"><span>音量: </span><input type="range" id="vol_id_user_define_2" name="vol_id_user_define_2" min="0" max="100" value="${volume_setting_info['volume_user_define_2']}"></span>`);
$("#id_user_define_3").after(`<span class="w3-button w3-black volume-control-button" style="height:32px;"><span>音量: </span><input type="range" id="vol_id_user_define_3" name="vol_id_user_define_3" min="0" max="100" value="${volume_setting_info['volume_user_define_3']}"></span>`);
$(".volume-control-button span").css({"position":"relative", "top":"-17px"});
$(".volume-control-button input").css({"position":"relative", "top":"-10px", "width": "100px"});


function isAudioLink(url) {
    if(typeof url !== 'string') return false;
    return(url.match(/^http[^\?]*.(mp3|ogg|wav)(\?(.*))?$/gmi) != null);
}

function isUserDataAudio(url) {
    if(typeof url !== 'string') return false;
    return(url.match(/.(mp3|ogg|wav)(\?(.*))?$/gmi) != null);
}

function isGoogleDriveAudio(url) {
	if(typeof url !== 'string') return false;
	return(url.match(/https:\/\/drive\.google\.com\//) != null);
}

function isGoogleDriveDownload(url) {
	if(typeof url !== 'string') return false;
	return(url.match(/https:\/\/docs\.google\.com\//) != null);
}

function stopAudio(button, myAudioElement) {
	button.html('<i class="fas fa-play"></i>聽聽看')
	myAudioElement.pause();
    myAudioElement.currentTime = 0;
}

let audioElements = {};
let defaultAudioUrlDict = {
	'id_background': 'bgm/background.mp3',
	'id_money_deduction': 'se/cash.mp3',
	'id_money_addition': 'se/coin.mp3',
	'id_dice': 'se/dice.mp3',
	'id_hover_button': 'se/hover.mp3',
	'id_build': 'se/build.mp3',
	'id_player_move': 'se/move.mp3',
	'id_player_teleport': 'se/teleport.mp3',
	'id_player_turn_over': 'se/turnover.mp3',
	'id_wrong_answer': 'se/wrong_answer.mp3'
}


$(".preview-button").on("mousedown", function() {
	if ($(this).text() === "聽聽看") {
		$(this).html('<i class="fas fa-stop"></i>停止播放')
		audioUrl = $(this).siblings().val();
		audioID =$(this).siblings().attr('id');
		console.log(audioUrl);
		console.log(audioID);
		let audio_vol_id = "#vol_" + audioID;
		console.log(audio_vol_id);
		let audio_vol = $(audio_vol_id).val() / 100;

		if (audioUrl === "預設") {
			defaultAudioUrl = "https://monopolyuserupload.blob.core.windows.net/userdata/music/default/" + defaultAudioUrlDict[audioID];
			myAudioElement = new Audio(defaultAudioUrl);
			myAudioElement.volume = audio_vol;
	        let preview_button = $(this);
        	myAudioElement.addEventListener('ended', function() {
			    stopAudio(preview_button, myAudioElement);
			}, false);
			myAudioElement.play();
			audioElements[audioID] = myAudioElement;
		} else if (isAudioLink(audioUrl)) {
        	myAudioElement = new Audio(audioUrl);
        	myAudioElement.volume = audio_vol;
        	let preview_button = $(this);
        	myAudioElement.addEventListener('ended', function() {
			    stopAudio(preview_button, myAudioElement);
			}, false);
			myAudioElement.play();
			audioElements[audioID] = myAudioElement;
        } else if (isUserDataAudio(audioUrl)) {
        	userdataAudioUrl = "https://monopolyuserupload.blob.core.windows.net/userdata/music/" + audioUrl;
        	myAudioElement = new Audio(userdataAudioUrl);
        	myAudioElement.volume = audio_vol;
	        let preview_button = $(this);
        	myAudioElement.addEventListener('ended', function() {
			    stopAudio(preview_button, myAudioElement);
			}, false);
			myAudioElement.play();
			audioElements[audioID] = myAudioElement;
        } else if (isGoogleDriveAudio(audioUrl)) {
        	let pattern = /\/d\/(.*)\/view\?/;
        	let googleID = audioUrl.match(pattern)[1];
        	let google_url = "https://docs.google.com/uc?export=download&id=" + googleID;
        	myAudioElement = new Audio(google_url);
        	myAudioElement.volume = audio_vol;
	        let preview_button = $(this);
        	myAudioElement.addEventListener('ended', function() {
			    stopAudio(preview_button, myAudioElement);
			}, false);
			myAudioElement.play();
			audioElements[audioID] = myAudioElement;
        } else if (isGoogleDriveDownload(audioUrl)) {
        	myAudioElement = new Audio(audioUrl);
        	myAudioElement.volume = audio_vol;
	        let preview_button = $(this);
        	myAudioElement.addEventListener('ended', function() {
			    stopAudio(preview_button, myAudioElement);
			}, false);
			myAudioElement.play();
			audioElements[audioID] = myAudioElement;
        } else {
        	  function notifyError() {
		          Swal.fire({
		            icon: 'error',
		            title: "音樂網址錯誤(只接受.mp3 or .ogg or .wav)",
		            showConfirmButton: false,
		            timer:  2000
	          	  })
		      }
		      notifyError();
        }
	} else {
		audioID =$(this).siblings().attr('id');
		stopAudio($(this), audioElements[audioID]);
	}
})

