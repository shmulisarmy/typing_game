function progressSnapShot(){
    progress.push(letterUpTo)
}

function toggleNightMode(){
    $('body').toggleClass('night-mode')
    background_color = $('body').hasClass('night-mode') ? 'black' : 'white';
}

function offerSetneceGenerationService(){
    const sortedLetterTimes = Object.entries(letterTimes).sort((a, b) => b[1] - a[1]).slice(0, 5);
    const topFiveLetters = sortedLetterTimes.map(([key]) => key).join('');
    const mostCommonLetter = topFiveLetters[0];
    if (prompt(`it seems as though you have lots of trouble typing out '${mostCommonLetter}',  
    would you like to generate a new custom sentence made to help you work on all the 
    letters that you struggle with?`) == "yes") {
        $.ajax({
            type: "GET",
            url:   `/api/generateSentence/${topFiveLetters}`,
            async: false, 
            data: {
                levelUpTo: levelUpTo,
                wpm: wpm
            },
            success: function(response) {
                alert(response.message);
                if (response["didGnereatedSentence"] == false) {
                    return
                }
                sentence = response["sentence"];
                usingGeneratedSentence = true
            },
            error: function(xhr, status, error) {
                console.error(xhr.responseText);
            }
        });
    } 
    if (!usingGeneratedSentence) {
        LoadNextLevel()
    } 
    reset()

}


function LoadNextLevel(){
    console.log("levelUpTo", levelUpTo)
    $.ajax({
        type: "GET",
        url:   `/loadNextLevel/${levelUpTo}`,
        async: false, 
        data: {
            wpm: wpm
        },
        success: function(response) {
            sentence = response["sentence"];
            levelUpTo = parseInt(response["level"]);
        },
        error: function(xhr, status, error) {
            console.error(xhr.responseText);
        }
    });

}

function reset(){
    wpm = 0;
    correct_letters_typed = 0;
    clearInterval(wpmInterval)
    $wpm.text("next level loaded");
    if (usingGeneratedSentence == true) {
        $('#levelDisplay').text(`ai generated sentence`)
    } else {
        $('#levelDisplay').text(`Level: ${levelUpTo}`)
    }
    letterUpTo = 0
    wpmData = []
    startTime = false
    setSpans();
}

function BackSpace() {
    // modifier
    letterUpTo--
    if (allSpans.eq(letterUpTo).hasClass('correct')) {
        correct_letters_typed--
        allSpans.eq(letterUpTo).removeClass('correct')
    }
    allSpans.eq(letterUpTo).css({
        "color": "var(--text-color)",
        "background-color": "transparent",
    })
}
function wpmCalc() {
    if (!startTime) {
        startTime = Date.now()
        wpmInterval = setInterval(wpmCalc, 300)

        return
    }
    timeSinceStart = Date.now() - startTime
    wpm = Math.round(correct_letters_typed / (timeSinceStart / 1000 / 12))
    $wpm.text(`wpm: ${wpm}`)
}

function setSpans() {
    //clear .text
    text.text("")
    sentence.split('').forEach(letter =>{
        text.append($('<span></span>').text(letter))
        }    
    );
    allSpans = $('span');
}



const text = $('.text')
let letterUpTo = 0;
let wpmData = [];
let correct_letters_typed = 0;
let key, startTime, timeSinceStart, wpm, backAWord, allSpans, wpmInterval, usingGeneratedSentence;
let levelUpTo = parseInt($('#levelDisplay').text().split(" ")[1])
const ignore_letters = ["Command", "Shift"]
const $wpm = $('.wpm')
let progress = [];
let background_color = "black"

const letterTimes = {}

setSpans();

window.addEventListener("keydown", event => {
    key = event.key
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
        update_accuracy()
        return

    }
    backAWord = false;
    if (key == sentence[letterUpTo]) {
        correct_letters_typed += 1
        allSpans.eq(letterUpTo).css({
            "color": "green",
            "background-color": "lightgreen",
        })
        allSpans.eq(letterUpTo).addClass('correct')
    } else {
        if (!letterTimes[sentence[letterUpTo]]) {
            letterTimes[sentence[letterUpTo]] = 0
        }
        letterTimes[sentence[letterUpTo]] += 1
        allSpans.eq(letterUpTo).css({
            "color": "red",
            "background-color": "orange",
        })
    }

    letterUpTo++

    wpmCalc()
    update_accuracy()


    if (letterUpTo == sentence.length){
        //end of level
        if (usingGeneratedSentence) {
            //escape usingGeneratedSentence mode and back into level mode
            usingGeneratedSentence = false
            LoadNextLevel()
            reset()
        } else {
            offerSetneceGenerationService()
        }
    }
})


function accuracy_persentage(){
    const accuracy = correct_letters_typed / letterUpTo
    return Math.round(accuracy * 100)
}

function update_accuracy(){
    $('#accuracy').text(`accuracy: ${accuracy_persentage()}%`)
}




var canvas = document.getElementById('graph');
        var ctx = canvas.getContext('2d');

        var graphWidth = canvas.width - 40; 
        var graphHeight = canvas.height - 40;
        var barSpacing = 5;
    
        function drawGraph(data) {
            var barWidth = (graphWidth - (data.length - 1) * barSpacing) / data.length;
            var maxValue = Math.max(...data);
    
            ctx.clearRect(0, 0, canvas.width, canvas.height);
    
            // Draw each bar
            data.forEach(function(value, index) {
                var barHeight = (value / maxValue) * graphHeight;
                var x = (index * (barWidth + barSpacing)) + 20;
                var y = graphHeight - barHeight + 40;
    
                ctx.fillStyle = 'blue';
                ctx.fillRect(x, y, barWidth, barHeight);
    
                ctx.fillStyle = background_color;
                ctx.font = '0px Arial';
                ctx.fillText(index + 1, x + barWidth / 2, graphHeight + 30);
            });
        }
    
        setInterval(() => {
            if (wpm && !wpm == 0){
                wpmData.push(wpm)
                drawGraph(wpmData);
            }
        }, 1000)