const players = {
    basketball: ["Michael Jordan", "LeBron James", "Kobe Bryant", "Shaquille O'Neal", "Stephen Curry"],
    soccer: ["Lionel Messi", "Cristiano Ronaldo", "Neymar", "Zinedine Zidane", "Pelé"]
};

async function loadBaseballPlayers() {
    const [pitchers, batters] = await Promise.all([
        fetch("MLB_pitcher_ERA+.json").then(res => res.json()),
        fetch("MLB_position_player_Rbat+.json").then(res => res.json())
    ]);

    const pitcherDropdown = document.getElementById("pitchers");
    const batterDropdown = document.getElementById("positionPlayers");

    pitchers.forEach(player => {
        const option = document.createElement("option");
        option.value = JSON.stringify({ name: player.Player, type: "pitcher", rank: player.Rank });
        option.textContent = `${player.Rank} ${player.Player}`;
        pitcherDropdown.appendChild(option);
    });

    batters.forEach(player => {
        const option = document.createElement("option");
        option.value = JSON.stringify({ name: player.Player, type: "batter", rank: player.Rank });
        option.textContent = `${player.Rank} ${player.Player}`;
        batterDropdown.appendChild(option);
    });
}

async function loadFootballPlayers() {
    const [qbs, rbs, wrs] = await Promise.all([
        fetch("NFL_QB_Players.json").then(res => res.json()),
        fetch("NFL_RB_Players.json").then(res => res.json()),
        fetch("NFL_WR_Players.json").then(res => res.json())
    ]);

    const qbDropdown = document.getElementById("QBs");
    const rbDropdown = document.getElementById("RBs");
    const wrDropdown = document.getElementById("WRs");

    qbs.forEach(player => {
        const option = document.createElement("option");
        option.value = JSON.stringify({ name: player.Player, type: "QB", rank: player.Rank });
        option.textContent = `${player.Rank}. ${player.Player}`;
        qbDropdown.appendChild(option);
    });

    rbs.forEach(player => {
        const option = document.createElement("option");
        option.value = JSON.stringify({ name: player.Player, type: "RB", rank: player.Rank });
        option.textContent = `${player.Rank}. ${player.Player}`;
        rbDropdown.appendChild(option);
    });

    wrs.forEach(player => {
        const option = document.createElement("option");
        option.value = JSON.stringify({ name: player.Player, type: "WR", rank: player.Rank });
        option.textContent = `${player.Rank}. ${player.Player}`;
        wrDropdown.appendChild(option);
    });
}

function populateDropdown(sport) {
    if (sport === "baseball") {
        loadBaseballPlayers();
    } else if (sport === "football") {
        loadFootballPlayers();
    } else {
        const dropdown = document.getElementById(`${sport}Players`);
        players[sport].forEach(player => {
            const option = document.createElement("option");
            option.value = player;
            option.textContent = player;
            dropdown.appendChild(option);
        });
    }
}

function loadTeams() {
    ["baseball", "football", "basketball", "soccer"].forEach(sport => {
        const team = JSON.parse(localStorage.getItem(`${sport}Team`)) || [];
        team.forEach(player => addPlayerToUI(sport, player, false));
    });
}

function addPlayer(sport, type = null) {
    let dropdown, selectedValue;

    if (sport === "baseball") {
        dropdown = document.getElementById(type === "pitcher" ? "pitchers" : "positionPlayers");
        selectedValue = dropdown.value;

        if (!selectedValue) {
            alert("Please select a player.");
            return;
        }

        const { name } = JSON.parse(selectedValue);
        let team = JSON.parse(localStorage.getItem("baseballTeam")) || [];

        const pitcherCount = team.filter(p => p.type === "pitcher").length;
        const batterCount = team.filter(p => p.type === "batter").length;

        if (team.find(p => p.name === name)) {
            alert("This player is already in your team.");
            return;
        }

        if (type === "pitcher" && pitcherCount >= 2) {
            alert("You can only select 2 pitchers.");
            return;
        }

        if (type === "batter" && batterCount >= 2) {
            alert("You can only select 2 position players.");
            return;
        }

        const player = { name, type };
        team.push(player);
        localStorage.setItem("baseballTeam", JSON.stringify(team));
        addPlayerToUI("baseball", player, false);
    } else if (sport === "football") {
        let selectedType;
        // Corrected dropdown access for football players
        if (type === "QB") {
            dropdown = document.getElementById("QBs");
        } else if (type === "RB") {
            dropdown = document.getElementById("RBs");
        } else if (type === "WR") {
            dropdown = document.getElementById("WRs");
        }

        selectedValue = dropdown.value;

        if (!selectedValue) {
            alert("Please select a player.");
            return;
        }

        const { name } = JSON.parse(selectedValue);
        let team = JSON.parse(localStorage.getItem("footballTeam")) || [];

        const qbCount = team.filter(p => p.type === "QB").length;
        const rbCount = team.filter(p => p.type === "RB").length;
        const wrCount = team.filter(p => p.type === "WR").length;

        if (team.find(p => p.name === name)) {
            alert("This player is already in your team.");
            return;
        }

        if (type === "QB" && qbCount >= 2) {
            alert("You can only select 2 QBs.");
            return;
        }

        if (type === "RB" && rbCount >= 2) {
            alert("You can only select 2 RBs.");
            return;
        }

        if (type === "WR" && wrCount >= 2) {
            alert("You can only select 2 WRs.");
            return;
        }

        const player = { name, type };
        team.push(player);
        localStorage.setItem("footballTeam", JSON.stringify(team));
        addPlayerToUI("football", player, false);
    } else {
        dropdown = document.getElementById(`${sport}Players`);
        selectedValue = dropdown.value;

        if (!selectedValue) {
            alert("Please select a player.");
            return;
        }

        let team = JSON.parse(localStorage.getItem(`${sport}Team`)) || [];

        if (team.length >= 5) {
            alert("You can only select 5 players per sport.");
            return;
        }

        if (team.includes(selectedValue)) {
            alert("This player is already in your team.");
            return;
        }

        team.push(selectedValue);
        localStorage.setItem(`${sport}Team`, JSON.stringify(team));
        addPlayerToUI(sport, selectedValue, true);
    }
}

function addPlayerToUI(sport, player, saveToStorage) {
    const teamList = document.getElementById(`${sport}Team`);
    const listItem = document.createElement("li");
    const playerName = typeof player === "string" ? player : player.name;

    listItem.textContent = playerName;

    const removeButton = document.createElement("button");
    removeButton.textContent = "Remove";
    removeButton.classList.add("remove-btn");
    removeButton.onclick = function () {
        removePlayer(sport, player);
    };

    listItem.appendChild(removeButton);
    teamList.appendChild(listItem);

    if (saveToStorage) {
        const team = JSON.parse(localStorage.getItem(`${sport}Team`)) || [];
        team.push(player);
        localStorage.setItem(`${sport}Team`, JSON.stringify(team));
    }
}

function removePlayer(sport, player) {
    let team = JSON.parse(localStorage.getItem(`${sport}Team`)) || [];

    team = team.filter(p => p.name !== player.name);

    localStorage.setItem(`${sport}Team`, JSON.stringify(team));
    document.getElementById(`${sport}Team`).innerHTML = "";
    team.forEach(p => addPlayerToUI(sport, p, false));
}

document.addEventListener("DOMContentLoaded", function () {
    ["baseball", "football", "basketball", "soccer"].forEach(populateDropdown);
    loadTeams();
});
