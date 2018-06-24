const App = (function() {

  let model = {username:'', user_email:'', user_pass:'', repeat_pass:''};

  function init() {
    const form = document.querySelector('form');
    form.addEventListener('submit', formEventHandler);
    inputOnChange();
  }

  function formEventHandler(e) {
    e.preventDefault();
    if(e.target.classList.contains('register')) registerHandler();
  }

  function registerHandler() {
    let username = document.getElementById('username').value;
    let user_email = document.getElementById('user-email').value;
    let user_pass = document.getElementById('user-password').value;
    let repeat_pass = document.getElementById('repeat-password').value;

    model = {username, user_email, user_pass, repeat_pass};
    console.log(model);
  }

  function inputOnChange() {
    const username = document.getElementById('username');
    const user_email = document.getElementById('user-email');
    const user_pass = document.getElementById('user-password');
    const repeat_pass = document.getElementById('repeat-password');

    let inputs = [username, user_email, user_pass, repeat_pass];
    inputs.forEach(input=>{
      input.addEventListener('change', e=>{
        if(e.target.id === 'username') model.username = e.target.value;
        else if(e.target.id === 'user-email') model.user_email = e.target.value;
        else if (e.target.id === 'user-password') model.user_pass = e.target.value;
        else if (e.target.id === 'repeat-password') model.repeat_pass = e.target.value;

        let {username, user_email, user_pass, repeat_pass} = model;
        if(username && user_email && user_pass && repeat_pass) {
          document.getElementById('register-btn').disabled = false;
        }
      });
    });
  }

  return {init};

}());

App.init();
