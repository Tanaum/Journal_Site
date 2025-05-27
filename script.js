//VARIABLES
var diaryEntry = $('.diaryEntry');
var diaryEntryButton = $('.diaryEntryButton');

//const keys = [-1]; idt imma need this later now lawlz


// EVENT LISTNER
diaryEntryButton.on("click", testButton);

//FUNCTION
function testButton(){
    //DATE
    var d = new Date()
    var date = d.getDate();
    var month = d.getMonth()+1;
    var year = d.getFullYear();

    var entryIndex = localStorage.getItem("entryIndex") || 0;

    //
    const diaryPage = {
        todaysDate : `${date}/${month}/${year}`,
        diaryContent : diaryEntry.val()
    };

    localStorage.setItem("entryIndex", Number(entryIndex)+1);
    localStorage.setItem(`${Date.now()}`,JSON.stringify(diaryPage));
};