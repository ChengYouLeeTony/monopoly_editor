INIT_MAP_ROLLED_RULE = """
if money < 0:
  self.trigger_event_type = "rule_end_game"
if x1 == 1:
  x1 = 0
  curr_player.set_variable_1(x1)
  self.rolled_money_and_variables["x1"] = x1
  self.trigger_event_type = "teleport"
  self.trigger_event_title = "進牢"
  self.trigger_event_message = "要好好反省喔"
  self.trigger_event_subtitle = "真是不幸"
  self.trigger_event_value = "10"
if x2 == 1:
  x2 = 0
  curr_player.set_variable_2(x2)
  self.rolled_money_and_variables["x2"] = x2
  self.trigger_event_type = "move_to"
  self.trigger_event_title = ""
  self.trigger_event_message = "您前進到了民族路"
  self.trigger_event_subtitle = ""
  self.trigger_event_value = "11"
if x2 == 2:
  x2 = 0
  curr_player.set_variable_2(x2)
  self.rolled_money_and_variables["x2"] = x2
  self.trigger_event_type = "move_to"
  self.trigger_event_title = ""
  self.trigger_event_message = "您前進到了博愛路"
  self.trigger_event_subtitle = ""
  self.trigger_event_value = "24"
"""
INIT_MAP_ROLLED_RULE_BLOCKLY = '<xml xmlns="https://developers.google.com/blockly/xml"><block type="start_block" id="03a@MMxf9QjZV_?noz}U" x="70" y="37"><next><block type="controls_if" id=",@hO`QW+#-8*W/VET-yQ"><value name="IF0"><block type="variable_vs_number" id="#TwWZ5u[=L;BRrq7W~(r"><field name="choice_1">money</field><field name="compare">@#%!less@#%!</field><field name="number">0</field></block></value><statement name="DO0"><block type="end_game_event" id="^X!K,51$lpF4/QmfK+KZ"></block></statement><next><block type="controls_if" id="Nm]z%p$]!UG}aNkF8xh="><value name="IF0"><block type="variable_vs_number" id="=2G$wt_Hr~zmxwxjLYsl"><field name="choice_1">x1</field><field name="compare">==</field><field name="number">1</field></block></value><statement name="DO0"><block type="set_user_define_variable" id="MUKhhFu71vOYQddnkyLf"><field name="variable">x1</field><value name="value"><block type="math_number" id="[w8.5%eQCS:/TIv|3xH`"><field name="NUM">0</field></block></value><next><block type="teleport_event" id="L/]EMXqWE0L$jX$~[e0B"><field name="position">10</field><field name="title">進牢</field><field name="subtitle">真是不幸</field><field name="message">要好好反省喔</field></block></next></block></statement><next><block type="controls_if" id=",)5-kHgO]SRen?ruw_1~"><value name="IF0"><block type="variable_vs_number" id="7-04l9jsL%AeN*^5#+G)"><field name="choice_1">x2</field><field name="compare">==</field><field name="number">1</field></block></value><statement name="DO0"><block type="set_user_define_variable" id="]mLQ}Zg6^Tzx:D9rMD!|"><field name="variable">x2</field><value name="value"><block type="math_number" id="oTd.O-?q4BL]vqY!r7(J"><field name="NUM">0</field></block></value><next><block type="move_to_event" id="$=|{T,bd0ZF~C$rhbLxQ"><field name="position">11</field><field name="title"></field><field name="subtitle"></field><field name="message">您前進到了民族路</field></block></next></block></statement><next><block type="controls_if" id="XNZt-s-OzZ}(I}HYbR!c"><value name="IF0"><block type="variable_vs_number" id="KovEOCX#cF,c/p0P300u"><field name="choice_1">x2</field><field name="compare">==</field><field name="number">2</field></block></value><statement name="DO0"><block type="set_user_define_variable" id="(F`fksCpZE(3bwmlp_9:"><field name="variable">x2</field><value name="value"><block type="math_number" id="@!U*0@.;$lx0aq+NTr78"><field name="NUM">0</field></block></value><next><block type="move_to_event" id="g^C^$4DP*`tk1pqEcOx~"><field name="position">24</field><field name="title"></field><field name="subtitle"></field><field name="message">您前進到了博愛路</field></block></next></block></statement></block></next></block></next></block></next></block></next></block></xml>'
INIT_MAP = {
	0: ['起點', '起點', "map/default/0.png", "#ED1B24", 0],
	1: ['可建造土地', '建國南路', "map/default/1.png", "#FF0000", 600],
	2: ['機會', '命運', "map/default/2.png", "#FF8000", 0],
	3: ['可建造土地', '建國北路', "map/default/3.png", "#FF0000", 600],
	4: ['自訂土地', '所得稅', "map/default/4.png", "#955436", 2000, "所得稅;\n繳交所得稅2000元"],
	5: ['基礎設施(不可蓋房子)', '台北車站', "map/default/5.png", "#808A87", 2000, '火車站'],
	6: ['可建造土地', '忠孝路', "map/default/6.png", "#FFD700", 1000],
	7: ['機會', '機會', "map/default/7.png", "#FF0000", 1],
	8: ['可建造土地', '仁愛路', "map/default/8.png", "#FFD700", 1000],
	9: ['可建造土地', '信義路', "map/default/9.png", "#FFD700", 1200],
	10: ['自訂土地', '探監', "map/default/10.png", "#F7941D", 0, '探監;\n您路過了監獄\n探望了裡面的朋友'],
	11: ['可建造土地', '民族路', "map/default/11.png", "#228B22", 1400],
	12: ['基礎設施(不可蓋房子)', '電力公司', "map/default/12.png", "#E3A869", 1500, '公營設施'],
	13: ['可建造土地', '民權路', "map/default/13.png", "#228B22", 1400],
	14: ['可建造土地', '民生路', "map/default/14.png", "#228B22", 1600],
	15: ['基礎設施(不可蓋房子)', '台中車站', "map/default/15.png", "#808A87", 2000, '火車站'],
	16: ['可建造土地', '延平路一段', "map/default/16.png", "#191970", 1800],
	17: ['機會', '命運', "map/default/17.png", "#FF8000", 0],
	18: ['可建造土地', '延平路二段', "map/default/18.png", "#228B22", 1800],
	19: ['可建造土地', '延平路三段', "map/default/19.png", "#955436", 2200],
	20: ['公園', '大安森林公園', "map/default/20.png", "#ED1B24", 0],
	21: ['可建造土地', '自由路', "map/default/21.png", "#955436", 2200],
	22: ['機會', '機會', "map/default/22.png", "#FF0000", 1],
	23: ['可建造土地', '平等路', "map/default/23.png", "#955436", 2200],
	24: ['可建造土地', '博愛路', "map/default/24.png", "#955436", 2400],
	25: ['基礎設施(不可蓋房子)', '台南車站', "map/default/25.png", "#808A87", 2000, '火車站'],
	26: ['可建造土地', '健康路', "map/default/26.png", "#87CEEB", 2600],
	27: ['可建造土地', '五福路', "map/default/27.png", "#87CEEB", 2600],
	28: ['基礎設施(不可蓋房子)', '自來水廠', "map/default/28.png", "#E3A869", 1500, '公營設施'],
	29: ['可建造土地', '光明路', "map/default/29.png", "#87CEEB", 2800],
	30: ['監獄', '進監獄', "map/default/30.png", "#F7941D", 1, "1"],
	31: ['可建造土地', '中華路', "map/default/31.png", "#FF00FF", 3000],
	32: ['可建造土地', '中正路', "map/default/31.png", "#FF00FF", 3000],
	33: ['機會', '命運', "map/default/33.png", "#FF8000", 0],
	34: ['可建造土地', '介壽路', "map/default/34.png", "#FF00FF", 3200],
	35: ['基礎設施(不可蓋房子)', '高雄車站', "map/default/35.png", "#808A87", 2000, '火車站'],
	36: ['機會', '機會', "map/default/36.png", "#87CEEB", 1],
	37: ['可建造土地', '新生南路', "map/default/37.png", "#87CEEB", 3500],
	38: ['自訂土地', '財產稅', "map/default/38.png", "#87CEEB", 2000, '財產稅;\n繳交財產稅2000元'],
	39: ['可建造土地', '新生北路', "map/default/39.png", "#87CEEB", 4000],
}