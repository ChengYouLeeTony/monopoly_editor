var x1 = document.getElementById('variable_1_name').value ? document.getElementById('variable_1_name').value + '(x1)' : 'x1';
var x2 = document.getElementById('variable_2_name').value ? document.getElementById('variable_2_name').value + '(x2)' : 'x2';
var x3 = document.getElementById('variable_3_name').value ? document.getElementById('variable_3_name').value + '(x3)' : 'x3';
var x4 = document.getElementById('variable_4_name').value ? document.getElementById('variable_4_name').value + '(x4)' : 'x4';
var x5 = document.getElementById('variable_5_name').value ? document.getElementById('variable_5_name').value + '(x5)' : 'x5';

Blockly.Blocks['variable_vs_variable'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldDropdown([["當前玩家金錢","money"], ["當前玩家跳過回合","stop_num"], ["當前玩家位置", "player_position"], [x1,"x1"], [x2,"x2"], [x3,"x3"], [x4,"x4"], [x5,"x5"]]), "choice_1")
        .appendField(new Blockly.FieldDropdown([["=","=="], ["≠","!="], ["<","<"], ["‏≤","‏<="], [">",">"], ["‏≥","‏>="]]), "compare")
        .appendField(new Blockly.FieldDropdown([["當前玩家金錢","money"], ["當前玩家跳過回合","stop_num"], ["當前玩家位置", "player_position"], [x1,"x1"], [x2,"x2"], [x3,"x3"], [x4,"x4"], [x5,"x5"]]), "choice_2");
    this.setInputsInline(true);
    this.setOutput(true, "Boolean");
    this.setColour(230);
 this.setTooltip("變數和變數進行比較");
 this.setHelpUrl("");
  }
};
Blockly.Blocks['variable_vs_number'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldDropdown([["當前玩家金錢","money"], ["當前玩家跳過回合","stop_num"], ["當前玩家位置", "player_position"], [x1,"x1"], [x2,"x2"], [x3,"x3"], [x4,"x4"], [x5,"x5"]]), "choice_1")
        .appendField(new Blockly.FieldDropdown([["=","=="], ["≠","!="], ["<","<"], ["‏≤","‏p<="], [">",">"], ["‏≥","‏p>="]]), "compare")
        .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.1), "number");
    this.setInputsInline(true);
    this.setOutput(true, "Boolean");
    this.setColour(230);
 this.setTooltip("變數和數值進行比較");
 this.setHelpUrl("");
  }
};
Blockly.Blocks['number_vs_variable'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldNumber(0, -Infinity, Infinity, 0.1), "number")
        .appendField(new Blockly.FieldDropdown([["=","=="], ["≠","!="], ["<","<"], ["‏≤","<="], [">",">"], ["‏≥",">="]]), "compare")
        .appendField(new Blockly.FieldDropdown([["當前玩家金錢","money"], ["當前玩家跳過回合","stop_num"], ["當前玩家位置", "player_position"], [x1,"x1"], [x2,"x2"], [x3,"x3"], [x4,"x4"], [x5,"x5"]]), "choice_1");
    this.setInputsInline(true);
    this.setOutput(true, "Boolean");
    this.setColour(230);
 this.setTooltip("數值和變數進行比較");
 this.setHelpUrl("");
  }
};
Blockly.Blocks['end_game_event'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("結束遊戲");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setColour(230);
 this.setTooltip("");
 this.setHelpUrl("");
  }
};
Blockly.Blocks['end_game_event_with_text'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("結束遊戲");
    this.appendDummyInput()
        .appendField("標題")
        .appendField(new Blockly.FieldTextInput(""), "title");
    this.appendDummyInput()
        .appendField("副標題")
        .appendField(new Blockly.FieldTextInput(""), "subtitle");
    this.appendDummyInput()
        .appendField("內容")
        .appendField(new Blockly.FieldTextInput(""), "message");
    this.setPreviousStatement(true, null);
    this.setColour(230);
 this.setTooltip("");
 this.setHelpUrl("");
  }
};
Blockly.Blocks['start_block'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("當骰完並結算事件後");
    this.setNextStatement(true, null);
    this.setColour(315);
 this.setTooltip("");
 this.setHelpUrl("");
  }
};
Blockly.Blocks['teleport_event'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("傳送至第")
        .appendField(new Blockly.FieldNumber(0, 0, 39), "position")
        .appendField("位置");
    this.appendDummyInput()
        .appendField("標題")
        .appendField(new Blockly.FieldTextInput(""), "title");
    this.appendDummyInput()
        .appendField("副標題")
        .appendField(new Blockly.FieldTextInput(""), "subtitle");
    this.appendDummyInput()
        .appendField("內容")
        .appendField(new Blockly.FieldTextInput(""), "message");
    this.setPreviousStatement(true, null);
    this.setColour(230);
 this.setTooltip("");
 this.setHelpUrl("");
  }
};
Blockly.Blocks['teleport_random_event'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("傳送至隨機位置");
    this.appendDummyInput()
        .appendField("標題")
        .appendField(new Blockly.FieldTextInput(""), "title");
    this.appendDummyInput()
        .appendField("副標題")
        .appendField(new Blockly.FieldTextInput(""), "subtitle");
    this.appendDummyInput()
        .appendField("內容")
        .appendField(new Blockly.FieldTextInput(""), "message");
    this.setPreviousStatement(true, null);
    this.setColour(230);
 this.setTooltip("");
 this.setHelpUrl("");
  }
};
Blockly.Blocks['move_forward_event'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("往前移動")
        .appendField(new Blockly.FieldNumber(1, 1, 39), "step")
        .appendField("格");
    this.appendDummyInput()
        .appendField("標題")
        .appendField(new Blockly.FieldTextInput(""), "title");
    this.appendDummyInput()
        .appendField("副標題")
        .appendField(new Blockly.FieldTextInput(""), "subtitle");
    this.appendDummyInput()
        .appendField("內容")
        .appendField(new Blockly.FieldTextInput(""), "message");
    this.setPreviousStatement(true, null);
    this.setColour(230);
 this.setTooltip("");
 this.setHelpUrl("");
  }
};
Blockly.Blocks['move_backward_event'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("往後移動")
        .appendField(new Blockly.FieldNumber(1, 1, 39), "step")
        .appendField("格");
    this.appendDummyInput()
        .appendField("標題")
        .appendField(new Blockly.FieldTextInput(""), "title");
    this.appendDummyInput()
        .appendField("副標題")
        .appendField(new Blockly.FieldTextInput(""), "subtitle");
    this.appendDummyInput()
        .appendField("內容")
        .appendField(new Blockly.FieldTextInput(""), "message");
    this.setPreviousStatement(true, null);
    this.setColour(230);
 this.setTooltip("");
 this.setHelpUrl("");
  }
};
Blockly.Blocks['turn_over_event'] = {
  init: function() {
    this.appendDummyInput()
        .setAlign(Blockly.ALIGN_CENTRE)
        .appendField("轉向");
    this.appendDummyInput()
        .appendField("標題")
        .appendField(new Blockly.FieldTextInput(""), "title");
    this.appendDummyInput()
        .appendField("副標題")
        .appendField(new Blockly.FieldTextInput(""), "subtitle");
    this.appendDummyInput()
        .appendField("內容")
        .appendField(new Blockly.FieldTextInput(""), "message");
    this.setPreviousStatement(true, null);
    this.setColour(230);
 this.setTooltip("");
 this.setHelpUrl("");
  }
}
Blockly.Blocks['move_to_event'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("移動到")
        .appendField(new Blockly.FieldNumber(0, 0, 39), "position")
        .appendField("位置");
    this.appendDummyInput()
        .appendField("標題")
        .appendField(new Blockly.FieldTextInput(""), "title");
    this.appendDummyInput()
        .appendField("副標題")
        .appendField(new Blockly.FieldTextInput(""), "subtitle");
    this.appendDummyInput()
        .appendField("內容")
        .appendField(new Blockly.FieldTextInput(""), "message");
    this.setInputsInline(false);
    this.setPreviousStatement(true, null);
    this.setColour(230);
 this.setTooltip("");
 this.setHelpUrl("");
  }
};
Blockly.Blocks['swap_event'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("隨機交換位置");
    this.appendDummyInput()
        .appendField("標題")
        .appendField(new Blockly.FieldTextInput(""), "title");
    this.appendDummyInput()
        .appendField("副標題")
        .appendField(new Blockly.FieldTextInput(""), "subtitle");
    this.appendDummyInput()
        .appendField("內容")
        .appendField(new Blockly.FieldTextInput(""), "message");
    this.setPreviousStatement(true, null);
    this.setColour(230);
 this.setTooltip("換當前玩家與另一名隨機玩家的位置");
 this.setHelpUrl("");
  }
};
Blockly.Blocks['swap_all_event'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("所有人隨機交換位置");
    this.appendDummyInput()
        .appendField("標題")
        .appendField(new Blockly.FieldTextInput(""), "title");
    this.appendDummyInput()
        .appendField("副標題")
        .appendField(new Blockly.FieldTextInput(""), "subtitle");
    this.appendDummyInput()
        .appendField("內容")
        .appendField(new Blockly.FieldTextInput(""), "message");
    this.setPreviousStatement(true, null);
    this.setColour(230);
 this.setTooltip("所有玩家隨機交換位置");
 this.setHelpUrl("");
  }
}
Blockly.Blocks['swap_except_self_event'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("其他人隨機交換位置");
    this.appendDummyInput()
        .appendField("標題")
        .appendField(new Blockly.FieldTextInput(""), "title");
    this.appendDummyInput()
        .appendField("副標題")
        .appendField(new Blockly.FieldTextInput(""), "subtitle");
    this.appendDummyInput()
        .appendField("內容")
        .appendField(new Blockly.FieldTextInput(""), "message");
    this.setPreviousStatement(true, null);
    this.setColour(230);
 this.setTooltip("隨機交換除了自己的其他玩家位置");
 this.setHelpUrl("");
  }
};
Blockly.Blocks['teleport_all_random_event'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("所有人隨機傳送位置");
    this.appendDummyInput()
        .appendField("標題")
        .appendField(new Blockly.FieldTextInput(""), "title");
    this.appendDummyInput()
        .appendField("副標題")
        .appendField(new Blockly.FieldTextInput(""), "subtitle");
    this.appendDummyInput()
        .appendField("內容")
        .appendField(new Blockly.FieldTextInput(""), "message");
    this.setPreviousStatement(true, null);
    this.setColour(230);
 this.setTooltip("傳送所有人到隨機位置");
 this.setHelpUrl("");
  }
};
Blockly.Blocks['teleport_except_self_random_event'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("其他人隨機傳送位置");
    this.appendDummyInput()
        .appendField("標題")
        .appendField(new Blockly.FieldTextInput(""), "title");
    this.appendDummyInput()
        .appendField("副標題")
        .appendField(new Blockly.FieldTextInput(""), "subtitle");
    this.appendDummyInput()
        .appendField("內容")
        .appendField(new Blockly.FieldTextInput(""), "message");
    this.setPreviousStatement(true, null);
    this.setColour(230);
 this.setTooltip("其他人隨機傳送位置");
 this.setHelpUrl("");
  }
};
Blockly.Blocks['user_define_variable'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldDropdown([["當前玩家金錢","money"], ["當前玩家跳過回合","stop_num"], ["當前玩家位置", "player_position"], [x1,"x1"], [x2,"x2"], [x3,"x3"], [x4,"x4"], [x5,"x5"]]), "variable");
    this.setOutput(true, "Number");
    this.setColour(230);
 this.setTooltip("");
 this.setHelpUrl("");
  }
};
Blockly.Blocks['set_user_define_variable'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("設");
    this.appendDummyInput()
        .appendField(new Blockly.FieldDropdown([["當前玩家金錢","money"], ["當前玩家跳過回合","stop_num"], [x1,"x1"], [x2,"x2"], [x3,"x3"], [x4,"x4"], [x5,"x5"]]), "variable");
    this.appendValueInput("value")
        .setCheck("Number")
        .appendField("為");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
 this.setTooltip("");
 this.setHelpUrl("");
  }
};
Blockly.Blocks['normal_event'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("標題")
        .appendField(new Blockly.FieldTextInput(""), "title");
    this.appendDummyInput()
        .appendField("副標題")
        .appendField(new Blockly.FieldTextInput(""), "subtitle");
    this.appendDummyInput()
        .appendField("內容")
        .appendField(new Blockly.FieldTextInput(""), "message");
    this.setPreviousStatement(true, null);
    this.setColour(230);
 this.setTooltip("用來單純地顯示文字");
 this.setHelpUrl("");
  }
};
Blockly.Blocks['play_sound_url'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("播放音效");
    this.appendDummyInput()
        .appendField(new Blockly.FieldTextInput("請輸入音效網址"), "sound_url");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
 this.setTooltip("音效網址結尾為.mp3 or .ogg or .wav");
 this.setHelpUrl("");
  }
};
Blockly.Blocks['change_background_sound_to'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("更換背景音樂為");
    this.appendDummyInput()
        .appendField(new Blockly.FieldTextInput("請輸入音樂網址"), "sound_url");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
 this.setTooltip("音樂網址結尾為.mp3 or .ogg or .wav");
 this.setHelpUrl("");
  }
};
Blockly.Blocks['play_sound_user_define'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("播放音效")
        .appendField(new Blockly.FieldDropdown([["自訂音效1","option_1"], ["自訂音效2","option_2"], ["自訂音效3","option_3"]]), "user_define_sound");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
 this.setTooltip("請先設定自訂音效");
 this.setHelpUrl("");
  }
};


Blockly.Python['variable_vs_variable'] = function(block) {
  var dropdown_choice_1 = block.getFieldValue('choice_1');
  var dropdown_compare = block.getFieldValue('compare');
  var dropdown_choice_2 = block.getFieldValue('choice_2');
  var code = [dropdown_choice_1, dropdown_compare, dropdown_choice_2].join(' ');
  return [code, Blockly.Python.ORDER_RELATIONAL];
};
Blockly.Python['variable_vs_number'] = function(block) {
  var dropdown_choice_1 = block.getFieldValue('choice_1');
  var dropdown_compare = block.getFieldValue('compare');
  if (dropdown_compare.length == 4) {
    dropdown_compare = dropdown_compare.slice(2,)
  }
  var number_number = block.getFieldValue('number');
  var code = [dropdown_choice_1, dropdown_compare, number_number].join(' ');
  return [code, Blockly.Python.ORDER_RELATIONAL];
};
Blockly.Python['number_vs_variable'] = function(block) {
  var number_number = block.getFieldValue('number');
  var dropdown_compare = block.getFieldValue('compare');
  var dropdown_choice_1 = block.getFieldValue('choice_1');
  var code = [number_number, dropdown_compare, dropdown_choice_1].join(' ');
  return [code, Blockly.Python.ORDER_RELATIONAL];
};
Blockly.Python['end_game_event'] = function(block) {
  var code = 'self.trigger_event_type = "rule_end_game"' + '\n';;
  return code;
};
Blockly.Python['end_game_event_with_text'] = function(block) {
  var text_title = block.getFieldValue('title');
  var text_subtitle = block.getFieldValue('subtitle');
  var text_message = block.getFieldValue('message');
  var code = 'self.trigger_event_type = "rule_end_game_with_text"\n' + 
             'self.trigger_event_title = "' + text_title + '"\n' +
             'self.trigger_event_subtitle = "' + text_subtitle + '"\n' +  
             'self.trigger_event_message = "' + text_message + '"' + '\n';
  return code;
};
Blockly.Python['start_block'] = function(block) {
  var code = "";
  return code;
};
Blockly.Python['teleport_event'] = function(block) {
  var number_position = block.getFieldValue('position');
  var text_title = block.getFieldValue('title');
  var text_subtitle = block.getFieldValue('subtitle');
  var text_message = block.getFieldValue('message');
  var code = 'self.trigger_event_type = "teleport"\n' + 
             'self.trigger_event_title = "' + text_title + '"\n' + 
             'self.trigger_event_message = "' + text_message + '"\n' + 
             'self.trigger_event_subtitle = "' + text_subtitle + '"\n' +
             'self.trigger_event_value = "' + number_position + '"'  + '\n';
  return code;
};
Blockly.Python['teleport_random_event'] = function(block) {
  var text_title = block.getFieldValue('title');
  var text_subtitle = block.getFieldValue('subtitle');
  var text_message = block.getFieldValue('message');
  var code = 'self.trigger_event_type = "teleport_random"\n' + 
             'self.trigger_event_title = "' + text_title + '"\n' + 
             'self.trigger_event_message = "' + text_message + '"\n' + 
             'self.trigger_event_subtitle = "' + text_subtitle + '"'  + '\n';
  return code;
};
Blockly.Python['move_forward_event'] = function(block) {
  var number_step = block.getFieldValue('step');
  var text_title = block.getFieldValue('title');
  var text_subtitle = block.getFieldValue('subtitle');
  var text_message = block.getFieldValue('message');
  var code = 'self.trigger_event_type = "move_forward"\n' + 
             'self.trigger_event_title = "' + text_title + '"\n' + 
             'self.trigger_event_message = "' + text_message + '"\n' + 
             'self.trigger_event_subtitle = "' + text_subtitle + '"\n' +
             'self.trigger_event_value = "' + number_step + '"' + '\n';
  return code;
};
Blockly.Python['move_backward_event'] = function(block) {
  var number_step = block.getFieldValue('step');
  var text_title = block.getFieldValue('title');
  var text_subtitle = block.getFieldValue('subtitle');
  var text_message = block.getFieldValue('message');
  var code = 'self.trigger_event_type = "move_backward"\n' + 
             'self.trigger_event_title = "' + text_title + '"\n' + 
             'self.trigger_event_message = "' + text_message + '"\n' + 
             'self.trigger_event_subtitle = "' + text_subtitle + '"\n' +
             'self.trigger_event_value = "' + number_step + '"'  + '\n';
  return code;
};
Blockly.Python['turn_over_event'] = function(block) {
  var text_title = block.getFieldValue('title');
  var text_subtitle = block.getFieldValue('subtitle');
  var text_message = block.getFieldValue('message');
  var code = 'self.trigger_event_type = "turn_over"\n' + 
             'self.trigger_event_title = "' + text_title + '"\n' + 
             'self.trigger_event_message = "' + text_message + '"\n' + 
             'self.trigger_event_subtitle = "' + text_subtitle + '"'  + '\n';
  return code;
};
Blockly.Python['move_to_event'] = function(block) {
  var number_position = block.getFieldValue('position');
  var text_title = block.getFieldValue('title');
  var text_subtitle = block.getFieldValue('subtitle');
  var text_message = block.getFieldValue('message');
  var code = 'self.trigger_event_type = "move_to"\n' + 
             'self.trigger_event_title = "' + text_title + '"\n' + 
             'self.trigger_event_message = "' + text_message + '"\n' + 
             'self.trigger_event_subtitle = "' + text_subtitle + '"\n' +
             'self.trigger_event_value = "' + number_position + '"'  + '\n';
  return code;
};
Blockly.Python['swap_event'] = function(block) {
  var text_title = block.getFieldValue('title');
  var text_subtitle = block.getFieldValue('subtitle');
  var text_message = block.getFieldValue('message');
  var code = 'self.trigger_event_type = "swap"\n' + 
             'self.trigger_event_title = "' + text_title + '"\n' + 
             'self.trigger_event_message = "' + text_message + '"\n' + 
             'self.trigger_event_subtitle = "' + text_subtitle + '"'  + '\n';
  return code;
};
Blockly.Python['swap_all_event'] = function(block) {
  var text_title = block.getFieldValue('title');
  var text_subtitle = block.getFieldValue('subtitle');
  var text_message = block.getFieldValue('message');
  var code = 'self.trigger_event_type = "swap_all"\n' + 
             'self.trigger_event_title = "' + text_title + '"\n' + 
             'self.trigger_event_message = "' + text_message + '"\n' + 
             'self.trigger_event_subtitle = "' + text_subtitle + '"'  + '\n';
  return code;
};
Blockly.Python['swap_except_self_event'] = function(block) {
  var text_title = block.getFieldValue('title');
  var text_subtitle = block.getFieldValue('subtitle');
  var text_message = block.getFieldValue('message');
  var code = 'self.trigger_event_type = "swap_except_self"\n' + 
             'self.trigger_event_title = "' + text_title + '"\n' + 
             'self.trigger_event_message = "' + text_message + '"\n' + 
             'self.trigger_event_subtitle = "' + text_subtitle + '"'  + '\n';
  return code;
};
Blockly.Python['teleport_all_random_event'] = function(block) {
  var text_title = block.getFieldValue('title');
  var text_subtitle = block.getFieldValue('subtitle');
  var text_message = block.getFieldValue('message');
  var code = 'self.trigger_event_type = "teleport_all_random"\n' + 
             'self.trigger_event_title = "' + text_title + '"\n' + 
             'self.trigger_event_message = "' + text_message + '"\n' + 
             'self.trigger_event_subtitle = "' + text_subtitle + '"'  + '\n';
  return code;
};
Blockly.Python['teleport_except_self_random_event'] = function(block) {
  var text_title = block.getFieldValue('title');
  var text_subtitle = block.getFieldValue('subtitle');
  var text_message = block.getFieldValue('message');
  var code = 'self.trigger_event_type = "teleport_except_self_random"\n' + 
             'self.trigger_event_title = "' + text_title + '"\n' + 
             'self.trigger_event_message = "' + text_message + '"\n' + 
             'self.trigger_event_subtitle = "' + text_subtitle + '"'  + '\n';
  return code;
};
Blockly.Python['user_define_variable'] = function(block) {
  var dropdown_variable = block.getFieldValue('variable');
  var code = dropdown_variable;
  return [code, Blockly.Python.ORDER_ATOMIC];
};
Blockly.Python['set_user_define_variable'] = function(block) {
  var dropdown_variable = block.getFieldValue('variable');
  var value_value = Blockly.Python.valueToCode(block, 'value', Blockly.Python.ORDER_ATOMIC);
  var code = dropdown_variable + ' = ' + value_value + '\n';
  if (dropdown_variable === 'money') {
    code += 'curr_player.set_money(money)\n' +
            'self.rolled_money_and_variables["money"] = money\n';
  } else if (dropdown_variable === "stop_num") {
    code += 'curr_player.set_stop(stop_num)\n';
  } else if (dropdown_variable === "x1") {
    code += 'curr_player.set_variable_1(x1)\n' +
            'self.rolled_money_and_variables["x1"] = x1\n';
  } else if (dropdown_variable === "x2") {
    code += 'curr_player.set_variable_2(x2)\n' +
            'self.rolled_money_and_variables["x2"] = x2\n';
  } else if (dropdown_variable === "x3") {
    code += 'curr_player.set_variable_3(x3)\n' +
            'self.rolled_money_and_variables["x3"] = x3\n';
  } else if (dropdown_variable === "x4") {
    code += 'curr_player.set_variable_4(x4)\n' +
            'self.rolled_money_and_variables["x4"] = x4\n';
  } else if (dropdown_variable === "x5") {
    code += 'curr_player.set_variable_5(x5)\n' +
            'self.rolled_money_and_variables["x5"] = x5\n';
  }
  return code;
};
Blockly.Python['normal_event'] = function(block) {
  var text_title = block.getFieldValue('title');
  var text_subtitle = block.getFieldValue('subtitle');
  var text_message = block.getFieldValue('message');
  var code = 'self.trigger_event_type = "normal"\n' + 
             'self.trigger_event_title = "' + text_title + '"\n' + 
             'self.trigger_event_message = "' + text_message + '"\n' + 
             'self.trigger_event_subtitle = "' + text_subtitle + '"'  + '\n';
  return code;
};
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
Blockly.Python['play_sound_url'] = function(block) {
  var text_sound_url = block.getFieldValue('sound_url');
  var code;
  if (isAudioLink(text_sound_url) == true || isGoogleDriveDownload(text_sound_url)) {
    code = 'self.sound_info["play_sound_url"] = "' + text_sound_url + '"\n';
  } else if (isUserDataAudio(text_sound_url) == true){
    code = 'self.sound_info["play_sound_url"] = "https://monopolyuserupload.blob.core.windows.net/userdata/music/' + text_sound_url + '"\n';
  } else if (isGoogleDriveAudio(text_sound_url) == true){
    let pattern = /\/d\/(.*)\/view\?/;
    let googleID = text_sound_url.match(pattern)[1];
    let google_url = "https://docs.google.com/uc?export=download&id=" + googleID;
    code = 'self.sound_info["play_sound_url"] = "' + google_url + '"\n';
  } else {
    code = '';
  }
  return code;
};
Blockly.Python['change_background_sound_to'] = function(block) {
  var text_sound_url = block.getFieldValue('sound_url');
  var code;
  if (isAudioLink(text_sound_url) == true || isGoogleDriveDownload(text_sound_url)) {
    code = 'self.sound_info["change_background_sound_to"] = "' + text_sound_url + '"\n';
  } else if (isUserDataAudio(text_sound_url) == true){
    code = 'self.sound_info["change_background_sound_to"] = "https://monopolyuserupload.blob.core.windows.net/userdata/music/' + text_sound_url + '"\n';
  } else if (isGoogleDriveAudio(text_sound_url) == true){
    let pattern = /\/d\/(.*)\/view\?/;
    let googleID = text_sound_url.match(pattern)[1];
    let google_url = "https://docs.google.com/uc?export=download&id=" + googleID;
    code = 'self.sound_info["change_background_sound_to"] = "' + google_url + '"\n';
  }else {
    code = '';
  }
  return code;
};
Blockly.Python['play_sound_user_define'] = function(block) {
  var dropdown_user_define_sound = block.getFieldValue('user_define_sound');
  var code = 'self.sound_info["play_sound_user_define"] = "' + dropdown_user_define_sound + '"\n';
  return code;
};




var workspace = Blockly.inject('blocklyDiv',
{
  toolbox: document.getElementById('toolbox'),
  maxInstances: {'start_block': 1}
});
//to avoid less than sybol encode in text area
var less_than_symbol_alternate = "@#%!less@#%!";
//init block from db
rolled_rule_blockly = rolled_rule_blockly.replace(/@#%!less@#%!/g, "&lt;");
xml = Blockly.Xml.textToDom(rolled_rule_blockly);
Blockly.Xml.domToWorkspace(xml, workspace);

var code;
function myUpdateFunction(event) {
  code = Blockly.Python.workspaceToCode(workspace);
  console.log(code);
}
workspace.addChangeListener(myUpdateFunction);
workspace.addChangeListener(Blockly.Events.disableOrphans);
var theme = Blockly.Theme.defineTheme('hats', {
  'base': Blockly.Themes.Classic,
  'startHats': true
});
workspace.setTheme(theme);



$("#update").on("mousedown", function(){
  BlocklyStorage.backupOnUnload();
  var rules = document.getElementById("rules");
  rules.innerHTML = code;
  var blockly_text_area = document.getElementById("blockly_text_area");
  var xml = Blockly.Xml.workspaceToDom(workspace);
  var text = Blockly.Xml.domToText(xml).replace(/&lt;/g, less_than_symbol_alternate);
  blockly_text_area.innerHTML = text;
})

$("#test").on("mousedown", function(){
  console.log("test");
  var blockly_text_area = document.getElementById("blockly_text_area");
  var xml = Blockly.Xml.workspaceToDom(workspace);
  var text = Blockly.Xml.domToText(xml).replace(/&lt;/g, less_than_symbol_alternate);
  blockly_text_area.innerHTML = text;
  console.log(text);
  // xml = Blockly.Xml.textToDom(text);
  // Blockly.Xml.domToWorkspace(xml, workspace);
})

$("#test2").on("mousedown", function(){
  rolled_rule_blockly = rolled_rule_blockly.replace("<br>", "&lt;br&gt;");
  xml = Blockly.Xml.textToDom(rolled_rule_blockly);
  Blockly.Xml.domToWorkspace(xml, workspace);
})