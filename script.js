//VARIABLES

//TO TAKE THE CONTENT FROM THE USER
var diaryEntry = $('.diaryEntry');
var diaryEntryButton = $('.diaryEntryButton');

var prvEntries = $('.prvEntries');

//stores all of the keys so that they can be arranged
const timestampKeys = [];

// EVENT LISTNER

//TO TAKE THE CONTENT FROM THE USER
diaryEntryButton.on("click", saveDiaryContent);

// On document ready, only display entries if the container exists (PrvEnt.html)
$(document).ready(function() {
    if (prvEntries.length) {
        displayPreviousEntries();
    }
});

//FUNCTIONS

//SAVING CONTENT GIVEN BY THE USER
function saveDiaryContent(){
    //DATE
    var d = new Date()
    var date = d.getDate();
    var month = d.getMonth()+1;
    var year = d.getFullYear();

    //DIARY PAGE OBJECT
    const diaryPage = {
        todaysDate : `${date}/${month}/${year}`,
        diaryContent : diaryEntry.val()
    };

    if (diaryPage.diaryContent !== ""){
        localStorage.setItem(`${Date.now()}`,JSON.stringify(diaryPage));
    }

    diaryEntry.val(''); // Clear the textarea after submission
};

function displayPreviousEntries(){
    for (let i = 0; i < localStorage.length; i++) {
        let key = localStorage.key(i);
        timestampKeys.push(Number(key));
    }

    // Sort keys descending (newest to oldest)
    timestampKeys.sort((a, b) => b-a);

    // Now loop through in order
    timestampKeys.forEach(keyNum => {
        let diaryEntry = JSON.parse(localStorage.getItem(keyNum.toString()));
        
        var entryHTML = `
            <div class="diaryentryBox">
                <p><strong>${diaryEntry.todaysDate}:</strong></p>
                <p>${diaryEntry.diaryContent}</p>
            </div>
        `;

        prvEntries.append(entryHTML);
    });
}