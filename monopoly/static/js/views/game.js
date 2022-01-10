"use strict";


class GameView {
    constructor() {
        this.initComponents();
        this.audioManager = new AudioManager(music_setting_info);
        this.audioManager.play("background");

        this.gameInProcess = true;
    }

    initComponents() {
        this.userName = document.getElementById("username").value;
        this.hostName = document.getElementById("hostname").value;
        this.mapID = document.getElementById("map-id").value;
        this.mode = document.getElementById("mode").value;
        this.isViewerMode = this.mode.slice(0, 6) === "viewer";
        this.playerVariableName_1 = document.getElementById("player-variable-1-name").value;
        this.playerVariableName_2 = document.getElementById("player-variable-2-name").value;
        this.playerVariableName_3 = document.getElementById("player-variable-3-name").value;
        this.playerVariableName_4 = document.getElementById("player-variable-4-name").value;
        this.playerVariableName_5 = document.getElementById("player-variable-5-name").value;
        this.IsVariableVisible_1 = document.getElementById("is_variable_1_visible").value;
        this.IsVariableVisible_2 = document.getElementById("is_variable_2_visible").value;
        this.IsVariableVisible_3 = document.getElementById("is_variable_3_visible").value;
        this.IsVariableVisible_4 = document.getElementById("is_variable_4_visible").value;
        this.IsVariableVisible_5 = document.getElementById("is_variable_5_visible").value;

        this.$chatMessageContainer = document.getElementById("chat-messages");
        this.$chatMessageToSend = document.getElementById("chat-message-input");

        this.$audioControl = document.getElementById("audio-control");
        this.$audioControl.addEventListener("click", this.switchAudio.bind(this));

        this.$helpControl = document.getElementById("help-control");
        this.$helpControl.addEventListener("click", this.showHelp.bind(this));
        this.$helpOverlay = document.getElementById("rules-overlay");
        this.showingHelp = false;

        if (this.userName === this.hostName) {
            this.$exitControl = document.getElementById("exit-control");
            this.$exitControl.addEventListener("click", this.endGame.bind(this));
        }
        //creator and cheat
        if (this.mode === "creator") {
            this.$cheatControl_1 = document.getElementById("cheat-control-1");
            this.$cheatControl_2 = document.getElementById("cheat-control-2");
            this.$cheatControl_3 = document.getElementById("cheat-control-3");
            this.$cheatControl_4 = document.getElementById("cheat-control-4");
            this.$cheatControl_5 = document.getElementById("cheat-control-5");
            this.$cheatControl_6 = document.getElementById("cheat-control-6");
            this.$cheatControl_10 = document.getElementById("cheat-control-10");
            this.$cheatControl_20 = document.getElementById("cheat-control-20");
            this.$cheatControl_30 = document.getElementById("cheat-control-30");
            this.$cheatControl_1.addEventListener("click", this.roll_1.bind(this));
            this.$cheatControl_2.addEventListener("click", this.roll_2.bind(this));
            this.$cheatControl_3.addEventListener("click", this.roll_3.bind(this));
            this.$cheatControl_4.addEventListener("click", this.roll_4.bind(this));
            this.$cheatControl_5.addEventListener("click", this.roll_5.bind(this));
            this.$cheatControl_6.addEventListener("click", this.roll_6.bind(this));
            this.$cheatControl_10.addEventListener("click", this.roll_10.bind(this));
            this.$cheatControl_20.addEventListener("click", this.roll_20.bind(this));
            this.$cheatControl_30.addEventListener("click", this.roll_30.bind(this));
        }

        //for camera controls
        this.$cameraControlNegative90 = document.getElementById("rotate_negative_90");
        this.$cameraControlPositive90 = document.getElementById("rotate_positive_90");
        this.$cameraControlPhi = document.getElementById("rotate_phi");
        this.$cameraControlDollyNegative2 = document.getElementById("dolly_negative_2");
        this.$cameraControlDollyPositive2 = document.getElementById("dolly_positive_2");
        this.$cameraControlEnableMouse = document.getElementById("enable_mouse_or_not");
        this.$cameraControlResetCamera = document.getElementById("reset_camera");
      
        
        this.$cameraControlNegative90.addEventListener("click", this.rotate_negative_90.bind(this));
        this.$cameraControlPositive90.addEventListener("click", this.rotate_positive_90.bind(this));
        this.$cameraControlPhi.addEventListener("click", this.rotate_phi.bind(this));
        this.$cameraControlDollyNegative2.addEventListener("click", this.dolly_negative_2.bind(this));
        this.$cameraControlDollyPositive2.addEventListener("click", this.dolly_positive_2.bind(this));
        this.$cameraControlEnableMouse.addEventListener("click", this.enable_mouse.bind(this));
        this.$cameraControlResetCamera.addEventListener("click", this.reset_camera.bind(this));

        this.$chatMessageToSend.addEventListener("keydown", e => {
            const key = e.which || e.keyCode;
            // Detect Enter pressed
            if (key === 13) this.sendMessage();
        });

        this.diceMessage = document.getElementById("dice-message").innerHTML;

        this.$usersContainer = document.getElementById("users-container");

        this.$modalCard = document.getElementById("modal-card");
        this.$modalCardContent = document.querySelector("#modal-card .card-content-container");
        this.$modalAvatar = document.getElementById("modal-user-avatar");
        this.$modalMessage = document.getElementById("modal-message-container");
        this.$modalButtons = document.getElementById("modal-buttons-container");
        this.$modalTitle = document.getElementById("modal-title");
        this.$modalSubTitle = document.getElementById("modal-subtitle");
        let welcome_info = document.getElementById("welcome-info").value;

        this.showModal(null, welcome_info, "", "下載遊戲資源中...", []);
        this.initBoard();
    }

    initBoard() {
        this.gameController = new GameController({
            // The DOM element in which the drawing will happen.
            containerEl: document.getElementById("game-container"),

            // The base URL from where the BoardController will load its data.
            assetsUrl: "/static/3d_assets",

            //The User define URL
            userDataUrl: "/userdata/",

            onBoardPainted: this.initWebSocket.bind(this)
        });

        window.addEventListener("resize", () => {
            this.gameController.resizeBoard();
        }, false);
    }

    initWebSocket() {
        if (this.isViewerMode) {
            this.socket = new WebSocket((window.location.protocol === 'https:' ? 'wss' : 'ws') + `://${window.location.host}/game/${this.hostName}/${this.mode}`);
        }
        else {
            this.socket = new WebSocket((window.location.protocol === 'https:' ? 'wss' : 'ws') + `://${window.location.host}/game/${this.hostName}`);
        }

        this.socket.onmessage = (event) => {
            const message = JSON.parse(event.data);
            this.handleStatusChange(message);
        };
    }

    onDiceRolled(dice_num) {
        const notifyServer = () => {
            this.socket.send(JSON.stringify({
                action: "roll",
                dice_num: dice_num
            }));
        };
        setTimeout(notifyServer, 2000);
    }

    changeDiceNum(dice_num) {
        const notifyServer = () => {
            this.socket.send(JSON.stringify({
                action: "change_dice_num",
                dice_num: dice_num
            }));
        };
        setTimeout(notifyServer, 2000);
    }

    handleChangeDiceNum(message) {
        let dice_num = message.dice_num;
        let dice2 = document.getElementById("dice-2");
        let dice1 = document.getElementById("dice-1");
        if (dice_num === 1) {
            dice2.style.display = "none";
            dice1.style.left = "35%";
            $('#dice-num').val('1');
        }
        else {
            dice2.style.display = null;
            dice1.style.left = null;
            $('#dice-num').val('2');
        }
    }

    handleNotifyCheat(message) {
        let url = location.href;
        if (url.match(/\/creator/) === null) {
            let cheatArea = `<a id="cheat-control-1" class="cheat-control">
                <button>1</button>
            </a>
            <a id="cheat-control-2" class="cheat-control">
                <button>2</button>
            </a>
            <a id="cheat-control-3" class="cheat-control">
                <button>3</button>
            </a>
            <a id="cheat-control-4" class="cheat-control">
                <button>4</button>
            </a>
            <a id="cheat-control-5" class="cheat-control">
                <button>5</button>
            </a>
            <a id="cheat-control-6" class="cheat-control">
                <button>6</button>
            </a>
            <a id="cheat-control-10" class="cheat-control">
                <button>10</button>
            </a>
            <a id="cheat-control-20" class="cheat-control">
                <button>20</button>
            </a>
            <a id="cheat-control-30" class="cheat-control">
                <button>30</button>
            </a>`
            $("#hide-before-cheat-control").after(cheatArea);
            this.$cheatControl_1 = document.getElementById("cheat-control-1");
            this.$cheatControl_2 = document.getElementById("cheat-control-2");
            this.$cheatControl_3 = document.getElementById("cheat-control-3");
            this.$cheatControl_4 = document.getElementById("cheat-control-4");
            this.$cheatControl_5 = document.getElementById("cheat-control-5");
            this.$cheatControl_6 = document.getElementById("cheat-control-6");
            this.$cheatControl_10 = document.getElementById("cheat-control-10");
            this.$cheatControl_20 = document.getElementById("cheat-control-20");
            this.$cheatControl_30 = document.getElementById("cheat-control-30");
            this.$cheatControl_1.addEventListener("click", this.roll_1.bind(this));
            this.$cheatControl_2.addEventListener("click", this.roll_2.bind(this));
            this.$cheatControl_3.addEventListener("click", this.roll_3.bind(this));
            this.$cheatControl_4.addEventListener("click", this.roll_4.bind(this));
            this.$cheatControl_5.addEventListener("click", this.roll_5.bind(this));
            this.$cheatControl_6.addEventListener("click", this.roll_6.bind(this));
            this.$cheatControl_10.addEventListener("click", this.roll_10.bind(this));
            this.$cheatControl_20.addEventListener("click", this.roll_20.bind(this));
            this.$cheatControl_30.addEventListener("click", this.roll_30.bind(this));
        }
    }

    handleStatusChange(message) {
        const messageHandlers = {
            "init": this.handleInit,
            "add_err": this.handleAddErr,
            "roll_res": this.handleRollRes,
            "buy_land": this.handleBuyLand,
            "construct": this.handleConstruct,
            "confirm_user_define_decision": this.handleConfirmUserDefine,
            "cancel_decision": this.handleCancel,
            "cancel_decision_user_define": this.handleCancelUserDefine,
            "wrong_answer": this.handleWrongAnswer,
            "game_end": this.handleGameEnd,
            "chat": this.handleChat,
            "change_dice_num": this.handleChangeDiceNum,
            "notify_cheat": this.handleNotifyCheat
        };

        if (!this.gameInProcess) return;

        messageHandlers[message.action].bind(this)(message);
    }

    /*
    * Init game status, called after ws.connect
    * players: @see initPlayers
    * amount: @see changeCashAmount
    * */
    initGame(players, amount, posChange, initDirection, player_varible_1s, player_varible_2s, player_varible_3s, player_varible_4s, player_varible_5s) {
        // Init players
        this.initPlayers(players, posChange, initDirection);

        //Init player variable
        if (this.playerVariableName_1 != "") this.changeAllPlayerVariable(player_varible_1s, 1);
        if (this.playerVariableName_2 != "") this.changeAllPlayerVariable(player_varible_2s, 2);
        if (this.playerVariableName_3 != "") this.changeAllPlayerVariable(player_varible_3s, 3);
        if (this.playerVariableName_4 != "") this.changeAllPlayerVariable(player_varible_4s, 4);
        if (this.playerVariableName_5 != "") this.changeAllPlayerVariable(player_varible_5s, 5);

        // Init cash amount
        this.changeCashAmount(amount);
        //cheat detect
        if (this.mode === "creator") {
            this.notify_cheat();
        }
    }

    /*
    * Display players on the top
    * players: [{
    *   fullName: string, // user full name
    *   userName: string, // username
    *   avatar: string // user avatar url
    * }]
    * */
    initPlayers(players, initPos, initDirection) {
        this.players = players;
        this.currentPlayer = null;

        for (let i = 0; i < players.length; i++) {
            if (this.userName === players[i].userName) this.myPlayerIndex = i;
            const avatarTemplate = players[i].avatar ? `<img class="user-avatar" src="${players[i].avatar}">`
                : `<div class="user-group-name">${players[i].fullName.charAt(0)}</div>`;

            let userGroupContent = `
                    <span class="user-info">
                        <a href="/monopoly/profile/${players[i].userName}" target="_blank">
                            ${avatarTemplate}
                        </a>
                        <div class="monopoly-cash">M</div>
                        <div class="user-cash-num">1500</div>
                         <img class="user-role" src="/static/images/player_${i}.png">
                    </span>`;
            if (this.playerVariableName_1 != "") {
                userGroupContent += `
                    <span class="user-info user-variable user-variable-1" style="display:none;">
                        <div class="player-variable-name">${this.playerVariableName_1}:</div>
                        <div class="player-variable-value">0</div>
                    </span> `;
            }
            if (this.playerVariableName_2 != "") {
                userGroupContent += `
                    <span class="user-info user-variable user-variable-2" style="display:none;">
                        <div class="player-variable-name">${this.playerVariableName_2}:</div>
                        <div class="player-variable-value">0</div>
                    </span> `;
            }
            if (this.playerVariableName_3 != "") {
                userGroupContent += `
                    <span class="user-info user-variable user-variable-3" style="display:none;">
                        <div class="player-variable-name">${this.playerVariableName_3}:</div>
                        <div class="player-variable-value">0</div>
                    </span> `;
            }
            if (this.playerVariableName_4 != "") {
                userGroupContent += `
                    <span class="user-info user-variable user-variable-4" style="display:none;">
                        <div class="player-variable-name">${this.playerVariableName_4}:</div>
                        <div class="player-variable-value">0</div>
                    </span> `;
            }
            if (this.playerVariableName_5 != "") {
                userGroupContent += `
                    <span class="user-info user-variable user-variable-5" style="display:none;">
                        <div class="player-variable-name">${this.playerVariableName_5}:</div>
                        <div class="player-variable-value">0</div>
                    </span> `;
            }
            this.$usersContainer.innerHTML += `
                <div id="user-group-${i}" class="user-group" style="background: ${GameView.PLAYERS_COLORS[i]}">
                    ${userGroupContent}
                 </div>` 
        }

        let IsVariableVisible_1 = this.IsVariableVisible_1;
        let IsVariableVisible_2 = this.IsVariableVisible_2;
        let IsVariableVisible_3 = this.IsVariableVisible_3;
        let IsVariableVisible_4 = this.IsVariableVisible_4;
        let IsVariableVisible_5 = this.IsVariableVisible_5;
        $(".user-group").on("mouseover", function(){
           $(".user-variable").css('display', 'flex');
           if (IsVariableVisible_1 === "False") {
             $('.user-variable-1').css('display', 'none');
           }
           if (IsVariableVisible_2 === "False") {
             $('.user-variable-2').css('display', 'none');
           }
           if (IsVariableVisible_3 === "False") {
             $('.user-variable-3').css('display', 'none');
           }
           if (IsVariableVisible_4 === "False") {
             $('.user-variable-4').css('display', 'none');
           }
           if (IsVariableVisible_5 === "False") {
             $('.user-variable-5').css('display', 'none');
           }

        }).on("mouseout", function() {
           $(".user-variable").css('display', 'none');
        });

        this.gameLoadingPromise = this.gameController.addPlayer(players.length, initPos, initDirection);
    }

    /*
    * Change the cash balance
    * amounts: [int]
    * */
    changeCashAmount(amounts) {
        for (let i in amounts) {
            const $cashAmount = document.querySelector(`#user-group-${i} .user-cash-num`);
            $cashAmount.innerText = amounts[i];
        }
    }

    changeOneCashAmount(curr_player, cash) {
        const $cashAmount = document.querySelector(`#user-group-${curr_player} .user-cash-num`);
        $cashAmount.innerText = cash;
    }

    changeAllPlayerVariable(playerVaribles, variablePos) {
        for (let i in playerVaribles) {
            const $playerVariableValue = document.querySelector(`#user-group-${i} .user-variable-${variablePos} .player-variable-value`);
            $playerVariableValue.innerText = playerVaribles[i];
        }
    }

    changeOnePlayerVariable(curr_player, playerVarible, variablePos) {
        const $playerVariableValue = document.querySelector(`#user-group-${curr_player} .user-variable-${variablePos} .player-variable-value`);
        $playerVariableValue.innerText = playerVarible;
    }

    /*
    * Change player
    * nextPlayer: int,
    * nextPlayerPos: int,
    * nextPlayerIsTurnOver: "true" or "false"
    * onDiceRolled: function
    * */
    changePlayer(nextPlayer, nextPlayerPos, nextPlayerIsTurnOver, onDiceRolled) {
        // update user indicator
        if (this.currentPlayer !== null) {
            let $currentUserGroup = document.getElementById(`user-group-${this.currentPlayer}`);
            $currentUserGroup.classList.remove("active");
        }

        let $nextUserGroup = document.getElementById(`user-group-${nextPlayer}`);
        $nextUserGroup.classList.add("active");

        this.currentPlayer = nextPlayer;
        let title = (this.currentPlayer === this.myPlayerIndex) ? "輪到你了!" : "";

        //change camera position
        console.log(nextPlayerPos);
        console.log(nextPlayerIsTurnOver);
        this.nextPlayerPos = nextPlayerPos;
        this.nextPlayerIsTurnOver = nextPlayerIsTurnOver;
        this.gameController.changeCameraPosition(nextPlayerPos, nextPlayerIsTurnOver);

        // role dice
        $('#dice-num').val('2');
        const button = (nextPlayer !== this.myPlayerIndex) ? [] :
            [{
                text: "骰岀",
                callback: () => {
                    document.getElementById("roll").checked = true;
                    document.querySelector("#modal-buttons-container button").disabled = true;
                    document.querySelector("#modal-buttons-container button").innerText = "請等待...";
                    document.getElementById("modal-button-1").style.display = "none";

                    this.audioManager.play("dice");
                    let dice_num = $('#dice-num').val();
                    console.log(dice_num);
                    onDiceRolled(dice_num);
                }
            }, {
                text: "切換為一骰",
                callback: () => {
                    let dice_num_control = document.getElementById("modal-button-1");
                    let dice2 = document.getElementById("dice-2");
                    let dice1 = document.getElementById("dice-1");
                    if (dice_num_control.innerText === "切換為一骰") {
                        dice2.style.display = "none";
                        dice1.style.left = "35%";
                        dice_num_control.innerText = "切換為兩骰";
                        $('#dice-num').val('1');
                        //notify server to change dice num
                        this.changeDiceNum(1);
                    }
                    else {
                        dice2.style.display = null;
                        dice1.style.left = null;
                        dice_num_control.innerText = "切換為一骰";
                        $('#dice-num').val('2');
                        //notify server to change dice num
                        this.changeDiceNum(2);
                    }
                }
            }];
        this.showModal(nextPlayer, title, "", this.diceMessage, button);
    }

    /*
    * Display a pop-up modal
    * message: a snippet of text or HTML
    * playerIndex: int,
    * buttons: [{
    *   text: string, // "button text"
    *   callback: function
    * }],
    * displayTime: int // seconds to display
    * */
    showModal(playerIndex, title, subTitle, message, buttons, displayTime, background_img_url) {
        return new Promise(resolve => {
            if (playerIndex === null) {
                this.$modalAvatar.src = GameView.DEFAULT_AVATAR;
            } else {
                this.$modalAvatar.src = `/static/images/player_${playerIndex}.png`;
                this.$modalAvatar.style.background = GameView.PLAYERS_COLORS[playerIndex];
            }

            if (playerIndex === this.myPlayerIndex) {
                this.$modalAvatar.classList.add("active");
            } else {
                this.$modalAvatar.classList.remove("active");
            }

            let is_description_image_url = this.isImgLink(message.trim());
            if (is_description_image_url === false) {
                    this.$modalMessage.innerHTML = message;
            } else {
                    let image_element = '<img class="description-image" src="' + message.trim() + '">';
                    this.$modalMessage.innerHTML = image_element;
            }
            // this.$modalMessage.innerHTML = message;
            this.$modalButtons.innerHTML = "";

            this.$modalTitle.innerText = title;
            this.$modalSubTitle.innerText = subTitle;
            console.log(playerIndex);
            console.log(this.myPlayerIndex);

            if (playerIndex === this.myPlayerIndex || playerIndex === null) {
                for (let i in buttons) {
                    let button = document.createElement("button");
                    button.classList.add("large-button");
                    button.id = `modal-button-${i}`;
                    button.innerText = buttons[i].text;

                    button.addEventListener("click", () => {
                        buttons[i].callback();
                        resolve();
                    });

                    button.addEventListener("mouseover", () => {
                        this.audioManager.play("hover_button");
                    });

                    this.$modalButtons.appendChild(button);
                }
            } else {
                for (let i in buttons) {
                    let button = document.createElement("button");
                    button.classList.add("large-button");
                    button.disabled = true;
                    button.id = `modal-button-${i}`;
                    button.innerText = buttons[i].text;
                    let isAnswer = buttons[i].isAnswer;
                    if (isAnswer === true) {
                        button.style = "background-color:green";
                    }

                    this.$modalButtons.appendChild(button);
                }
            }

     

            this.$modalCard.classList.remove("hidden");
            this.$modalCard.classList.remove("modal-hidden");

            let basic_setting_modal_background_img_url = document.getElementById("modal-background-img-url").value;

            if (background_img_url !== undefined && background_img_url !== "") {
                $('#modal-card').css('background', `url("${background_img_url}") no-repeat`);
                $('#modal-card').css('background-size', `cover`);
            } else if (basic_setting_modal_background_img_url !== "") {
                $('#modal-card').css('background', `url("${basic_setting_modal_background_img_url}") no-repeat`);
                $('#modal-card').css('background-size', `cover`);
            } else {
                $('#modal-card').css('background', '');
            }

            // hide modal after a period of time if displayTime is set
            if (displayTime !== undefined && displayTime > 0) {
                setTimeout(async () => {
                    await this.hideModal(true);
                    resolve();
                }, displayTime * 1000);
            } else {
                resolve();
            }
        });
    }

    /*
    * Hide the modal
    * */
    hideModal(delayAfter) {
        return new Promise((resolve => {
            this.$modalCard.classList.add("modal-hidden");
            if (delayAfter === true) {
                setTimeout(() => {
                    resolve();
                }, 500);
            } else {
                resolve();
            }
        }))
    }

    async dealRolledEvent(message,  bankrupt_end, onDiceRolled) {
        let currPlayer = message.curr_player;
        let nextPlayer = message.next_player;
        let newPos = message.new_pos;
        let nextPlayerPos = message.next_player_info["pos"];
        let nextPlayerIsTurnOver = message.next_player_info["is_turn_over"];
        //event info
        let is_trigger_move_pass_start = message.event_info["is_trigger_move_pass_start"];
        let is_turn_over = message.event_info["is_turn_over"];
        let swap_event_info = message.event_info["swap_event_info"];
        let swap_all_event_info = message.event_info["swap_all_event_info"];
        let swap_except_self_event_info = message.event_info["swap_except_self_event_info"];
        let teleport_all_random_event_info = message.event_info["teleport_all_random_event_info"];
        let teleport_except_self_random_event_info = message.event_info["teleport_except_self_random_event_info"];
        let rolled_money_and_variables = message.rolled_money_and_variables;
        console.log(rolled_money_and_variables);

        let trigger_event_title = message.trigger_event_title;
        let trigger_event_subtitle = message.trigger_event_subtitle;
        let trigger_event_message = message.trigger_event_message;
        let trigger_event_value = parseInt(message.trigger_event_value);
        // play sound from sound_info
        let sound_info = message.sound_info;
        console.log(sound_info);
        if (Object.keys(sound_info).length !== 0) {
            if (sound_info['play_sound_url'] != null) {
                this.audioManager.play_url(sound_info['play_sound_url']);
            }
            if (sound_info['play_sound_user_define'] != null) {
                switch(sound_info['play_sound_user_define']) {
                    case 'option_1':
                        this.audioManager.play("user_define_1");
                        break;
                    case 'option_2':
                        this.audioManager.play("user_define_2");
                        break;
                    case 'option_3':
                        this.audioManager.play("user_define_3");
                        break;
                    default:
                }
            }
            if (sound_info['change_background_sound_to'] != null) {
                this.audioManager.change_background_sound_to(sound_info['change_background_sound_to']);
            }
        }
        //event
        let game_is_already_ended = false;
        if (bankrupt_end === true) {
            game_is_already_ended = true;
            this.endGame();
        } else if (message.trigger_event_type === "rule_end_game_with_text") {
            await this.showModal(currPlayer, trigger_event_title, trigger_event_subtitle, trigger_event_message, [], 2);
            game_is_already_ended = true;
            this.endGame();
        } else if (message.trigger_event_type === "rule_end_game") {
            game_is_already_ended = true;
            this.endGame();
        } else if (message.trigger_event_type === "teleport") {
            await this.showModal(currPlayer, trigger_event_title, trigger_event_subtitle, trigger_event_message, [], 2);
            await this.gameController.teleportPlayer(currPlayer, trigger_event_value, is_turn_over);
            this.audioManager.play("player_teleport");
        } else if (message.trigger_event_type === "teleport_random") {
            await this.showModal(currPlayer, trigger_event_title, trigger_event_subtitle, trigger_event_message, [], 2);
            await this.gameController.teleportPlayer(currPlayer, trigger_event_value, is_turn_over);
            this.audioManager.play("player_teleport");
        } else if (message.trigger_event_type === "move_forward" || message.trigger_event_type === "move_to") {
            let move_distance;
            this.audioManager.play("player_move");
            if (is_turn_over == "false") {
                move_distance = (trigger_event_value - newPos) > 0 ? (trigger_event_value - newPos) : 40 + (trigger_event_value - newPos);
                await this.gameController.movePlayer(currPlayer, trigger_event_value);
            }  else if (is_turn_over == "true") {
                move_distance = (newPos - trigger_event_value) > 0 ? (newPos - trigger_event_value) : 40 + (newPos - trigger_event_value);
                await this.gameController.movePlayerCounterclockwise(currPlayer, trigger_event_value);
            }
            let modal_exist_time = Math.max(move_distance / 5, 1.5);        
            await this.showModal(currPlayer, trigger_event_title, trigger_event_subtitle, trigger_event_message, [], modal_exist_time);
            
            if (is_trigger_move_pass_start === "true") {
                let eventMsg = this.players[currPlayer].userName + " 經過了起點<br><div>獲得了"+ message.START_REWARD + "元!";
                let cash = message.curr_cash;
                for (let i = 0; i < cash.length; i++) {
                    cash[i] += message.START_REWARD
                }
                this.changeCashAmount(cash);
                await this.showModal(currPlayer, "獲得獎勵", "起點", eventMsg, [], 2);
                this.audioManager.play("money_addition");

            }
        } else if (message.trigger_event_type === "move_backward") {
            let move_distance;
            this.audioManager.play("player_move");
            if (is_turn_over == "false") {
                move_distance = (newPos - trigger_event_value) > 0 ? (newPos - trigger_event_value) : 40 + (newPos - trigger_event_value);
                await this.gameController.movePlayerBack(currPlayer, trigger_event_value);
            }  else if (is_turn_over == "true") {
                move_distance = (trigger_event_value - newPos) > 0 ? (trigger_event_value - newPos) : 40 + (trigger_event_value - newPos);
                await this.gameController.movePlayerBackClockwise(currPlayer, trigger_event_value);
            }
            let modal_exist_time = Math.max(move_distance / 5, 1.5);              
            await this.showModal(currPlayer, trigger_event_title, trigger_event_subtitle, trigger_event_message, [], modal_exist_time);
            
        } else if (message.trigger_event_type === "turn_over") {
            let modal_exist_time =Math.min(4,Math.max(trigger_event_message.length / 10, 2));    
            await this.showModal(currPlayer, trigger_event_title, trigger_event_subtitle, trigger_event_message, [], modal_exist_time);
            this.audioManager.play("player_turn_over");
            await this.gameController.turnOverPlayer(currPlayer, is_turn_over);
        } else if (message.trigger_event_type === "swap") {
            let modal_exist_time =Math.min(4,Math.max(trigger_event_message.length / 10, 2));    
            await this.showModal(currPlayer, trigger_event_title, trigger_event_subtitle, trigger_event_message, [], modal_exist_time);
            let playerIndex1 = swap_event_info[0];
            let playerIndex2 = swap_event_info[1];
            let playerPos1 = swap_event_info[2];
            let playerPos2 = swap_event_info[3];
            let playerIsTurnOver1 = swap_event_info[4];
            let playerIsTurnOver2 = swap_event_info[5];
            await this.gameController.swapPlayer(playerIndex1, playerIndex2, playerPos1, playerPos2, playerIsTurnOver1, playerIsTurnOver2);
            this.audioManager.play("player_teleport");
        } else if (message.trigger_event_type === "swap_all") {
            let modal_exist_time =Math.min(4,Math.max(trigger_event_message.length / 10, 2));    
            await this.showModal(currPlayer, trigger_event_title, trigger_event_subtitle, trigger_event_message, [], modal_exist_time);
            if (swap_all_event_info.length > 0) {
                await this.gameController.swapAllPlayer(swap_all_event_info);
            }
            this.audioManager.play("player_teleport");
        } else if (message.trigger_event_type === "swap_except_self") {
            let modal_exist_time =Math.min(4,Math.max(trigger_event_message.length / 10, 2));    
            await this.showModal(currPlayer, trigger_event_title, trigger_event_subtitle, trigger_event_message, [], modal_exist_time);
            if (swap_except_self_event_info.length > 0) {
                await this.gameController.swapAllPlayer(swap_except_self_event_info);
            }
            this.audioManager.play("player_teleport");
        } else if (message.trigger_event_type === "teleport_all_random") {
            let modal_exist_time =Math.min(4,Math.max(trigger_event_message.length / 10, 2));    
            await this.showModal(currPlayer, trigger_event_title, trigger_event_subtitle, trigger_event_message, [], modal_exist_time);
            await this.gameController.teleportAllPlayer(teleport_all_random_event_info);
            this.audioManager.play("player_teleport");
        } else if (message.trigger_event_type === "teleport_except_self_random") {
            let modal_exist_time =Math.min(4,Math.max(trigger_event_message.length / 10, 2));    
            await this.showModal(currPlayer, trigger_event_title, trigger_event_subtitle, trigger_event_message, [], modal_exist_time);
            await this.gameController.teleportAllPlayer(teleport_except_self_random_event_info);
            this.audioManager.play("player_teleport");
        } else if (message.trigger_event_type === "normal") {
            let modal_exist_time =Math.min(4,Math.max(trigger_event_message.length / 10, 2));   
            await this.showModal(currPlayer, trigger_event_title, trigger_event_subtitle, trigger_event_message, [], modal_exist_time);
        }
        //money and variable change
        if ("money" in rolled_money_and_variables) {
            this.changeOneCashAmount(currPlayer, rolled_money_and_variables["money"]);
            //if money < 0, end game
            if (rolled_money_and_variables["money"] < 0 && game_is_already_ended === false) {
                this.endGame();
            }
            this.audioManager.play("money_deduction");
        }
        if ("x1" in rolled_money_and_variables) {
            this.changeOnePlayerVariable(currPlayer, rolled_money_and_variables["x1"], 1);
        }
        if ("x2" in rolled_money_and_variables) {
            this.changeOnePlayerVariable(currPlayer, rolled_money_and_variables["x2"], 2);
        }
        if ("x3" in rolled_money_and_variables) {
            this.changeOnePlayerVariable(currPlayer, rolled_money_and_variables["x3"], 3);
        }
        if ("x4" in rolled_money_and_variables) {
            this.changeOnePlayerVariable(currPlayer, rolled_money_and_variables["x4"], 4);
        }
        if ("x5" in rolled_money_and_variables) {
            this.changeOnePlayerVariable(currPlayer, rolled_money_and_variables["x5"], 5);
        }
        //after trigger event. change player
        this.changePlayer(nextPlayer, nextPlayerPos, nextPlayerIsTurnOver, onDiceRolled); 
    }

    async handleInit(message) {
        let players = message.players;
        let changeCash = message.changeCash;
        let nextPlayer = message.nextPlayer;
        let nextPlayerPos = message.next_player_info["pos"];
        let nextPlayerIsTurnOver = message.next_player_info["is_turn_over"];
        let posChange = message.posChange;
        let initDirection = message.initDirection;
        let eventMsg = message.decision;
        let title = message.title;
        let landname = message.landname;
        let owners = message.owners;
        let houses = message.houses;
        let player_names = message.player_names;
        let player_varible_1s = message.player_varible_1s;
        let player_varible_2s = message.player_varible_2s;
        let player_varible_3s = message.player_varible_3s;
        let player_varible_4s = message.player_varible_4s;
        let player_varible_5s = message.player_varible_5s;
        let NUM_OF_HOUSE_EQUAL_HOTEL = message.NUM_OF_HOUSE_EQUAL_HOTEL;
        this.initGame(players, changeCash, posChange, initDirection, player_varible_1s, player_varible_2s, player_varible_3s, player_varible_4s, player_varible_5s);

        await this.gameLoadingPromise;
        await this.hideModal(true);

        for (let i = 0; i < owners.length; i++) {
            if (owners[i] !== null) {
                this.gameController.addProperty(PropertyManager.PROPERTY_OWNER_MARK, i, owners[i]);
            }
        }

        for (let i = 0; i < houses.length; i++) {
            if (houses[i] === NUM_OF_HOUSE_EQUAL_HOTEL) {
                this.gameController.addProperty(PropertyManager.PROPERTY_HOTEL, i);
            }
            else {
                for (let building_num = 0; building_num < houses[i]; building_num++) {
                    this.gameController.addProperty(PropertyManager.PROPERTY_HOUSE, i);
                }
            }
        }

        if (message.waitDecision === "true") {
            const buttons = (this.myPlayerIndex === nextPlayer) ? [{
                text: "購買",
                callback: this.confirmDecision.bind(this)
            }, {
                text: "取消",
                callback: this.cancelDecision.bind(this)
            }] : [];
            eventMsg = this.players[nextPlayer].userName + " " + eventMsg;
            this.showModal(nextPlayer, title, landname, eventMsg, buttons);

        } else if (message.waitUserDefineDecision === "true") {
            const buttons = (this.myPlayerIndex === nextPlayer) ? [{
                text: message.confirm_button_text,
                callback: this.confirmUserDefineDecision.bind(this)
            }, {
                text: message.cancel_button_text,
                callback: this.cancelDecisionUserDefine.bind(this)
            }] : [];

            this.showModal(nextPlayer, title, landname, eventMsg, buttons);

        } else if (message.wait_multiple_choice_decision === "true") {
            let chance_card_answer = message.multiple_choice_info['multiple_choice_answer'];

            let choice_buttons = [];
            if(message.multiple_choice_info['multiple_choice_1'] !== "") {
                let choice_button = {
                    text: message.multiple_choice_info['multiple_choice_1'],
                    callback: (chance_card_answer === 1) ? this.confirmUserDefineDecision.bind(this) : this.wrongAnswer.bind(this),
                    isAnswer: (chance_card_answer === 1) ? true : false
                };
                choice_buttons.push(choice_button);
            }
            if(message.multiple_choice_info['multiple_choice_2'] !== "") {
                let choice_button = {
                    text: message.multiple_choice_info['multiple_choice_2'],
                    callback: (chance_card_answer === 2) ? this.confirmUserDefineDecision.bind(this) : this.wrongAnswer.bind(this),
                    isAnswer: (chance_card_answer === 2) ? true : false
                };
                choice_buttons.push(choice_button);
            }
            if(message.multiple_choice_info['multiple_choice_3'] !== "") {
                let choice_button = {
                    text: message.multiple_choice_info['multiple_choice_3'],
                    callback: (chance_card_answer === 3) ? this.confirmUserDefineDecision.bind(this) : this.wrongAnswer.bind(this),
                    isAnswer: (chance_card_answer === 3) ? true : false
                };
                choice_buttons.push(choice_button);
            }
            if(message.multiple_choice_info['multiple_choice_4'] !== "") {
                let choice_button = {
                    text: message.multiple_choice_info['multiple_choice_4'],
                    callback: (chance_card_answer === 4) ? this.confirmUserDefineDecision.bind(this) : this.wrongAnswer.bind(this),
                    isAnswer: (chance_card_answer === 4) ? true : false
                };
                choice_buttons.push(choice_button);
            }
            const buttons = choice_buttons;

            this.showModal(nextPlayer, title, landname, eventMsg, buttons);

        } else {
            this.changePlayer(nextPlayer, nextPlayerPos, nextPlayerIsTurnOver, this.onDiceRolled.bind(this));
        }
    }


    async handleAddErr() {
        await this.showModal(null, "未獲得許可", "找不到遊戲", "導回加入頁面中... 開始你自己的遊戲吧!", [], 5);
        window.location = (window.location.protocol === 'https:' ? 'https' : 'http') + `://${window.location.host}/monopoly/join/${this.userName}/${this.mapID}`;
    }


    async handleRollRes(message) {
        let currPlayer = message.curr_player;
        let nextPlayer = message.next_player;
        let steps = message.steps;
        let newPos = message.new_pos;
        let eventMsg = message.result;
        console.log(eventMsg);
        console.log(message.event_info);
        let title = message.title;
        let landname = message.landname;
        let curr_variable_1 = message.curr_variable_1;
        let curr_variable_2 = message.curr_variable_2;
        let curr_variable_3 = message.curr_variable_3;
        let curr_variable_4 = message.curr_variable_4;
        let curr_variable_5 = message.curr_variable_5;
        let rollResMsg = this.players[currPlayer].userName + " gets a roll result " + steps.toString();
        //if money < 0 end
        let bankrupt_end = false;
        let is_trigger_move_pass_start = message.event_info["is_trigger_move_pass_start"];
        let is_turn_over = message.event_info["is_turn_over"];

        this.audioManager.play("player_move");
        if (is_turn_over == "false") {
            await this.gameController.movePlayer(currPlayer, newPos);
        }  else if (is_turn_over == "true") {
            await this.gameController.movePlayerCounterclockwise(currPlayer, newPos);
        }
        await this.showModal(currPlayer, this.players[currPlayer].userName + " 骰岀 " + steps.toString(), "", "", [], 1.5);

        

        if (message.is_variable_1_change === "true") {
            this.changeOnePlayerVariable(currPlayer, curr_variable_1[0], 1);
        }
        if (message.is_variable_2_change === "true") {
            this.changeOnePlayerVariable(currPlayer, curr_variable_2[0], 2);
        }
        if (message.is_variable_3_change === "true") {
            this.changeOnePlayerVariable(currPlayer, curr_variable_3[0], 3);
        }
        if (message.is_variable_4_change === "true") {
            this.changeOnePlayerVariable(currPlayer, curr_variable_4[0], 4);
        }
        if (message.is_variable_5_change === "true") {
            this.changeOnePlayerVariable(currPlayer,curr_variable_5[0], 5);
        }

        //todo
        if (message.bypass_start === "true") {
            let eventMsg = this.players[currPlayer].userName + " 經過了起點<br><div>獲得了"+ message.START_REWARD + "元!";
            if (message.is_cash_change !== "true") {
                let cash = message.curr_cash;
                this.changeCashAmount(cash);
            }
            await this.showModal(currPlayer, "獲得獎勵", "起點", eventMsg, [], 2);
            this.audioManager.play("money_addition");
        }

        if (message.is_option === "true") {
            const buttons = (this.myPlayerIndex === currPlayer) ? [{
                text: "購買",
                callback: this.confirmDecision.bind(this)
            }, {
                text: "取消",
                callback: this.cancelDecision.bind(this)
            }] : [];

            this.showModal(currPlayer, title, landname, this.players[currPlayer].userName + eventMsg, buttons);
        } else if (message.is_user_define_option === "true") {
            const buttons = (this.myPlayerIndex === currPlayer) ? [{
                text: message.confirm_button_text,
                callback: this.confirmUserDefineDecision.bind(this)
            }, {
                text: message.cancel_button_text,
                callback: this.cancelDecisionUserDefine.bind(this)
            }] : [];

            this.showModal(currPlayer, title, landname, eventMsg, buttons);

        } else if (message.is_multiple_choice === "true") {
            let chance_card_answer = message.multiple_choice_info['multiple_choice_answer'];

            let choice_buttons = [];
            if(message.multiple_choice_info['multiple_choice_1'] !== "") {
                let choice_button = {
                    text: message.multiple_choice_info['multiple_choice_1'],
                    callback: (chance_card_answer === 1) ? this.confirmUserDefineDecision.bind(this) : this.wrongAnswer.bind(this),
                    isAnswer: (chance_card_answer === 1) ? true : false
                };
                choice_buttons.push(choice_button);
            }
            if(message.multiple_choice_info['multiple_choice_2'] !== "") {
                let choice_button = {
                    text: message.multiple_choice_info['multiple_choice_2'],
                    callback: (chance_card_answer === 2) ? this.confirmUserDefineDecision.bind(this) : this.wrongAnswer.bind(this),
                    isAnswer: (chance_card_answer === 2) ? true : false
                };
                choice_buttons.push(choice_button);
            }
            if(message.multiple_choice_info['multiple_choice_3'] !== "") {
                let choice_button = {
                    text: message.multiple_choice_info['multiple_choice_3'],
                    callback: (chance_card_answer === 3) ? this.confirmUserDefineDecision.bind(this) : this.wrongAnswer.bind(this),
                    isAnswer: (chance_card_answer === 3) ? true : false
                };
                choice_buttons.push(choice_button);
            }
            if(message.multiple_choice_info['multiple_choice_4'] !== "") {
                let choice_button = {
                    text: message.multiple_choice_info['multiple_choice_4'],
                    callback: (chance_card_answer === 4) ? this.confirmUserDefineDecision.bind(this) : this.wrongAnswer.bind(this),
                    isAnswer: (chance_card_answer === 4) ? true : false
                };
                choice_buttons.push(choice_button);
            }
            //shuffle array
            for (let i = choice_buttons.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [choice_buttons[i], choice_buttons[j]] = [choice_buttons[j], choice_buttons[i]];
            }

            const buttons = choice_buttons;

            this.showModal(currPlayer, title, landname, eventMsg, buttons, undefined, message.chance_card_background_img_url);

        } else {
            if (message.is_cash_change === "true") {
                let modal_exist_time = Math.min(4,Math.max((this.players[currPlayer].userName + eventMsg).length / 10, 1.5));
                await this.showModal(currPlayer, title, landname, this.players[currPlayer].userName + eventMsg, [], modal_exist_time);
                let cash = message.curr_cash;
                this.changeCashAmount(cash);
                this.audioManager.play("money_deduction");
                if (message.is_game_end === "true") {
                    bankrupt_end = true;
                } 
            } else if (message.is_user_define_event === "true") {
                let modal_exist_time =Math.min(4,Math.max(eventMsg.length / 10, 1.5));
                await this.showModal(currPlayer, title, landname, eventMsg, [], modal_exist_time);
                if (message.is_user_define_cash_change == "true") {
                    let curr_cash = message.curr_cash;
                    this.changeCashAmount(curr_cash);
                    this.audioManager.play("money_deduction");
                }
                if (message.is_game_end === "true") {
                    bankrupt_end = true;
                } 
            } else if (message.is_chance_card_event === "true") {
                let modal_exist_time = Math.min(4,Math.max((this.players[currPlayer].userName + eventMsg).length / 10, 1.5));
                await this.showModal(currPlayer, title, landname, eventMsg, [], modal_exist_time, message.chance_card_background_img_url);
                if (message.is_chance_card_cash_change == "true") {
                    let curr_cash = message.curr_cash;
                    this.changeCashAmount(curr_cash);
                    this.audioManager.play("money_deduction");
                }
                if (message.is_game_end === "true") {
                    bankrupt_end = true;
                } 
            } else if (message.is_simple_event === "true") {
                let modal_exist_time = Math.min(4,Math.max((this.players[currPlayer].userName + eventMsg).length / 10, 1.5));
                await this.showModal(currPlayer, title, landname, this.players[currPlayer].userName + eventMsg, [], modal_exist_time);
            } else if (message.is_not_show_event === "true") {
                //pass
            } else if (message.is_new_event === "true") {
                let modal_exist_time = Math.min(4,Math.max((this.players[currPlayer].userName + eventMsg).length / 10, 1.5));
                await this.showModal(currPlayer, title, landname, this.players[currPlayer].userName + eventMsg, [], modal_exist_time);
            } else {
                //pass
            }
        }
        //deal roller event and change player
        if (message.is_option === "false" && message.is_user_define_option === "false" && message.is_multiple_choice === "false") { 
            this.dealRolledEvent(message,  bankrupt_end, this.onDiceRolled.bind(this));
        }                       
    }

    handleBuyLand(message) {
        const {curr_player, curr_cash, tile_id} = message;
        this.changeCashAmount(curr_cash);
        this.gameController.addProperty(PropertyManager.PROPERTY_OWNER_MARK, tile_id, curr_player);
        //change variable
        let currPlayer = message.curr_player;
        let curr_variable_1 = message.curr_variable_1;
        let curr_variable_2 = message.curr_variable_2;
        let curr_variable_3 = message.curr_variable_3;
        let curr_variable_4 = message.curr_variable_4;
        let curr_variable_5 = message.curr_variable_5;
        if (message.is_variable_1_change === "true") {
            this.changeOnePlayerVariable(currPlayer, curr_variable_1[0], 1);
        }
        if (message.is_variable_2_change === "true") {
            this.changeOnePlayerVariable(currPlayer, curr_variable_2[0], 2);
        }
        if (message.is_variable_3_change === "true") {
            this.changeOnePlayerVariable(currPlayer, curr_variable_3[0], 3);
        }
        if (message.is_variable_4_change === "true") {
            this.changeOnePlayerVariable(currPlayer, curr_variable_4[0], 4);
        }
        if (message.is_variable_5_change === "true") {
            this.changeOnePlayerVariable(currPlayer,curr_variable_5[0], 5);
        }
        //deal rolled event
        let bankrupt_end = false;
        this.dealRolledEvent(message,  bankrupt_end, this.onDiceRolled.bind(this)); 
    }

    handleConstruct(message) {
        let curr_cash = message.curr_cash;
        let tile_id = message.tile_id;
        this.changeCashAmount(curr_cash);
        if (message.build_type === "house") {
            this.gameController.addProperty(PropertyManager.PROPERTY_HOUSE, tile_id);
        } else {
            this.gameController.addProperty(PropertyManager.PROPERTY_HOTEL, tile_id);
        }
        this.audioManager.play("build");
        //change variable
        let currPlayer = message.curr_player;
        let curr_variable_1 = message.curr_variable_1;
        let curr_variable_2 = message.curr_variable_2;
        let curr_variable_3 = message.curr_variable_3;
        let curr_variable_4 = message.curr_variable_4;
        let curr_variable_5 = message.curr_variable_5;
        if (message.is_variable_1_change === "true") {
            this.changeOnePlayerVariable(currPlayer, curr_variable_1[0], 1);
        }
        if (message.is_variable_2_change === "true") {
            this.changeOnePlayerVariable(currPlayer, curr_variable_2[0], 2);
        }
        if (message.is_variable_3_change === "true") {
            this.changeOnePlayerVariable(currPlayer, curr_variable_3[0], 3);
        }
        if (message.is_variable_4_change === "true") {
            this.changeOnePlayerVariable(currPlayer, curr_variable_4[0], 4);
        }
        if (message.is_variable_5_change === "true") {
            this.changeOnePlayerVariable(currPlayer,curr_variable_5[0], 5);
        }
        //deal rolled event
        let bankrupt_end = false;
        this.dealRolledEvent(message,  bankrupt_end, this.onDiceRolled.bind(this));        
    }

    handleConfirmUserDefine(message) {
        let curr_cash = message.curr_cash;
        this.changeCashAmount(curr_cash);
        //change variable
        let currPlayer = message.curr_player;
        let curr_variable_1 = message.curr_variable_1;
        let curr_variable_2 = message.curr_variable_2;
        let curr_variable_3 = message.curr_variable_3;
        let curr_variable_4 = message.curr_variable_4;
        let curr_variable_5 = message.curr_variable_5;
        if (message.is_variable_1_change === "true") {
            this.changeOnePlayerVariable(currPlayer, curr_variable_1[0], 1);
        }
        if (message.is_variable_2_change === "true") {
            this.changeOnePlayerVariable(currPlayer, curr_variable_2[0], 2);
        }
        if (message.is_variable_3_change === "true") {
            this.changeOnePlayerVariable(currPlayer, curr_variable_3[0], 3);
        }
        if (message.is_variable_4_change === "true") {
            this.changeOnePlayerVariable(currPlayer, curr_variable_4[0], 4);
        }
        if (message.is_variable_5_change === "true") {
            this.changeOnePlayerVariable(currPlayer,curr_variable_5[0], 5);
        }
        //deal rolled event
        let bankrupt_end = false;
        if (message.is_game_end === "true") {
            bankrupt_end = true;
        }
        this.dealRolledEvent(message,  bankrupt_end, this.onDiceRolled.bind(this));
    }

    handleCancel(message) {
        console.log(message);
        //deal rolled event
        let bankrupt_end = false;
        this.dealRolledEvent(message,  bankrupt_end, this.onDiceRolled.bind(this)); 
    }

    handleCancelUserDefine(message) {
        let next_player = message.next_player;
        let nextPlayerPos = message.next_player_info["pos"];
        let nextPlayerIsTurnOver = message.next_player_info["is_turn_over"];
        this.changePlayer(message.next_player, nextPlayerPos, nextPlayerIsTurnOver, this.onDiceRolled.bind(this));
        //deal rolled event
        let bankrupt_end = false;
        this.dealRolledEvent(message,  bankrupt_end, this.onDiceRolled.bind(this));
    }

    handleWrongAnswer(message) {
        let curr_cash = message.curr_cash;
        this.changeCashAmount(curr_cash);
        let next_player = message.next_player;
        let nextPlayerPos = message.next_player_info["pos"];
        let nextPlayerIsTurnOver = message.next_player_info["is_turn_over"];
        this.changePlayer(message.next_player, nextPlayerPos, nextPlayerIsTurnOver, this.onDiceRolled.bind(this));
        //deal rolled event
        let bankrupt_end = false;
        if (message.is_game_end === "true") {
            bankrupt_end = true;
        }
        this.dealRolledEvent(message, bankrupt_end, this.onDiceRolled.bind(this));
    }

    async handleGameEnd(message) {
        this.gameInProcess = false;

        let result = [];
        // let loser = message.loser;
        let all_scores = message.all_scores;
        for (let k = 0; k < all_scores.length; k++) {
            let big_asset = -1e20;
            let big_index = 0;
            for (let i = 0; i < all_scores.length; i++) {
                if (all_scores[i] === null) {
                    continue;
                }
                if (big_asset < all_scores[i]) {
                    big_asset = all_scores[i];
                    big_index = i;
                }
            }
            result.push({
                playerIndex: big_index,
                score: big_asset,
            });
            all_scores.splice(big_index, 1, null);
        }
        let score_board_info = message.score_board_info;
        if (score_board_info['is_descending_order'] === false) {
            result = result.reverse();
        }
        this.showScoreboard(result, score_board_info);
    }

    handleChat(message) {
        let sender = message.sender;
        let content = message.content;
        this.addChatMessage(sender, content);
    }

    async confirmDecision() {
        this.socket.send(JSON.stringify({
            action: "confirm_decision",
            hostname: this.hostName,
        }));

        this.audioManager.play("money_deduction");
        await this.hideModal(true);
    }

    async confirmUserDefineDecision() {
        this.socket.send(JSON.stringify({
            action: "confirm_user_define_decision",
            hostname: this.hostName,
        }));

        this.audioManager.play("money_deduction");
        await this.hideModal(true);
    }

    async cancelDecision() {
        this.socket.send(JSON.stringify({
            action: "cancel_decision",
            hostname: this.hostName,
        }));
        await this.hideModal(true);
    }

    async cancelDecisionUserDefine() {
        this.socket.send(JSON.stringify({
            action: "cancel_decision_user_define",
            hostname: this.hostName,
        }));
        await this.hideModal(true);
    }

    async wrongAnswer() {
        this.socket.send(JSON.stringify({
            action: "wrong_answer",
            hostname: this.hostName,
        }));
        this.audioManager.play("wrong_answer");
        await this.hideModal(true);
    }

    /*
    * Add a chat message
    * playerIndex: int
    * message: string
    * */
    addChatMessage(playerIndex, message) {
        let messageElement = document.createElement("div");
        messageElement.classList.add("chat-message");
        messageElement.innerHTML = `
            <img class="chat-message-avatar" src="/static/images/player_${playerIndex}.png">
            <span class="chat-message-content">${message}</span>`;
        this.$chatMessageContainer.appendChild(messageElement);
    }

    sendMessage() {
        const message = this.$chatMessageToSend.value;
        this.socket.send(JSON.stringify({
            action: "chat",
            from: this.myPlayerIndex,
            content: message,
        }));
        this.$chatMessageToSend.value = "";
    }

    /*
    * ScoreList should be sorted
    * [{
    *   playerIndex: int,
    *   score: int
    * }]
    * */
    showScoreboard(scoreList, score_board_info) {
        let scoreboardTemplate = `<div id="scoreboard">`;
        for (let index in scoreList) {
            let rank = parseInt(index) + 1;
            scoreboardTemplate += `
                <div class="scoreboard-row">
                    <span class="scoreboard-ranking">${rank}</span>
                    <img class="chat-message-avatar" src="${this.players[scoreList[index].playerIndex].avatar}">
                    <span class="scoreboard-username">${this.players[scoreList[index].playerIndex].fullName}</span>
                    <div class="monopoly-cash">M</div>
                    <span class="scoreboard-score">${scoreList[index].score}</span>
                </div>`;
        }
        scoreboardTemplate += "</div>";
        let scoreboardBackGroungAudio = score_board_info.audio_url;
        let score_board_sound_effect = score_board_info.score_board_sound_effect
        if (score_board_sound_effect !== "background" && scoreboardBackGroungAudio !== "") {
            this.audioManager.stop("background");
            this.audioManager.play("scoreboard_bgm");
        }
        let backgroundImgUrl = score_board_info.background_img_url;
        console.log(backgroundImgUrl === "");
        this.$modalCardContent.classList.add("scoreboard-bg");
        if (backgroundImgUrl !== "") {
            $('.scoreboard-bg').css('background', `url("${backgroundImgUrl}") no-repeat`);
            $('.scoreboard-bg').css('background-size', `cover`);
        }
        this.showModal(null, score_board_info.title, score_board_info.subtitle, scoreboardTemplate, [{
            text: "開始新遊戲",
            callback: () => {
                window.location = (window.location.protocol === 'https:' ? 'https' : 'http') + `://${window.location.host}/monopoly/join/${this.hostName}/${this.mapID}`;
            }
        }]);
    }

    switchAudio() {
        if (this.audioManager.playing) {
            this.$audioControl.classList.add("control-off");
        } else {
            this.$audioControl.classList.remove("control-off");
        }
        this.audioManager.mute();
    }

    showHelp() {
        this.showingHelp = !this.showingHelp;

        if (this.showingHelp) {
            this.$helpControl.classList.remove("control-off");
            this.$helpOverlay.classList.remove("hidden");
        } else {
            this.$helpControl.classList.add("control-off");
            this.$helpOverlay.classList.add("hidden");
        }
    }

    endGame() {
        this.socket.send(JSON.stringify({
            action: "end_game",
        }));
    }

    roll_1() {
        this.socket.send(JSON.stringify({
            action: "roll_1",
        }));
    }
    roll_2() {
        this.socket.send(JSON.stringify({
            action: "roll_2",
        }));
    }
    roll_3() {
        this.socket.send(JSON.stringify({
            action: "roll_3",
        }));
    }
    roll_4() {
        this.socket.send(JSON.stringify({
            action: "roll_4",
        }));
    }
    roll_5() {
        this.socket.send(JSON.stringify({
            action: "roll_5",
        }));
    }
    roll_6() {
        this.socket.send(JSON.stringify({
            action: "roll_6",
        }));
    }
    roll_10() {
        this.socket.send(JSON.stringify({
            action: "roll_10",
        }));
    }
    roll_20() {
        this.socket.send(JSON.stringify({
            action: "roll_20",
        }));
    }
    roll_30() {
        this.socket.send(JSON.stringify({
            action: "roll_30",
        }));
    }
    notify_cheat() {
        this.socket.send(JSON.stringify({
            action: "notify_cheat",
        }));
    }

    rotate_negative_90() {
        this.gameController.rotateCameraTheta(-90);
    }

    rotate_positive_90() {
        this.gameController.rotateCameraTheta(90);
    }

    rotate_phi() {
        if (this.$cameraControlPhi.innerHTML === "鳥瞰視角") {
            console.log("save state");
            this.gameController.saveCameraState();
            this.gameController.rotateCameraPhi(-90);
            this.gameController.dollyCamera(-30);
            this.$cameraControlPhi.innerHTML = "預設視角";
        } else if (this.$cameraControlPhi.innerHTML === "預設視角") {
            this.gameController.resetCamera();
            this.$cameraControlPhi.innerHTML = "鳥瞰視角";
        }
    }

    dolly_negative_2() {
        this.gameController.dollyCamera(-2);
    }

    dolly_positive_2() {
        this.gameController.dollyCamera(2);
    }

    enable_mouse() {
        if (this.$cameraControlEnableMouse.innerHTML === "允許滑鼠控制") {
            this.gameController.enableMouse( true );
            this.$cameraControlEnableMouse.innerHTML = "禁止滑鼠控制";

        } else if (this.$cameraControlEnableMouse.innerHTML === "禁止滑鼠控制") {
            this.gameController.enableMouse( false );
            this.$cameraControlEnableMouse.innerHTML = "允許滑鼠控制";
        }
    }

    reset_camera() {
        this.gameController.changeCameraPosition(this.nextPlayerPos, this.nextPlayerIsTurnOver);
        this.gameController.enableMouse( false );
        this.$cameraControlEnableMouse.innerHTML = "允許滑鼠控制";
        this.$cameraControlPhi.innerHTML = "鳥瞰視角";

    }

    isImgLink(url) {
        if(typeof url !== 'string') return false;
        return(url.match(/^http[^\?]*.(jpg|jpeg|gif|png|tiff|bmp)(\?(.*))?$/gmi) != null);
    }

    // async handleGameEnd() {
    //     await this.showModal(null, "Game Terminated by Host", "", "Navigating back...", [], 5);
    //     window.location = `http://${window.location.host}/monopoly/join`;
    // }
}

window.onload = () => {
    new GameView();
};

GameView.DEFAULT_AVATAR = "/static/images/favicon.png";

GameView.PLAYERS_COLORS = ["#FFD54F", "#90CAF9", "#E0E0E0", "#B39DDB"];