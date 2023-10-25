const addVisitButton = document.querySelector('#visit-button');
const removeVisitButton = document.querySelector('#unvisit-button');

const addToListButton = document.querySelector('#add-to-list-button');

const addTagButton = document.querySelector('#add-tag-button');


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

function addToList() {
    const formInputs = {
        listid: document.querySelector('#which-list').value,
        restaurantid: document.querySelector('#visit-button').value
    };

    fetch('/addtolist', {
        method: 'POST',
        body: JSON.stringify(formInputs),
        headers: {
          'Content-Type': 'application/json',
        }
    })
        .then((response) => response.json())
        .then((responsejson) => {
            alert(responsejson['code']);
        })
}

function addTag() {
    const formInputs = {
        tagid: document.querySelector('#which-tag').value,
        restaurantid: document.querySelector('#visit-button').value
    };

    fetch('/addtag', {
        method: 'POST',
        body: JSON.stringify(formInputs),
        headers: {
          'Content-Type': 'application/json',
        }
    })
        .then((response) => response.json())
        .then((responsejson) => {
            console.log(responsejson)
            alert(responsejson['code']);
            const allTags = document.querySelectorAll('.displayed-tag')
            console.log(allTags)
            for (let i=0; i < allTags.length; i++) {
                console.log(allTags[i])
                if (allTags[i].value == responsejson['tag_id']) {
                    allTags[i].style.display = 'none';
                }
            }
            document.querySelector('#which-tag').selectedIndex = 0
        })
}

addVisitButton.addEventListener('click', addVisit);
removeVisitButton.addEventListener('click', removeVisit);
addToListButton.addEventListener('click', addToList);
addTagButton.addEventListener('click', addTag);
