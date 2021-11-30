const allSkillElements = document.querySelectorAll('.grid-container p');

const skillInput = document.querySelector('#skills-tree');

const careerPathInput = document.querySelector('#career-path');

const submitButton = document.querySelector('.btn-submit-custom');

const emptyErrorMessage = document.querySelector('.empty-error-message');

const skillInputList = [];

const mainContent = document.querySelector('.main-content');
const loaderWrapper = document.querySelector('.initial-loader-wrapper');
const outerLoader = document.querySelector('.outer-loader');
const innerLoader = document.querySelector('.inner-loader');

// skill bubble chip event listener logic
allSkillElements.forEach(function (e) {
  e.addEventListener('click', function () {
    if (e.classList.length == 1) {
      e.classList.remove('clicked');
      const targetIndex = skillInputList.indexOf(e.textContent);
      skillInputList.splice(targetIndex, 1);
      if (skillInputList.length == 0) {
        skillInput.value = '';
      } else {
        skillInput.value = skillInputList.join(', ') + ', ';
        console.log(skillInputList);
        console.log(skillInput.value);
      }
    } else {
      e.classList.add('clicked');
      skillInput.value += `${e.textContent}, `;
      skillInputList.push(e.textContent);
      console.log(skillInputList);
      console.log(skillInput.value);
    }
  });
});

// final submit button eventListener logic: prevent form-data submit if all required field are empty
submitButton.addEventListener('click', function () {
  careerPathInput.value = careerPathInput.value.toLowerCase();
  if (skillInput.value == '') {
    submitButton.setAttribute('type', 'button');
    emptyErrorMessage.classList.add('show');
    console.log('empty');
  } else {
    emptyErrorMessage.classList.remove('show');
    submitButton.setAttribute('type', 'submit');
    mainContent.classList.add('.main-content-hidden');
    loaderWrapper.classList.add('loader-wrapper');
    outerLoader.classList.add('loader');
    innerLoader.classList.add('loader-inner');
  }
});
