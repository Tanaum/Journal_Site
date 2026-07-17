//VARIABLES

//TO TAKE THE CONTENT FROM THE USER
var diaryEntry = $('.diaryEntry');
var diaryEntryButton = $('.diaryEntryButton');
var prvEntries = $('.prvEntries');
var usernameEntry = $('.usernameEntry');
var passwordEntry = $('.passwordEntry');
var signUpButton = $('.signUpButton');
var logInButton = $('.logInButton');
const UUID = getCookie("userID");

// SIGN UP
signUpButton.on("click", ()=>{
   if (passwordEntry.val() !== "" && usernameEntry.val() !== ""){
    $.ajax({
        url:'http://localhost:5000/sign-up',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            username: usernameEntry.val(),
            password: passwordEntry.val()
        }),
        success: function(response) {
                console.log("Update success:", response);
            },
        error: function(xhr, status, error) {
                alert(xhr.responseJSON.Message);
                console.error("PUT error:", error);
            }
    })
   } 
})

// LOG IN
logInButton.on("click",()=>{
    if (passwordEntry.val() !== "" && usernameEntry.val() !== ""){
    $.ajax({
        url:'http://localhost:5000/log-in',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            username: usernameEntry.val(),
            password: passwordEntry.val()
        }),
        success: function(response) {
                console.log("Update success:", response);
                document.cookie = "userID=" + response["User ID"];
                console.log(document.cookie);
            },
        error: function(xhr, status, error) {
                alert(xhr.responseJSON.Message);
                console.error("PUT error:", error);
            }
    })
   } 
})

// FUNCTION TO GET UUID FROM COOKIE
function getCookie(cname) {
  let name = cname + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(';');
  for(let i = 0; i <ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

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
            url: 'http://localhost:5000/api/save-entry/', // your Flask endpoint
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ 
                TimeInMilli: Date.now(),
                Date: `${date}/${month}/${year}`,
                Entry: diaryEntry.val(),
                userID: UUID
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
    url: 'http://localhost:5000/api/get-entries/'+UUID, // ✅ now it targets the actual API
    method: 'GET',
    success: function(data) {
        for (let i=0; i<data.length; i++){
            console.log(data[i])

            var entryHTML = `
            <div class="diaryentryBox">
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
