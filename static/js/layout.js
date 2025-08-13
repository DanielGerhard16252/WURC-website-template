const MESSAGE_TIMEOUT = 5000;

window.setTimeout(function() {
    // we make the flash mesage disappear after 5 seconds
    hideAlerts();
}, MESSAGE_TIMEOUT);


/**
 * Make the alert boxes fade out
 */
function hideAlerts() {
    let alerts = document.getElementsByClassName('alert-box');
    for (let i = 0; i < alerts.length; i++) {
        alerts[i].style.opacity = 0;
    }
}

window.addEventListener("scroll", function () {
    const header = document.querySelector("header");
    if (window.scrollY > 0) {
        header.classList.add("scrolled");
    } else {
        header.classList.remove("scrolled");
    }
});

document.addEventListener("DOMContentLoaded", function () {
  const track = document.querySelector(".gallery-track");
  const slides = document.querySelectorAll(".gallery-track img");
  const prevBtn = document.querySelector(".gallery-button.prev");
  const nextBtn = document.querySelector(".gallery-button.next");

  let index = 0;

  function updateSlide() {
    const slideWidth = slides[0].clientWidth;
    track.style.transform = `translateX(-${index * slideWidth}px)`;
  }

  nextBtn.addEventListener("click", () => {
    index = (index + 1) % slides.length;
    updateSlide();
  });

  prevBtn.addEventListener("click", () => {
    index = (index - 1 + slides.length) % slides.length;
    updateSlide();
  });

  window.addEventListener("resize", updateSlide);
});