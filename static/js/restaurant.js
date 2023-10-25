const addVisitButton = document.querySelector('#visit-button');
const removeVisitButton = document.querySelector('#unvisit-button');
const addToListButton = document.querySelector('#add-to-list-button');
const addTagButton = document.querySelector('#add-tag-button');
const removeTagButton = document.querySelector('#delete-tags-button');
const addedTags = document.querySelector('#added-tags-div');


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
            const allTags = document.querySelectorAll('.displayed-tag');
            for (let i=0; i < allTags.length; i++) {
                if (allTags[i].value == responsejson['tag_id']) {
                    allTags[i].style.display = 'none';
                }
            }
            document.querySelector('#which-tag').selectedIndex = 0;
            if (responsejson['code'] == 'Tag successfully added!') {
                let tagCheckbox = `<input type='checkbox' id= ${responsejson['tag_id']} name='tag_id' value=${responsejson['tag_id']}>`;
                let tagLabel = `<label for=${responsejson['tag_id']}> ${responsejson['tag_name']} </label>`;
                addedTags.insertAdjacentHTML('beforeend', tagCheckbox);
                addedTags.insertAdjacentHTML('beforeend', tagLabel);
                addedTags.insertAdjacentHTML('beforeend', '<br/>');
                removeTagButton.style.display = "inline";
            } else {
                alert(responsejson['code'])
            }
        })
}

addVisitButton.addEventListener('click', addVisit);
removeVisitButton.addEventListener('click', removeVisit);
addToListButton.addEventListener('click', addToList);
addTagButton.addEventListener('click', addTag);
