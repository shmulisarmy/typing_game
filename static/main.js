function progressSnapShot(){
    progress.push(letterUpTo)
}

function toggleNightMode(){
    $('body').toggleClass('night-mode')
}


function LoadNextLevel(){
    $.ajax({
        type: "GET",
        url:   `/loadNextLevel/${levelUpTo}`,
        async: false, // Make the request synchronous
        data: {
            wpm: wpm
        },
        success: function(response) {
            // Assign the response to the variable
            sentence = response;
        },
        error: function(xhr, status, error) {
            // Handle errors here
            console.error(xhr.responseText);
        }
    });
    clearInterval(wpmInterval)
    $wpm.text("next level loaded");
    levelUpTo++
    $('#levelUpTo').text(levelUpTo)
    letterUpTo = 0
    startTime = false
    setSpans();

}


function BackSpace() {
    // modifier
    letterUpTo--
    allSpans.eq(letterUpTo).css({
        "color": "white",
        "background-color": "transparent",
    })
}
function wpmCalc() {
    if (!startTime) {
        startTime = Date.now()
        return
    }
    timeSinceStart = Date.now() - startTime
    wpm = Math.round(letterUpTo / (timeSinceStart / 1000 / 12))
    $wpm.text(`wpm: ${wpm}`)
}


const text = $('.text')
let letterUpTo = 0;
let key, startTime, timeSinceStart, wpm, backAWord, allSpans, wpmInterval;
let levelUpTo = parseInt($('#levelUpTo').text())
const ignore_letters = ["Command", "Shift"]
const $wpm = $('.wpm')
let progress = [];

setSpans();

window.addEventListener("keydown", event => {
    key = event.key
    console.log(key)
    if (key == "Space"){
        event.preventDefault();
    }
    if (ignore_letters.includes(key)) {
        return
    }
    if (key == 'Alt') {
        backAWord = true;
        return
    }
    if (key == 'Backspace') {
        BackSpace()
        if (backAWord) {
            while (sentence[letterUpTo] != ' ' || letterUpTo != 0) {
                BackSpace()
            }
        }
        return

    }
    backAWord = false;
    if (key == sentence[letterUpTo]) {
        allSpans.eq(letterUpTo).css({
            "color": "green",
            "background-color": "lightgreen",
        })
    } else {
        allSpans.eq(letterUpTo).css({
            "color": "red",
            "background-color": "orange",
        })
    }

    letterUpTo++

    wpmCalc()

    wpmInterval = setInterval(wpmCalc, 3000)

    if (letterUpTo == sentence.length){
        LoadNextLevel()
    }
})

function setSpans() {
    //clear .text
    text.text("")
    sentence.split('').forEach(letter =>{
        text.append($('<span></span>').text(letter))
        }    
    );
    allSpans = $('span');
}
