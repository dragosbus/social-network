const View = (function() {

  function init() {
    const form = document.querySelector('form');
    form.addEventListener('submit', formEventHandler);
  }

  function formEventHandler(e) {
    e.preventDefault();
    console.log(e.target);
  }

  return {init};

}());

// View.init();
