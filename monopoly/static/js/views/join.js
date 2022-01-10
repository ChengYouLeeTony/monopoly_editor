"use strict";

/**
 *WebSocket Interface
 */

/*const receivedMessage = {
    action: "join" | "start",
    data: [{
        id: "user_id",
        name: "user_name",
        avatar: "user_url"
    }]
};

const sentMessage = {
    action: "start"
};*/

class JoinView {
    constructor() {
        this.userName = document.getElementById("user-name").value;
        this.hostName = document.getElementById("host-name").value;
        this.mapID = document.getElementById("map-id").value;
        this.viewerUrl = document.getElementById("viewer-url").value
        this.friends = [this.userName];

        this.initComponents();
        this.initWebSocket();
    }

    initComponents() {
        this.$usersContainer = document.getElementById("joined-users-container");
        this.$newGameNotice = document.getElementById("new-game-notice");
        this.$startGame = document.getElementById("start-game");
        this.$clearFriends = document.getElementById("clear-friends");
        this.$clearHistory = document.getElementById("clear-history");
        this.$leaveGame = document.getElementById("leave-game");
        this.$backToHome = document.getElementById("back-to-home");
        this.$startGameCreator = document.getElementById("start-game-creator");
        this.$startGame.addEventListener("click", () => {
            this.startGame();
        });
        this.$clearHistory.addEventListener("click", () => {
            this.clearHistory();
        });
        this.$clearFriends.addEventListener("click", () => {
            this.clearFriends();
        });
        this.$leaveGame.addEventListener("click", () => {
            this.clientLeaveGame();
        });
        this.$startGameCreator.addEventListener("click", () => {
            this.startGameCreator();
        });

        if (this.userName === this.hostName) {
            this.$invitationLink = document.getElementById("invitation-url");
            this.$invitationLink.value = (window.location.protocol === 'https:' ? 'https://' : '') +  `${window.location.host}/monopoly/join/${this.hostName}/${this.mapID}`;

            this.$copyTooltip = document.getElementById("copied-tooltip");
            this.$copyButton = document.getElementById("share-invitation");
            this.$copyButton.addEventListener("click", () => {
                this.copyToClipboard();
            })
            this.$viewerLink = document.getElementById("for-viewer-url");
            this.$viewerLink.value = (window.location.protocol === 'https:' ? 'https://' : '') + `${window.location.host}/monopoly/game/${this.hostName}/${this.viewerUrl}`;

            this.$copyTooltipViewer= document.getElementById("copied-tooltip-viewer");
            this.$copyButtonViewer = document.getElementById("share-viewer");
            this.$copyButtonViewer.addEventListener("click", () => {
                this.copyToClipboardViewer();
            })
        }

        const isProfileInited = document.getElementById("user-avatar").getAttribute("src").length !== 0;
        if (!isProfileInited) {
            const $addProfileButton = document.getElementById("init-profile");
            $addProfileButton.classList.remove("hidden");
        }
    }

    initWebSocket() {
        this.socket = new WebSocket((window.location.protocol === 'https:' ? 'wss' : 'ws') + `://${window.location.host}/join/${this.hostName}/${this.mapID}`);

        this.socket.onmessage = (event) => {
            const message = JSON.parse(event.data);
            this.handleStatusChange(message);
        }
    }

    handleStatusChange(message) {
        if (message.action === "join") {
            this.addFriend(message.data);

            if (this.friends.length >= 1) {
                if (this.hostName !== this.userName) {
                    this.$startGame.innerText = "等待室長開始遊戲...";
                    this.$clearFriends.style.display = "none";
                    this.$clearHistory.style.display = "none";
                } else {
                    this.$startGame.disabled = false;
                    this.$startGame.innerText = "開始遊戲";
                    this.$leaveGame.style.display = "none";
                }
            }
        } else if (message.action === "start") {
            this.navigateToGame();
        } else if (message.action === "start_creator") {
            this.navigateToGameCreator();
        }else if (message.action === "clear_friends") {
            this.onlyHostLeft(message.data, message.host_name);
        } else if (message.action === "client_leave_game") {
            this.removeFriend(message.data, message.host_name, message.client_name);
        } else if (message.action === "clear_history") {
            location.reload();
        } else if (message.action === "fail_join") {
            this.$startGame.disabled = true;
            this.$startGame.innerText = "Navigating back... Create your own game!";
            this.$newGameNotice.innerText = "4 Players Max Per Game!";
            this.$newGameNotice.style.color = "#F44336";
            setTimeout(this.navigateBack, 2000);
        }
    }

    addFriend(friends) {
        for (let friend of friends) {
            if (this.friends.indexOf(friend.name) !== -1 || friend.name === this.userName) continue;

            this.friends.push(friend.name);

            this.$usersContainer.innerHTML += `
                <a href="/monopoly/profile/${friend.name}" target="_blank">
                    <img class="joined-user-avatar" src="${friend.avatar}" title="${friend.name}">
                </a>
            `;
        }
    }

    onlyHostLeft(friends, host_name) {
        if (this.hostName !== this.userName) {
            this.$startGame.innerText = "您已被踢出遊戲";
            this.$leaveGame.style.display = "none";
            this.$backToHome.style.display = "block";
            this.leaveGame();
        } 
        for (let friend of friends) {
            if (friend.name === host_name) {
                this.friends = [this.hostName];
                this.$usersContainer.innerHTML = `
                <a href="/monopoly/profile/${friend.name}" target="_blank">
                    <img class="joined-user-avatar" src="${friend.avatar}" title="${friend.name}">
                </a>
            `;
            }
        }
    }

    removeFriend(friends, host_name, client_name) {
        console.log(client_name);
        this.$usersContainer.innerHTML = "";
        if (this.hostName !== this.userName) {
            this.$startGame.innerText = "您已離開遊戲";
            this.$leaveGame.style.display = "none";
            this.$backToHome.style.display = "block";
            this.leaveGame();
        } 
        for (let friend of friends) {
            if (friend.name === client_name) {
                continue;
            }
            this.friends.push(friend.name);

            this.$usersContainer.innerHTML += `
                <a href="/monopoly/profile/${friend.name}" target="_blank">
                    <img class="joined-user-avatar" src="${friend.avatar}" title="${friend.name}">
                </a>
            `;
           
        }
    }

    startGame() {
        this.socket.send(JSON.stringify({
            action: "start"
        }));
    }
    startGameCreator() {
        this.socket.send(JSON.stringify({
            action: "start_game_creator"
        }));
    }

    clearFriends() {
        this.socket.send(JSON.stringify({
            action: "clear_friends"
        }));
    }

    clearHistory() {
        this.socket.send(JSON.stringify({
            action: "clear_history"
        }));
    }

    clientLeaveGame() {
        this.socket.send(JSON.stringify({
            action: "client_leave_game"
        }));
    }

    leaveGame() {
        this.socket.send(JSON.stringify({
            action: "leave_game"
        }));
    }

    navigateToGame() {
        window.location = (window.location.protocol === 'https:' ? 'https' : 'http') + `://${window.location.host}/monopoly/game/${this.hostName}`;
    }
    navigateToGameCreator() {
        window.location = (window.location.protocol === 'https:' ? 'https' : 'http') + `://${window.location.host}/monopoly/game/${this.hostName}/creator`;
    }

    navigateBack() {
        window.location = (window.location.protocol === 'https:' ? 'https' : 'http') + + `://${window.location.host}/monopoly/join`;
    }

    copyToClipboard() {
        let copyText = this.$invitationLink;
        copyText.select();
        document.execCommand("Copy");

        this.$copyTooltip.classList.add("shown");
        setTimeout(() => {
            this.$copyTooltip.classList.remove("shown");
        }, 2000);
    }

    copyToClipboardViewer() {
        let copyText = this.$viewerLink;
        copyText.select();
        document.execCommand("Copy");

        this.$copyTooltipViewer.classList.add("shown");
        setTimeout(() => {
            this.$copyTooltipViewer.classList.remove("shown");
        }, 2000);
    }
}

window.onload = () => {
    new JoinView();
};