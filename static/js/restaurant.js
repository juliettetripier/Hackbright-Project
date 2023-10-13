const addVisitButton = document.querySelector('#visit-button');
const removeVisitButton = document.querySelector('#unvisit-button');

function addVisit() {

    const formInputs = {
        restaurantid: document.querySelector('#visit-button').value
    };

    fetch('/addvisit', {
        method: 'POST',
        body: JSON.stringify(formInputs),
        headers: {
          'Content-Type': 'application/json',
        }
    })
        .then((response) => response.json())
        .then((responsejson) => {
            // this is where we will enable/disable buttons once add visit button works
            alert(responsejson['code']);
       
            addVisitButton.style.display = "none";
            removeVisitButton.style.display = "inline";
        });
}

function removeVisit() {

    const formInputs = {
        restaurantid: document.querySelector('#unvisit-button').value
    };

    fetch('/removevisit', {
        method: 'POST',
        body: JSON.stringify(formInputs),
        headers: {
          'Content-Type': 'application/json',
        }
    })
        .then((response) => response.json())
        .then((responsejson) => {
            alert(responsejson['code']);
            addVisitButton.style.display = "inline";
            removeVisitButton.style.display = "none";
        })
}

addVisitButton.addEventListener('click', addVisit);
removeVisitButton.addEventListener('click', removeVisit);
