const App = (function() {

  let model = {
    username: '',
    user_email: '',
    user_password: '',
    repeat_password: ''
  };

  function init() {
    const form = document.querySelector('form');
    form.addEventListener('submit', formEventHandler);
    inputOnChange();
  }

  function formEventHandler(e) {
    e.preventDefault();
    if (e.target.classList.contains('register'))
      registerHandler();
    }

  function registerHandler() {
    let {username, user_email, user_password, repeat_password} = model;

  }

  function inputOnChange() {
    const username = document.getElementById('username');
    const user_email = document.getElementById('user_email');
    const user_pass = document.getElementById('user_password');
    const repeat_pass = document.getElementById('repeat_password');

    let inputs = [username, user_email, user_pass, repeat_pass];
    inputs.forEach(input => {
      input.addEventListener('input', e => {
        setModelProp(e.target, 'username');
        setModelProp(e.target, 'user_email');
        setModelProp(e.target, 'user_password');
        setModelProp(e.target, 'repeat_password');
        setBorderColor(e.target);
        let {username, user_email, user_password, repeat_password} = model;
        //check if all inputs are not empty then check if passwords match
        if (!username || !user_email || !user_password || !repeat_password) {
          document.getElementById('register-btn').disabled = true;
        } else {
          if (user_password !== repeat_password) {
            document.getElementById('register-btn').disabled = true;
            document.querySelector('.not-match').classList.remove('hide');
          } else {
            document.getElementById('register-btn').disabled = false;
            document.querySelector('.not-match').classList.add('hide');
          }
        }
      }); //end change event listener
    }); //end forEach
  }

  function setModelProp(target, prop) {
    if(target.id === prop) model[prop] = target.value
  }

  function setBorderColor(target) {
    if(target.value) target.style.border = '2px solid #3ac162';
    else target.style.border = '2px solid #f21541';
  }

  return {init};

}());

App.init();
