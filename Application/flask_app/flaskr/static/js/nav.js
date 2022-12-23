// Get modal

let modal = document.getElementById("simpleModal");

// Get result box

let result = document.getElementById("result");

// Get button to open modal

let btn = document.getElementById("modalBtn");

// Get button to close modal

let closeBtn = document.getElementsByClassName("closeBtn")[0];

// Get button to make predictions

let predictBtn = document.getElementsByClassName("submit")[0];

let card = document.getElementsByClassName("card")[0];

let another = document.getElementById("another");

btn.onclick = function () {
  modal.style.display = "block";
  result.style.display = "none";
};

closeBtn.onclick = function () {
  modal.style.display = "none";
};

another.onclick = function () {
  result.style.display = "none";
  card.style.display = "block";
};

function showresult() {
  let resultData = document.getElementById("result-p").innerHTML;
  if (!resultData.includes("$0.00")) {
    result.style.display = "block";
    card.style.display = "none";
  }
}

window.onclick = function (event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
};

let flash = document.getElementsByClassName("flash")[0];

window.setTimeout(function () {
  flash.fadeTo(500, 0);
}, 4000);

showresult();
