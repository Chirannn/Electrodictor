// POPUP FUNCTION

function enterDashboard(){

    const username =
        document.getElementById("popup-name").value;

    if(username.trim() === ""){

        alert("Please enter your name!");
        return;
    }

    document.getElementById("popup").style.display = "none";

    document.getElementById("welcome-message").innerHTML =
        "Welcome " + username + " ⚡";
}

// LIVE DATE & TIME

function updateDateTime(){

    const now = new Date();

    document.getElementById("clock").innerHTML =
        now.toLocaleTimeString();

    document.getElementById("live-date").innerHTML =
        now.toDateString();
}

setInterval(updateDateTime,1000);

updateDateTime();

// WELCOME USER

function welcomeUser(){

    const username = document.getElementById("username").value;

    if(username.trim() === ""){
        alert("Please enter your name!");
        return;
    }

    alert("Welcome " + username + " ⚡");

    document.getElementById("welcome-message").innerHTML =
        "Hello " + username + ", let's predict your electricity usage!";
}

// PREDICTION FUNCTION

async function predictConsumption(){

    document.getElementById("loader").style.display = "block";

    const voltage = document.getElementById("voltage").value;
    const intensity = document.getElementById("intensity").value;
    const sub1 = document.getElementById("sub1").value;
    const sub2 = document.getElementById("sub2").value;
    const sub3 = document.getElementById("sub3").value;

    const response = await fetch("/predict", {

        method: "POST",

        headers:{
            "Content-Type":"application/json"
        },

        body: JSON.stringify({

            voltage: voltage,
            intensity: intensity,
            sub_metering_1: sub1,
            sub_metering_2: sub2,
            sub_metering_3: sub3

        })

    });
}