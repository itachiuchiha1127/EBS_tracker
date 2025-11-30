@
document.addEventListener("DOMContentLoaded", function() {
    const menuToggle = document.getElementById("menu-toggle");
    if(menuToggle){
        menuToggle.addEventListener("click", function(e) {
            e.preventDefault();
            document.body.classList.toggle("toggled");
        });
    }
    
    const dateInput = document.getElementById("txDate");
    if(dateInput && !dateInput.value) {
        dateInput.valueAsDate = new Date();
    }
});
@
