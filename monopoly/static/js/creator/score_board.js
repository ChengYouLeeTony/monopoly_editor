let $modalAvatar = document.getElementById("modal-user-avatar");
let $modalMessage = document.getElementById("modal-message-container");
let $modalTitle = document.getElementById("modal-title");
let $modalSubTitle = document.getElementById("modal-subtitle");
let previewButton = document.getElementById("preview");
let contentContainer = document.getElementById("content-container");

let title = document.getElementById("id_title");
let subtitle = document.getElementById("id_subtitle");
let avatar = document.getElementById("avatar");
let user_name = document.getElementById("user_name");
let background_img_url = document.getElementById("id_background_img_url");

$modalAvatar.src = `/static/images/favicon.png`;

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

//score board template
function scoreBoardTemplate(is_descending_order) {
	let scoreList;
	let avatarList;
	let playerNameList;
	let scoreboardTemplate = `<div id="scoreboard">`;
	if (is_descending_order === true) {
		scoreList = [{playerIndex: 0, score: 1500}, {playerIndex: 1, score: 1400}]
	} else {
		scoreList = [{playerIndex: 1, score: 1400}, {playerIndex: 0, score: 1500}]
	}
	avatarList = [`/userdata/${avatar.value}`, '/userdata/default_rival.png'];
	playerNameList = [user_name.value, 'Bob'];
	for (let index in scoreList) {
	    let rank = parseInt(index) + 1;
	    scoreboardTemplate += `
	        <div class="scoreboard-row">
	            <span class="scoreboard-ranking">${rank}</span>
	            <img class="chat-message-avatar" src="${avatarList[index]}">
	            <span class="scoreboard-username">${playerNameList[index]}</span>
	            <div class="monopoly-cash">M</div>
	            <span class="scoreboard-score">${scoreList[index].score}</span>
	        </div>`;
	}
	scoreboardTemplate += "</div>";
	return scoreboardTemplate
}

let audioManager = new AudioManager();
let outer_audio;
let is_outer_audio_playing = false;


function stopPreview() {
	previewButton.value = '預覽';
        document.getElementById('modal-card').style.display='none';
        if (is_outer_audio_playing !== true) {
                audioManager.stop(audioUrl);
        }
        else {
        	outer_audio.pause();
        	outer_audio.currentTime = 0;
        }
}

let audioUrl;
previewButton.addEventListener("click", 
function() { 
        if (previewButton.value === '預覽') {
        	$modalTitle.innerText = title.value;
                $modalSubTitle.innerText = subtitle.value;
                let is_descending_order = document.getElementById('id_is_descending_order').checked;
                scoreboardTemplate = scoreBoardTemplate(is_descending_order);
                $modalMessage.innerHTML = scoreboardTemplate;
                //change background_img_url
				if (background_img_url.value !== "") {
					contentContainer.style.background = `url("${background_img_url.value}") no-repeat`;
					contentContainer.style.backgroundSize = `cover`;
				} else {
					contentContainer.style.background = `url(/static/images/scoreboard_bg.png) no-repeat`;
					contentContainer.style.backgroundSize = `cover`;
				}
                previewButton.value = '取消預覽';
                document.getElementById('modal-card').style.display='block';
                let is_other_selected = $("#id_score_board_sound_effect_3").prop("checked");
                if (is_other_selected !== true) {
	                audioUrl = document.querySelector('input[name="score_board_sound_effect"]:checked').value;
	                audioManager.play(audioUrl);
	                is_outer_audio_playing = false;
	        }
	        else {
	        	audioUrl = $("#other_input").val();
	        	if (isAudioLink(audioUrl) || isGoogleDriveDownload(audioUrl)) {
		        	outer_audio = new Audio(audioUrl);
		        	outer_audio.play();
		        	is_outer_audio_playing = true;
		        } else if (isUserDataAudio(audioUrl)) {
		        	userdata_audioUrl = "https://monopolyuserupload.blob.core.windows.net/userdata/music/" + audioUrl;
			        outer_audio = new Audio(userdata_audioUrl);   
		        	outer_audio.play();
		        	is_outer_audio_playing = true;
		        } else if (isGoogleDriveAudio(audioUrl)) {
		        	let pattern = /\/d\/(.*)\/view\?/;
		        	let googleID = audioUrl.match(pattern)[1];
		        	let google_url = "https://docs.google.com/uc?export=download&id=" + googleID;
		        	outer_audio = new Audio(google_url);
		        	outer_audio.play();
		        	is_outer_audio_playing = true;
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
	        }
        } else if (previewButton.value === '取消預覽') {
               stopPreview();    
        }
});

//if user mouse down the form part, hide the preview modal
let card_form = document.getElementById("card-form");
card_form.addEventListener("mousedown", function() { 
	if (previewButton.value === '取消預覽') {
	       stopPreview();
        }      
});

//if user chooses another, show input part of another
let other_radio = document.getElementById("id_score_board_sound_effect_3");
if ($("#id_score_board_sound_effect_3").prop("checked") === true) {
	let input = document.createElement("input");
	input.type = "text";
	input.id = "other_input";
	input.name = "other_input";
	input.value = $("#other_audio_url").val();
	other_radio.parentNode.appendChild(input);
} else {
	$("#id_score_board_sound_effect_3").one("click", function() {
		let input = document.createElement("input");
		input.type = "text";
		input.id = "other_input";
		input.name = "other_input";
		input.placeholder = "請輸入音樂網址或從音樂庫中複製"
		other_radio.parentNode.appendChild(input);
	})
}