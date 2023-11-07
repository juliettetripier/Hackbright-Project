const hatSelectButtons = document.querySelectorAll('.hat-option');
const eggPicture = document.querySelector('#egg-mascot-edit-page');
const saveButton = document.querySelector('#back-to-profile-button');
let newHat = 'basic';


function showHatOption(evt) {
    let hatSelection = evt.target.id;
    newHat = hatSelection;
    eggPicture.src = `/static/img/egg-${hatSelection}.PNG`;
}

function saveHatOption() {
    const formInputs = {
        newHat: newHat,
    };

    fetch('/updatehat', {
        method: 'POST',
        body: JSON.stringify(formInputs),
        headers: {
          'Content-Type': 'application/json',
        }
    })
        .then((response) => response.json())
        .then(responsejson => {
            console.log('Success')
        })
}


hatSelectButtons.forEach(function(item) {
    item.addEventListener('click', showHatOption)
})

saveButton.addEventListener('click', saveHatOption)