var button = document.querySelector('#submit-btn');

button.addEventListener('click', function(){
    document.getElementById('submit-btn').innerText = 'Loading.....';

    Changegreeting1();
    function Changegreeting1(){
        document.getElementById('submit-btn').innerHTML = 'Still Loading';
        document.getElementById('submit-btn').style.opacity = 0;
        document.getElementById('submit-btn').style.opacity = 1;
        setTimeout(Changegreeting, 2000);
      }
    function Changegreeting(){
        document.getElementById('submit-btn').innerHTML = '';
        document.getElementById('submit-btn').style.opacity = 1;
        document.getElementById('submit-btn').style.opacity = 0;
        setTimeout(Changegreeting1, 2000);
      }
});