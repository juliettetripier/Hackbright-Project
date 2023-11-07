const hatSelectButtons = document.querySelectorAll('.hat-option');
const eggPicture = document.querySelector('#egg-mascot-edit-page');
const oldHat = document.querySelector('#egg-mascot-edit-page').id;
const saveButton = document.querySelector('#save-hat-button');
let newHat = oldHat;


function showHatOption(evt) {
    let hatSelection = evt.target.id;
    newHat = hatSelection;
    eggPicture.src = `/static/img/egg-${hatSelection}.PNG`;
}

function saveHatOption() {
    const formInputs = {
        newHat: newHat,
    };
    console.log(newHat);

    fetch('/updatehat', {
        method: 'POST',
        body: JSON.stringify(formInputs),
        headers: {
          'Content-Type': 'application/json',
        }
    })
        .then((response) => response.json())
        .then((responsejson) => {
            console.log(responsejson['code'])
            alert('Hat successfully updated!')
        })
}


hatSelectButtons.forEach(function(item) {
    item.addEventListener('click', showHatOption)
})

saveButton.addEventListener('click', saveHatOption)