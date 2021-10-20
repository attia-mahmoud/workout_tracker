document.addEventListener('DOMContentLoaded', function() {

    window.onscroll = () => {
        var element = document.getElementById("navigate");
        if (window.scrollY >= 1000) {
            element.classList.add("bg-dark");
            element.classList.remove("nav-transparent")
        }
        else if (window.scrollY === 0) {
            element.classList.remove("bg-dark");
            element.classList.add("nav-transparent")
        }
        else {
            element.classList.remove("bg-dark");
            element.classList.add("nav-transparent")
        }
    };

    document.querySelectorAll('.choose').forEach(button => {
        button.onclick=function() {
            showpage(this.dataset.page);
        }
    });

    document.addEventListener('input', function (event) {
        if (event.target.id == 'dates') {
            console.log(event.target.value);
            document.querySelectorAll(".parents").forEach(parent => {
                parent.innerHTML = '';
            })
            
            showdate(event.target.value);
        }
    });

    

    
});

function refresh() {
    document.querySelectorAll('.parents').forEach(parent => {
        parent.style.display = 'none';
    });
}

function join() { 
    const thanks = document.getElementById("thanks");
    thanks.innerHTML = 'Thank you for joining.'; 
    thanks.style.fontSize = "40px";
    document.getElementById("inputer").style.display="none"; 
}

function showpage(page) {
    document.querySelectorAll('.form').forEach(div => {
        div.style.display = 'none';
    });
    document.querySelector(`#${page}`).style.display = 'block';
    console.log(page);
    const body = document.querySelector('body');
    if (page == 'page1') {
        body.removeAttribute("class");
        body.classList.add("weight-bg");
    }
    else if (page == 'page2') {
        body.removeAttribute("class");
        body.classList.add("calis-bg");
    }
    else if (page == 'page3'){
        body.removeAttribute("class");
        body.classList.add("cardio-bg");
    }
}

function showdate(date) {
    fetch(`/workout/${date}`)
    .then(response => response.json())
    .then(data => {
        data = JSON.parse(data);
        console.log(data);
        var arraylength = data.length;
        console.log(arraylength);
        addworkout(data);
    })
};

function addworkout(data) {
    
    const length = data.length; 
    var weight = 0;
    var calis = 0;
    var cardio = 0;
    for (i=0; i < length; i++) {
        var workout = data[i].fields.workout;
        var session_id = data[i].pk;
        
        console.log(session_id);
        console.log(workout);
        jukebox(workout, session_id);
        if (workout == "weight") {
            weight = weight + 1;
        }
        else if (workout == "calisthenics") {
            calis = calis  + 1;
        }
        else if (workout == "cardio") {
            cardio = cardio + 1;
        }
    }
    check(weight, calis, cardio);
    
    
};

function jukebox(workout, session_id) {
    fetch(`/jukebox/${workout}/${session_id}`)
    .then(response => response.json())
    .then(data => {
        data = JSON.parse(data);
        console.log(data);
        const post = document.createElement('div');
        const model = data[0].model;
        if (model == "auctions.weights") {
            const exercise = data[0].fields.exercise;
            const reps = data[0].fields.reps;
            const sets = data[0].fields.sets;
            const weight = data[0].fields.weight;
            post.append(`${exercise} for ${sets} sets of ${reps} reps at ${weight}kg.`);
            post.classList.add('list');
            
            document.querySelector('.weights').append(post);
        }
        else if (model == "auctions.calisthenics") {
            const exercise = data[0].fields.exercise;
            const reps = data[0].fields.reps;
            const sets = data[0].fields.sets;
            post.append(`${exercise} for ${sets} sets of ${reps} reps.`);
            post.classList.add('list');
           
            document.querySelector('.calis').append(post);
        }
        else if (model == "auctions.cardio") {
            const exercise = data[0].fields.exercise;
            const duration = data[0].fields.duration;
            const distance = data[0].fields.distance;
            post.append(`${exercise} ${distance}km for ${duration} minutes.`);
            post.classList.add('list');
            
            document.querySelector('.cardio').append(post);
        }
        
    })
}


