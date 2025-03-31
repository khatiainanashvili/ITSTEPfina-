const userDropdown = document.querySelectorAll('.dropdown');
const userHeandler = document.querySelector('.dropdown-menu');

userDropdown.forEach(element => {

element.addEventListener('click', ()=>{
    userHeandler.classList.toggle('active')
    console.log("works");
   
}
)

});
