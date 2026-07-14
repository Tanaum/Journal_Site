//VARIABLES

//TO TAKE THE CONTENT FROM THE USER
var diaryEntry = $('.diaryEntry');
var diaryEntryButton = $('.diaryEntryButton');
var prvEntries = $('.prvEntries');
var editBtn = $('.editBtn');

//TO TAKE THE CONTENT FROM THE USER
diaryEntryButton.on("click", ()=>{
    //DATE
    var d = new Date()
    var date = d.getDate();
    var month = d.getMonth()+1;
    var year = d.getFullYear();

    if (diaryEntry.val() !== ""){
        // using POST
        $.ajax({
            url: 'http://localhost:5000/api/save-entry', // your Flask endpoint
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ 
                TimeInMilli: Date.now(),
                Date: `${date}/${month}/${year}`,
                Entry: diaryEntry.val()
            }),
            success: function(response) {
                console.log("Update success:", response);
                diaryEntry.val(''); // Clear the textarea after submission
            },
            error: function(xhr, status, error) {
                console.error("PUT error:", error);
            }
        });
    }
});

// On document ready, only display entries if the container exists (PrvEnt.html)
$(document).ready(()=>{
    $.ajax({
    url: 'http://localhost:5000/api/get-entries', // ✅ now it targets the actual API
    method: 'GET',
    success: function(data) {
        for (let i=0; i<data.length; i++){
            console.log(data[i])

            var entryHTML = `
            <div class="diaryentryBox" id=${data[i].TimeInMilli}>
                <p><strong>${data[i].Date}:</strong></p>
                <p>${data[i].Entry}</p>
            </div>
            `;
            prvEntries.append(entryHTML);
        }
    },
    error: function(xhr, status, error) {
        console.error("AJAX error:", error);
    }
    });
});

// Editing an entry
// editBtn.on("click", ()=>{
//     alert("btn workss")
// });