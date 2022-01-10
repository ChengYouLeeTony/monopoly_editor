let enlargeWrap = document.body.appendChild(document.createElement("div"));
enlargeWrap.id = "enlarge-wrap";
let HTML = "";
for (var i = 0; i < 40; i++) {
  let img_src = "userdata/" + land_list[i][6];
  // console.log(img_src);
  if (i <= 19 && i >= 11) {
    HTML += "<img id='enlarge" + i + "' class='enlarge rotate270' " + 'src="https://monopolyuserupload.blob.core.windows.net/' + img_src + '">';
  } else if (i <= 30 && i >= 21){
    HTML += "<img id='enlarge" + i + "' class='enlarge rotate180' " + 'src="https://monopolyuserupload.blob.core.windows.net/' + img_src + '">';
  } else if (i <= 39 && i >= 31){
    HTML += "<img id='enlarge" + i + "' class='enlarge rotate90' " + 'src="https://monopolyuserupload.blob.core.windows.net/' + img_src + '">';
  } else {
    HTML += "<img id='enlarge" + i + "' class='enlarge' " + 'src="https://monopolyuserupload.blob.core.windows.net/' + img_src + '">';
  }
}
enlargeWrap.innerHTML = HTML;

let currentCell;
let currentCellAnchor;
let currentCellPositionHolder;
let currentCellName;
let currentCellValue;
let land_pos_list = [];
let description_list = [];
let land_type_list = [];
let value_list = [];
let color_list = [];
let is_use_upload_image_list = [];

for (var i = 0; i < 40; i++) {
  s = land_list[i];
  //store the initial value
  let land_pos = s[0];
  let description = s[1];
  let land_type = s[2];
  let value = s[3];
  let color = s[4];
  let is_use_upload_image = s[5];
  let additional_parameter = s[7];
  land_pos_list.push(land_pos);
  description_list.push(description);
  land_type_list.push(land_type);
  value_list.push(value);
  color_list.push(color);
  is_use_upload_image_list.push(is_use_upload_image);

  currentCell = document.getElementById("cell" + i);

  currentCellAnchor = currentCell.appendChild(document.createElement("div"));
  currentCellAnchor.id = "cell" + i + "anchor";
  currentCellAnchor.className = "cell-anchor";

  currentCellPositionHolder = currentCellAnchor.appendChild(document.createElement("div"));
  currentCellPositionHolder.id = "cell" + i + "positionholder";
  currentCellPositionHolder.className = "cell-position-holder";
  currentCellPositionHolder.enlargeId = "enlarge" + i;
  currentCellPositionHolder.posId = "pos" + i;

  currentCellName = currentCellAnchor.appendChild(document.createElement("div"));
  currentCellName.id = "cell" + i + "name";
  currentCellName.className = "cell-name";
  currentCellName.textContent = s[1];

  currentCellValue = currentCellAnchor.appendChild(document.createElement("div"));
  currentCellValue.id = "cell" + i + "value";
  currentCellValue.className = "cell-value";
  if (land_type == "可建造土地" || land_type == "基礎設施(不可蓋房子)") {
    currentCellValue.textContent = "$" + s[3];
  }

  let land_type_change_to = "";
  let selector_table_tr_description = ".land-form-pos" + land_pos + " tr:nth-child(2)";
  let selector_table_tr_value = ".land-form-pos" + land_pos + " tr:nth-child(3)";
  let selector_table_tr_color = ".land-form-pos" + land_pos + " tr:nth-child(4)";
  let selector_table_tr_is_use_upload_image = ".land-form-pos" + land_pos + " tr:nth-child(5)";
  let selector_table_tr_image = ".land-form-pos" + land_pos + " tr:nth-child(6)";
  let selector_table_tr_moddal_message = ".land-form-pos" + land_pos + " tr:nth-child(7)";
  let selector_table_tr_additional_parameter = ".land-form-pos" + land_pos + " tr:nth-child(8)";
  let selector_table_tr_value_label = selector_table_tr_value + " label";
  let selector_table_tr_color_label = selector_table_tr_color + " label";
  let selector_table_tr_additional_parameter_label = selector_table_tr_additional_parameter + " label";
  let selector_table_tr_image_help_text = selector_table_tr_image + " .helptext";
  let selector_table_tr_image_input = selector_table_tr_image + " input";
  let selector_id_is_use_upload_image = ".land-form-pos" + land_pos + " #id_is_use_upload_image";
  let selector_id_variable_1_change = ".land-form-pos" + land_pos + " #id_variable_1_change";
  let selector_id_variable_2_change = ".land-form-pos" + land_pos + " #id_variable_2_change";
  let selector_id_variable_3_change = ".land-form-pos" + land_pos + " #id_variable_3_change";
  let selector_id_variable_4_change = ".land-form-pos" + land_pos + " #id_variable_4_change";
  let selector_id_variable_5_change = ".land-form-pos" + land_pos + " #id_variable_5_change";
  //initial
  switch (land_type) {
    case "可建造土地":
      $(selector_table_tr_description).css("display", "table-row");
      $(selector_table_tr_value).css("display", "table-row");
      $(selector_table_tr_color).css("display", "table-row");
      $(selector_table_tr_is_use_upload_image).css("display", "table-row");
      $(selector_table_tr_image).css("display", "table-row");
      $(selector_table_tr_moddal_message).css("display", "none");
      $(selector_table_tr_additional_parameter).css("display", "none");
      $(selector_table_tr_value_label).html("土地價格:");            
      $(selector_table_tr_color_label).html("土地顏色:");
      $(selector_table_tr_image_help_text).html("設定自訂圖片後，將不再自動產生圖片");
      if ($(selector_id_is_use_upload_image).is(":checked") == true) {
        $(selector_table_tr_image_input).prop('disabled', false);
      }
      else {
        $(selector_table_tr_image_input).prop('disabled', true);
      }
      break
    case "基礎設施(不可蓋房子)":
      $(selector_table_tr_description).css("display", "table-row");
      $(selector_table_tr_value).css("display", "table-row");
      $(selector_table_tr_color).css("display", "table-row");
      $(selector_table_tr_is_use_upload_image).css("display", "table-row");
      $(selector_table_tr_image).css("display", "table-row");
      $(selector_table_tr_moddal_message).css("display", "none");
      $(selector_table_tr_additional_parameter).css("display", "table-row");
      $(selector_table_tr_value_label).html("土地價格:");
      $(selector_table_tr_color_label).html("圖示顏色:");
      $(selector_table_tr_additional_parameter_label).html("設施種類:");
      $(selector_table_tr_image_help_text).html("設定自訂圖片後，將不再自動產生圖片");
      if ($(selector_id_is_use_upload_image).is(":checked") == true) {
        $(selector_table_tr_image_input).prop('disabled', false);
      }
      else {
        $(selector_table_tr_image_input).prop('disabled', true);
      }
      break
    case "起點":
      $(selector_table_tr_description).css("display", "table-row");
      $(selector_table_tr_value).css("display", "none");
      $(selector_table_tr_color).css("display", "table-row");
      $(selector_table_tr_is_use_upload_image).css("display", "table-row");
      $(selector_table_tr_image).css("display", "table-row");
      $(selector_table_tr_moddal_message).css("display", "none");
      $(selector_table_tr_additional_parameter).css("display", "none");
      $(selector_table_tr_color_label).html("圖示顏色:");
      $(selector_table_tr_image_help_text).html("設定自訂圖片後，將不再自動產生圖片");
      if ($(selector_id_is_use_upload_image).is(":checked") == true) {
        $(selector_table_tr_image_input).prop('disabled', false);
      }
      else {
        $(selector_table_tr_image_input).prop('disabled', true);
      }
      break
    case "公園":
      $(selector_table_tr_description).css("display", "table-row");
      $(selector_table_tr_value).css("display", "none");
      $(selector_table_tr_color).css("display", "table-row");
      $(selector_table_tr_is_use_upload_image).css("display", "table-row");
      $(selector_table_tr_image).css("display", "table-row");
      $(selector_table_tr_moddal_message).css("display", "none");
      $(selector_table_tr_additional_parameter).css("display", "none");
      $(selector_table_tr_color_label).html("圖示顏色:");
      $(selector_table_tr_image_help_text).html("設定自訂圖片後，將不再自動產生圖片");
      if ($(selector_id_is_use_upload_image).is(":checked") == true) {
        $(selector_table_tr_image_input).prop('disabled', false);
      }
      else {
        $(selector_table_tr_image_input).prop('disabled', true);
      }
      break
    case "監獄":
      $(selector_table_tr_description).css("display", "table-row");
      $(selector_table_tr_value).css("display", "table-row");
      $(selector_table_tr_color).css("display", "table-row");
      $(selector_table_tr_is_use_upload_image).css("display", "table-row");
      $(selector_table_tr_image).css("display", "table-row");
      $(selector_table_tr_moddal_message).css("display", "none");
      $(selector_table_tr_additional_parameter).css("display", "none");
      $(selector_table_tr_value_label).html("跳過回合:");
      $(selector_table_tr_color_label).html("圖示顏色:");
      $(selector_table_tr_image_help_text).html("設定自訂圖片後，將不再自動產生圖片");
      if ($(selector_id_is_use_upload_image).is(":checked") == true) {
        $(selector_table_tr_image_input).prop('disabled', false);
      }
      else {
        $(selector_table_tr_image_input).prop('disabled', true);
      }
      break
    case "機會":
      $(selector_table_tr_description).css("display", "table-row");
      $(selector_table_tr_value).css("display", "table-row");
      $(selector_table_tr_color).css("display", "table-row");
      $(selector_table_tr_is_use_upload_image).css("display", "table-row");
      $(selector_table_tr_image).css("display", "table-row");
      $(selector_table_tr_moddal_message).css("display", "none");
      $(selector_table_tr_additional_parameter).css("display", "none");
      $(selector_table_tr_value_label).html("使用卡片集:");
      $(selector_table_tr_color_label).html("圖示顏色:");
      $(selector_table_tr_image_help_text).html("設定自訂圖片後，將不再自動產生圖片");
      if ($(selector_id_is_use_upload_image).is(":checked") == true) {
        $(selector_table_tr_image_input).prop('disabled', false);
      }
      else {
        $(selector_table_tr_image_input).prop('disabled', true);
      }
      $(selector_id_variable_1_change).parent().parent().css("display", "none");
      $(selector_id_variable_2_change).parent().parent().css("display", "none");
      $(selector_id_variable_3_change).parent().parent().css("display", "none");
      $(selector_id_variable_4_change).parent().parent().css("display", "none");
      $(selector_id_variable_5_change).parent().parent().css("display", "none");
      break
    case "自訂土地":
      //check using user uploaded image
      $(selector_id_is_use_upload_image).prop('checked', true);
      $(selector_table_tr_description).css("display", "table-row");
      $(selector_table_tr_value).css("display", "table-row");
      $(selector_table_tr_color).css("display", "none");
      $(selector_table_tr_is_use_upload_image).css("display", "none");
      $(selector_table_tr_image).css("display", "table-row");
      $(selector_table_tr_moddal_message).css("display", "table-row");
      $(selector_table_tr_additional_parameter).css("display", "none");
      $(selector_table_tr_value_label).html("減損金額:");
      $(selector_table_tr_image_help_text).html("請為自訂土地上傳一張圖片");
      $(selector_table_tr_image_input).prop('disabled', false);
      break
  }

  //change
  let selector_id_land_type = ".land-form-pos" + land_pos + " #id_land_type"
  $(selector_id_land_type).on('change', function() {
    switch (this.value) {
      case "1":
        land_type_change_to = "可建造土地";
        $(selector_table_tr_description).css("display", "table-row");
        $(selector_table_tr_value).css("display", "table-row");
        $(selector_table_tr_color).css("display", "table-row");
        $(selector_table_tr_is_use_upload_image).css("display", "table-row");
        $(selector_table_tr_image).css("display", "table-row");
        $(selector_table_tr_moddal_message).css("display", "none");
        $(selector_table_tr_additional_parameter).css("display", "none");
        $(selector_table_tr_value_label).html("土地價格:");            
        $(selector_table_tr_color_label).html("土地顏色:");
        $(selector_table_tr_image_help_text).html("設定自訂圖片後，將不再自動產生圖片");
        if ($(selector_id_is_use_upload_image).is(":checked") == true) {
          $(selector_table_tr_image_input).prop('disabled', false);
        }
        else {
          $(selector_table_tr_image_input).prop('disabled', true);
        }
        $(selector_id_variable_1_change).parent().parent().css("display", "table-row");
        $(selector_id_variable_2_change).parent().parent().css("display", "table-row");
        $(selector_id_variable_3_change).parent().parent().css("display", "table-row");
        $(selector_id_variable_4_change).parent().parent().css("display", "table-row");
        $(selector_id_variable_5_change).parent().parent().css("display", "table-row");
        break;
      case "2":
        land_type_change_to = "基礎設施(不可蓋房子)";
        $(selector_table_tr_description).css("display", "table-row");
        $(selector_table_tr_value).css("display", "table-row");
        $(selector_table_tr_color).css("display", "table-row");
        $(selector_table_tr_is_use_upload_image).css("display", "table-row");
        $(selector_table_tr_image).css("display", "table-row");
        $(selector_table_tr_moddal_message).css("display", "none");
        $(selector_table_tr_additional_parameter).css("display", "table-row");
        $(selector_table_tr_value_label).html("土地價格:");
        $(selector_table_tr_color_label).html("圖示顏色:");
        $(selector_table_tr_additional_parameter_label).html("設施種類:");
        $(selector_table_tr_image_help_text).html("設定自訂圖片後，將不再自動產生圖片");
        if ($(selector_id_is_use_upload_image).is(":checked") == true) {
          $(selector_table_tr_image_input).prop('disabled', false);
        }
        else {
          $(selector_table_tr_image_input).prop('disabled', true);
        }
        $(selector_id_variable_1_change).parent().parent().css("display", "table-row");
        $(selector_id_variable_2_change).parent().parent().css("display", "table-row");
        $(selector_id_variable_3_change).parent().parent().css("display", "table-row");
        $(selector_id_variable_4_change).parent().parent().css("display", "table-row");
        $(selector_id_variable_5_change).parent().parent().css("display", "table-row");
        break;
      case "3":
        land_type_change_to = "起點";
        $(selector_table_tr_description).css("display", "table-row");
        $(selector_table_tr_value).css("display", "none");
        $(selector_table_tr_color).css("display", "table-row");
        $(selector_table_tr_is_use_upload_image).css("display", "table-row");
        $(selector_table_tr_image).css("display", "table-row");
        $(selector_table_tr_moddal_message).css("display", "none");
        $(selector_table_tr_additional_parameter).css("display", "none");
        $(selector_table_tr_color_label).html("圖示顏色:");
        $(selector_table_tr_image_help_text).html("設定自訂圖片後，將不再自動產生圖片");
        if ($(selector_id_is_use_upload_image).is(":checked") == true) {
          $(selector_table_tr_image_input).prop('disabled', false);
        }
        else {
          $(selector_table_tr_image_input).prop('disabled', true);
        }
        $(selector_id_variable_1_change).parent().parent().css("display", "table-row");
        $(selector_id_variable_2_change).parent().parent().css("display", "table-row");
        $(selector_id_variable_3_change).parent().parent().css("display", "table-row");
        $(selector_id_variable_4_change).parent().parent().css("display", "table-row");
        $(selector_id_variable_5_change).parent().parent().css("display", "table-row");
        break;
      case "4":
        land_type_change_to = "公園";
        $(selector_table_tr_description).css("display", "table-row");
        $(selector_table_tr_value).css("display", "none");
        $(selector_table_tr_color).css("display", "table-row");
        $(selector_table_tr_is_use_upload_image).css("display", "table-row");
        $(selector_table_tr_image).css("display", "table-row");
        $(selector_table_tr_moddal_message).css("display", "none");
        $(selector_table_tr_additional_parameter).css("display", "none");
        $(selector_table_tr_color_label).html("圖示顏色:");
        $(selector_table_tr_image_help_text).html("設定自訂圖片後，將不再自動產生圖片");
        if ($(selector_id_is_use_upload_image).is(":checked") == true) {
          $(selector_table_tr_image_input).prop('disabled', false);
        }
        else {
          $(selector_table_tr_image_input).prop('disabled', true);
        }
        $(selector_id_variable_1_change).parent().parent().css("display", "table-row");
        $(selector_id_variable_2_change).parent().parent().css("display", "table-row");
        $(selector_id_variable_3_change).parent().parent().css("display", "table-row");
        $(selector_id_variable_4_change).parent().parent().css("display", "table-row");
        $(selector_id_variable_5_change).parent().parent().css("display", "table-row");
        break;
      case "5":
        land_type_change_to = "監獄";
        $(selector_table_tr_description).css("display", "table-row");
        $(selector_table_tr_value).css("display", "table-row");
        $(selector_table_tr_color).css("display", "table-row");
        $(selector_table_tr_is_use_upload_image).css("display", "table-row");
        $(selector_table_tr_image).css("display", "table-row");
        $(selector_table_tr_moddal_message).css("display", "none");
        $(selector_table_tr_additional_parameter).css("display", "none");
        $(selector_table_tr_value_label).html("跳過回合:");
        $(selector_table_tr_color_label).html("圖示顏色:");
        $(selector_table_tr_image_help_text).html("設定自訂圖片後，將不再自動產生圖片");
        if ($(selector_id_is_use_upload_image).is(":checked") == true) {
          $(selector_table_tr_image_input).prop('disabled', false);
        }
        else {
          $(selector_table_tr_image_input).prop('disabled', true);
        }
        $(selector_id_variable_1_change).parent().parent().css("display", "table-row");
        $(selector_id_variable_2_change).parent().parent().css("display", "table-row");
        $(selector_id_variable_3_change).parent().parent().css("display", "table-row");
        $(selector_id_variable_4_change).parent().parent().css("display", "table-row");
        $(selector_id_variable_5_change).parent().parent().css("display", "table-row");
        break;
      case "6":
        land_type_change_to = "機會";
        $(selector_table_tr_description).css("display", "table-row");
        $(selector_table_tr_value).css("display", "table-row");
        $(selector_table_tr_color).css("display", "table-row");
        $(selector_table_tr_is_use_upload_image).css("display", "table-row");
        $(selector_table_tr_image).css("display", "table-row");
        $(selector_table_tr_moddal_message).css("display", "none");
        $(selector_table_tr_additional_parameter).css("display", "none");
        $(selector_table_tr_value_label).html("使用卡片集:");
        $(selector_table_tr_color_label).html("圖示顏色:");
        $(selector_table_tr_image_help_text).html("設定自訂圖片後，將不再自動產生圖片");
        if ($(selector_id_is_use_upload_image).is(":checked") == true) {
          $(selector_table_tr_image_input).prop('disabled', false);
        }
        else {
          $(selector_table_tr_image_input).prop('disabled', true);
        }
        $(selector_id_variable_1_change).parent().parent().css("display", "none");
        $(selector_id_variable_2_change).parent().parent().css("display", "none");
        $(selector_id_variable_3_change).parent().parent().css("display", "none");
        $(selector_id_variable_4_change).parent().parent().css("display", "none");
        $(selector_id_variable_5_change).parent().parent().css("display", "none");
        break;
      case "7":
        land_type_change_to = "自訂土地";
        //check using user uploaded image
        $(selector_id_is_use_upload_image).prop('checked', true);
        $(selector_table_tr_description).css("display", "table-row");
        $(selector_table_tr_value).css("display", "table-row");
        $(selector_table_tr_color).css("display", "none");
        $(selector_table_tr_is_use_upload_image).css("display", "none");
        $(selector_table_tr_image).css("display", "table-row");
        $(selector_table_tr_moddal_message).css("display", "table-row");
        $(selector_table_tr_additional_parameter).css("display", "none");
        $(selector_table_tr_value_label).html("減損金額:");
        $(selector_table_tr_image_help_text).html("請為自訂土地上傳一張圖片");
        $(selector_table_tr_image_input).prop('disabled', false);
        $(selector_id_variable_1_change).parent().parent().css("display", "table-row");
        $(selector_id_variable_2_change).parent().parent().css("display", "table-row");
        $(selector_id_variable_3_change).parent().parent().css("display", "table-row");
        $(selector_id_variable_4_change).parent().parent().css("display", "table-row");
        $(selector_id_variable_5_change).parent().parent().css("display", "table-row");
        break;
    }
  });
  //change
  $(selector_id_is_use_upload_image).on('change', function() {
    if (this.checked == true) {
      $(selector_table_tr_image_input).prop('disabled', false);
    } 
    else {
      $(selector_table_tr_image_input).prop('disabled', true);
    }
  });
}

var drag, dragX, dragY, dragObj, dragTop, dragLeft;

$(".cell-position-holder, #jail").on("mouseover", function(){
  $("#" + this.enlargeId).show();

}).on("mouseout", function() {
  $("#" + this.enlargeId).hide();

}).on("mousemove", function(e) {
  var element = document.getElementById(this.enlargeId);

  if (e.clientY + 20 > window.innerHeight - 204) {
    element.style.top = (window.innerHeight - 204) + "px";
  } else {
    element.style.top = (e.clientY + 20) + "px";
  }

  element.style.left = (e.clientX + 10) + "px";
});

let land_change_list = [];
$(".cell-position-holder, #jail").on("mousedown", function(){
  document.getElementById(this.posId).style.display='block';
  let land_pos = this.posId.slice(3);
  let pos_id = parseInt(land_pos);
  let land_type = land_type_list[pos_id];
  let selector_table_tr_land_type = ".land-form-pos" + land_pos + " tr:nth-child(1)";
  let selector_table_tr_description = ".land-form-pos" + land_pos + " tr:nth-child(2)";
  let selector_table_tr_value = ".land-form-pos" + land_pos + " tr:nth-child(3)";
  let selector_table_tr_color = ".land-form-pos" + land_pos + " tr:nth-child(4)";
  let selector_table_tr_is_use_upload_image = ".land-form-pos" + land_pos + " tr:nth-child(5)";
  let selector_table_tr_image = ".land-form-pos" + land_pos + " tr:nth-child(6)";
  let selector_table_tr_moddal_message = ".land-form-pos" + land_pos + " tr:nth-child(7)";
  let selector_table_tr_additional_parameter = ".land-form-pos" + land_pos + " tr:nth-child(8)";
  let selector_table_tr_value_label = selector_table_tr_value + " label";
  let selector_table_tr_color_label = selector_table_tr_color + " label";
  let selector_table_tr_additional_parameter_label = selector_table_tr_additional_parameter + " label";
  let selector_table_tr_image_help_text = selector_table_tr_image + " .helptext";
  let selector_table_tr_image_input = selector_table_tr_image + " input";
  let selector_id_is_use_upload_image = ".land-form-pos" + land_pos + " #id_is_use_upload_image"
  let selector_table_tr_land_type_select = selector_table_tr_land_type + " select";
  let selector_table_tr_description_input = selector_table_tr_description + " input";
  let selector_table_tr_value_input = selector_table_tr_value + " input";
  let selector_table_tr_color_input = selector_table_tr_color + " input";
  let selector_table_tr_is_use_upload_image_input = selector_table_tr_is_use_upload_image + " input";
  let selector_id_variable_1_change = ".land-form-pos" + land_pos + " #id_variable_1_change";
  let selector_id_variable_2_change = ".land-form-pos" + land_pos + " #id_variable_2_change";
  let selector_id_variable_3_change = ".land-form-pos" + land_pos + " #id_variable_3_change";
  let selector_id_variable_4_change = ".land-form-pos" + land_pos + " #id_variable_4_change";
  let selector_id_variable_5_change = ".land-form-pos" + land_pos + " #id_variable_5_change";
  // let land_pos_list = [];
  // let description_list = [];
  // let land_type_list = [];
  // let value_list = [];
  // let color_list = [];
  // let is_use_upload_image_list = [];
  // let image_list = [];
  switch (land_type) {
    case "可建造土地":
      $(selector_table_tr_description).css("display", "table-row");
      $(selector_table_tr_value).css("display", "table-row");
      $(selector_table_tr_color).css("display", "table-row");
      $(selector_table_tr_is_use_upload_image).css("display", "table-row");
      $(selector_table_tr_image).css("display", "table-row");
      $(selector_table_tr_moddal_message).css("display", "none");
      $(selector_table_tr_additional_parameter).css("display", "none");
      $(selector_table_tr_value_label).html("土地價格:");            
      $(selector_table_tr_color_label).html("土地顏色:");
      $(selector_table_tr_image_help_text).html("設定自訂圖片後，將不再自動產生圖片");
      if ($(selector_id_is_use_upload_image).is(":checked") == true) {
        $(selector_table_tr_image_input).prop('disabled', false);
      }
      else {
        $(selector_table_tr_image_input).prop('disabled', true);
      }
      $(selector_table_tr_land_type_select).val("1");
      $(selector_id_variable_1_change).parent().parent().css("display", "table-row");
      $(selector_id_variable_2_change).parent().parent().css("display", "table-row");
      $(selector_id_variable_3_change).parent().parent().css("display", "table-row");
      $(selector_id_variable_4_change).parent().parent().css("display", "table-row");
      $(selector_id_variable_5_change).parent().parent().css("display", "table-row");
      break
    case "基礎設施(不可蓋房子)":
      $(selector_table_tr_description).css("display", "table-row");
      $(selector_table_tr_value).css("display", "table-row");
      $(selector_table_tr_color).css("display", "table-row");
      $(selector_table_tr_is_use_upload_image).css("display", "table-row");
      $(selector_table_tr_image).css("display", "table-row");
      $(selector_table_tr_moddal_message).css("display", "none");
      $(selector_table_tr_additional_parameter).css("display", "table-row");
      $(selector_table_tr_value_label).html("土地價格:");
      $(selector_table_tr_color_label).html("圖示顏色:");
      $(selector_table_tr_additional_parameter_label).html("設施種類:");
      $(selector_table_tr_image_help_text).html("設定自訂圖片後，將不再自動產生圖片");
      if ($(selector_id_is_use_upload_image).is(":checked") == true) {
        $(selector_table_tr_image_input).prop('disabled', false);
      }
      else {
        $(selector_table_tr_image_input).prop('disabled', true);
      }
      $(selector_table_tr_land_type_select).val("2");
      $(selector_id_variable_1_change).parent().parent().css("display", "table-row");
      $(selector_id_variable_2_change).parent().parent().css("display", "table-row");
      $(selector_id_variable_3_change).parent().parent().css("display", "table-row");
      $(selector_id_variable_4_change).parent().parent().css("display", "table-row");
      $(selector_id_variable_5_change).parent().parent().css("display", "table-row");
      break
    case "起點":
      $(selector_table_tr_description).css("display", "table-row");
      $(selector_table_tr_value).css("display", "none");
      $(selector_table_tr_color).css("display", "table-row");
      $(selector_table_tr_is_use_upload_image).css("display", "table-row");
      $(selector_table_tr_image).css("display", "table-row");
      $(selector_table_tr_moddal_message).css("display", "none");
      $(selector_table_tr_additional_parameter).css("display", "none");
      $(selector_table_tr_color_label).html("圖示顏色:");
      $(selector_table_tr_image_help_text).html("設定自訂圖片後，將不再自動產生圖片");
      if ($(selector_id_is_use_upload_image).is(":checked") == true) {
        $(selector_table_tr_image_input).prop('disabled', false);
      }
      else {
        $(selector_table_tr_image_input).prop('disabled', true);
      }
      $(selector_table_tr_land_type_select).val("3");
      $(selector_id_variable_1_change).parent().parent().css("display", "table-row");
      $(selector_id_variable_2_change).parent().parent().css("display", "table-row");
      $(selector_id_variable_3_change).parent().parent().css("display", "table-row");
      $(selector_id_variable_4_change).parent().parent().css("display", "table-row");
      $(selector_id_variable_5_change).parent().parent().css("display", "table-row");
      break
    case "公園":
      $(selector_table_tr_description).css("display", "table-row");
      $(selector_table_tr_value).css("display", "none");
      $(selector_table_tr_color).css("display", "table-row");
      $(selector_table_tr_is_use_upload_image).css("display", "table-row");
      $(selector_table_tr_image).css("display", "table-row");
      $(selector_table_tr_moddal_message).css("display", "none");
      $(selector_table_tr_additional_parameter).css("display", "none");
      $(selector_table_tr_color_label).html("圖示顏色:");
      $(selector_table_tr_image_help_text).html("設定自訂圖片後，將不再自動產生圖片");
      if ($(selector_id_is_use_upload_image).is(":checked") == true) {
        $(selector_table_tr_image_input).prop('disabled', false);
      }
      else {
        $(selector_table_tr_image_input).prop('disabled', true);
      }
      $(selector_table_tr_land_type_select).val("4");
      $(selector_id_variable_1_change).parent().parent().css("display", "table-row");
      $(selector_id_variable_2_change).parent().parent().css("display", "table-row");
      $(selector_id_variable_3_change).parent().parent().css("display", "table-row");
      $(selector_id_variable_4_change).parent().parent().css("display", "table-row");
      $(selector_id_variable_5_change).parent().parent().css("display", "table-row");
      break
    case "監獄":
      $(selector_table_tr_description).css("display", "table-row");
      $(selector_table_tr_value).css("display", "table-row");
      $(selector_table_tr_color).css("display", "table-row");
      $(selector_table_tr_is_use_upload_image).css("display", "table-row");
      $(selector_table_tr_image).css("display", "table-row");
      $(selector_table_tr_moddal_message).css("display", "none");
      $(selector_table_tr_additional_parameter).css("display", "none");
      $(selector_table_tr_value_label).html("跳過回合:");
      $(selector_table_tr_color_label).html("圖示顏色:");
      $(selector_table_tr_image_help_text).html("設定自訂圖片後，將不再自動產生圖片");
      if ($(selector_id_is_use_upload_image).is(":checked") == true) {
        $(selector_table_tr_image_input).prop('disabled', false);
      }
      else {
        $(selector_table_tr_image_input).prop('disabled', true);
      }
      $(selector_table_tr_land_type_select).val("5");
      $(selector_id_variable_1_change).parent().parent().css("display", "table-row");
      $(selector_id_variable_2_change).parent().parent().css("display", "table-row");
      $(selector_id_variable_3_change).parent().parent().css("display", "table-row");
      $(selector_id_variable_4_change).parent().parent().css("display", "table-row");
      $(selector_id_variable_5_change).parent().parent().css("display", "table-row");
      break
    case "機會":
      $(selector_table_tr_description).css("display", "table-row");
      $(selector_table_tr_value).css("display", "table-row");
      $(selector_table_tr_color).css("display", "table-row");
      $(selector_table_tr_is_use_upload_image).css("display", "table-row");
      $(selector_table_tr_image).css("display", "table-row");
      $(selector_table_tr_moddal_message).css("display", "none");
      $(selector_table_tr_additional_parameter).css("display", "none");
      $(selector_table_tr_value_label).html("使用卡片集:");
      $(selector_table_tr_color_label).html("圖示顏色:");
      $(selector_table_tr_image_help_text).html("設定自訂圖片後，將不再自動產生圖片");
      if ($(selector_id_is_use_upload_image).is(":checked") == true) {
        $(selector_table_tr_image_input).prop('disabled', false);
      }
      else {
        $(selector_table_tr_image_input).prop('disabled', true);
      }
      $(selector_table_tr_land_type_select).val("6");
      $(selector_id_variable_1_change).parent().parent().css("display", "none");
      $(selector_id_variable_2_change).parent().parent().css("display", "none");
      $(selector_id_variable_3_change).parent().parent().css("display", "none");
      $(selector_id_variable_4_change).parent().parent().css("display", "none");
      $(selector_id_variable_5_change).parent().parent().css("display", "none");
      break
    case "自訂土地":
      console.log(1);
      //check using user uploaded image
      $(selector_id_is_use_upload_image).prop('checked', true);
      $(selector_table_tr_description).css("display", "table-row");
      $(selector_table_tr_value).css("display", "table-row");
      $(selector_table_tr_color).css("display", "none");
      $(selector_table_tr_is_use_upload_image).css("display", "none");
      $(selector_table_tr_image).css("display", "table-row");
      $(selector_table_tr_moddal_message).css("display", "table-row");
      $(selector_table_tr_additional_parameter).css("display", "none");
      $(selector_table_tr_value_label).html("減損金額:");
      $(selector_table_tr_image_help_text).html("請為自訂土地上傳一張圖片");
      $(selector_table_tr_image_input).prop('disabled', false);
      $(selector_table_tr_land_type_select).val("7");
      $(selector_id_variable_1_change).parent().parent().css("display", "table-row");
      $(selector_id_variable_2_change).parent().parent().css("display", "table-row");
      $(selector_id_variable_3_change).parent().parent().css("display", "table-row");
      $(selector_id_variable_4_change).parent().parent().css("display", "table-row");
      $(selector_id_variable_5_change).parent().parent().css("display", "table-row");
      break
  }
  $(selector_table_tr_description_input).val(description_list[pos_id]);
  $(selector_table_tr_value_input).val(value_list[pos_id]);
  $(selector_table_tr_color_input).val(color_list[pos_id]);
  if (is_use_upload_image_list[pos_id] === true || land_type === "自訂土地") {
    $(selector_table_tr_is_use_upload_image_input).prop("checked",true);
  } else {
    $(selector_table_tr_is_use_upload_image_input).prop("checked",false);
  }
})

function copyMapID() {
  var copyText = document.getElementById("mapID");
  copyText.type = 'text';
  copyText.select();
  document.execCommand("Copy");
  copyText.type = 'hidden'
  Swal.fire({
    icon: 'success',
    title: '已複製地圖ID',
    showConfirmButton: false,
    timer: 1200
  })
}
