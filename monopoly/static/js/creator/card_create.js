let $modalAvatar = document.getElementById("modal-user-avatar");
let $modalMessage = document.getElementById("modal-message-container");
let $modalTitle = document.getElementById("modal-title");
let $modalSubTitle = document.getElementById("modal-subtitle");
let modalCard = document.getElementById("modal-card");
let background_img_url = document.getElementById("background_img_url");
let previewButton = document.getElementById("preview");

let title = document.getElementById("id_title");
let subtitle = document.getElementById("id_subtitle");
let description = document.getElementById("id_description");

let button_0 = document.getElementById("modal-button-0");
let button_1 = document.getElementById("modal-button-1");
let button_2 = document.getElementById("modal-button-2");
let button_3 = document.getElementById("modal-button-3");
let choice_1 = document.getElementById("id_multiple_choice_1");
let choice_2 = document.getElementById("id_multiple_choice_2");
let choice_3 = document.getElementById("id_multiple_choice_3");
let choice_4 = document.getElementById("id_multiple_choice_4");
let audioManager = new AudioManager();
let is_description_image_url = false;


$modalAvatar.src = `/static/images/player_0.png`;

function isImgLink(url) {
    if(typeof url !== 'string') return false;
    return(url.match(/^http[^\?]*.(jpg|jpeg|gif|png|tiff|bmp)(\?(.*))?$/gmi) != null);
}


previewButton.addEventListener("click", 
function() { 
        if (previewButton.value === '預覽') {
                $modalTitle.innerText = title.value;
                $modalSubTitle.innerText = subtitle.value;
                is_description_image_url = isImgLink(description.value);
                if (background_img_url.value !== "") {
                        modalCard.style.background = `url("${background_img_url.value}") no-repeat`;
                        modalCard.style.backgroundSize = `cover`;
                }
                if (is_description_image_url === false) {
                        $modalMessage.innerText = description.value;
                } else {
                        let image_element = '<img class="description-image" src="' + description.value + '">';
                        $modalMessage.innerHTML = image_element;
                }
                if (choice_1.value != "") {
                        button_0.style.display = "block";
                        button_0.innerText = choice_1.value; 
                } else {
                         button_0.style.display = "none";
                }
                if (choice_2.value != "") {
                        button_1.style.display = "block";
                        button_1.innerText = choice_2.value; 
                } else {
                         button_1.style.display = "none";
                }
                if (choice_3.value != "") {
                        button_2.style.display = "block";
                        button_2.innerText = choice_3.value; 
                } else {
                         button_2.style.display = "none";
                }
                if (choice_4.value != "") {
                        button_3.style.display = "block";
                        button_3.innerText = choice_4.value; 
                } else {
                         button_3.style.display = "none";
                }
                previewButton.value = '取消預覽';
                document.getElementById('modal-card').style.display='block';
        } else if (previewButton.value === '取消預覽') {
                 previewButton.value = '預覽';
                document.getElementById('modal-card').style.display='none';
        }
});

$(".large-button").on("mouseover", function(){
        audioManager.play("hover");
})

let card_form = document.getElementById("card-form");
card_form.addEventListener("mousedown", 
function() { 
        previewButton.value = '預覽';
        document.getElementById('modal-card').style.display='none';
        
});

let selector_table_tr_choice_1 = "#card-form" + " tr:nth-child(13)";
let selector_table_tr_choice_2 = "#card-form" + " tr:nth-child(14)";
let selector_table_tr_choice_3 = "#card-form" + " tr:nth-child(15)";
let selector_table_tr_choice_4 = "#card-form" + " tr:nth-child(16)";
let selector_table_tr_answer = "#card-form" + " tr:nth-child(17)";
let selector_table_tr_money_deduction_when_wrong_answer = "#card-form" + " tr:nth-child(18)";
//Hide at first
if ($('#id_is_multiple_choice').is(":checked") == true) {
} else {
        $(selector_table_tr_choice_1).hide();
        $(selector_table_tr_choice_2).hide();
        $(selector_table_tr_choice_3).hide();
        $(selector_table_tr_choice_4).hide();
        $(selector_table_tr_answer).hide();
        $(selector_table_tr_money_deduction_when_wrong_answer).hide();
        $('#modal-buttons-container').css("visibility", "hidden");
}

$('#id_is_multiple_choice').on('change', function() {
        $(selector_table_tr_choice_1).toggle();
        $(selector_table_tr_choice_2).toggle();
        $(selector_table_tr_choice_3).toggle();
        $(selector_table_tr_choice_4).toggle();
        $(selector_table_tr_answer).toggle();
        $(selector_table_tr_money_deduction_when_wrong_answer).toggle();
        if ($('#id_is_multiple_choice').is(":checked") == true) {
                $('#modal-buttons-container').css("visibility", "visible");
        } else {
                $('#modal-buttons-container').css("visibility", "hidden");
        }
})
