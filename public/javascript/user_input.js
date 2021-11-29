const allSkillElements = document.querySelectorAll(".grid-container p");

const skillInput = document.querySelector("#skills-tree");

const careerPathInput = document.querySelector("#career-path");

const submitButton = document.querySelector(".btn-submit-custom");

const emptyErrorMessage = document.querySelector(".empty-error-message");

const skillInputList = [];

// skill bubble chip event listener logic
allSkillElements.forEach(function (e) {
  e.addEventListener("click", function () {
    if (e.classList.length == 1) {
      e.classList.remove("clicked");
      const targetIndex = skillInputList.indexOf(e.textContent);
      skillInputList.splice(targetIndex, 1);
      if (skillInputList.length == 0) {
        skillInput.value = "";
      } else {
        skillInput.value = skillInputList.join(", ") + ", ";
        console.log(skillInputList);
        console.log(skillInput.value);
      }
    } else {
      e.classList.add("clicked");
      skillInput.value += `${e.textContent}, `;
      skillInputList.push(e.textContent);
      console.log(skillInputList);
      console.log(skillInput.value);
    }
  });
});

// final submit button eventListener logic: prevent form-data submit if all required field are empty
submitButton.addEventListener("click", function () {
  careerPathInput.value = careerPathInput.value.toLowerCase();
  if (skillInput.value == "") {
    submitButton.setAttribute("type", "button");
    emptyErrorMessage.classList.add("show");
    console.log("empty");
  } else {
    emptyErrorMessage.classList.remove("show");
    submitButton.setAttribute("type", "submit");
  }
});

// const initiallist = [];
// initiallist.push(...["111", "222", "33"]);

// console.log(initiallist);

// console.log(initiallist.join(", "));

// const targetString = "1, 2, ccc, cbbb, 3, 4, kkk, ";
// const trims = targetString.slice(0, targetString.length - 2);

// console.log(trims);

// const targetStringList = trims.split(", ");

// console.log(targetStringList);

// const targetindex = targetStringList.indexOf("cbbb");

// console.log(targetindex);

// targetStringList.splice(targetindex, 1);

// console.log(targetStringList);
