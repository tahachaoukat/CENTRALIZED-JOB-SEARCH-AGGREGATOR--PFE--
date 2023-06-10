

// run swal
let pass1= document.querySelector("#pass1");
let pass2= document.querySelector("#pass2");
let btn = document.querySelector("#btn");
let form= document.forms;

btn.onclick=(e)=>{
    e.preventDefault();
    let test=pass1.value===pass2.value;
    if(test){
        Swal.fire({
            position: 'center',
            icon: 'success',
            title: 'Votre Compte est crée avec succés',
            showConfirmButton: false,
            timer: 1500
          })
         setTimeout(()=>{
             form[0].submit();

         },2500) 
         
    }else{
        Swal.fire({
            position: 'center',
            icon: 'error',
            title: 'Mot de passe Invalide Veuillez Confirmer !',
            showConfirmButton: false,
            timer: 1500
          })   
     
    }


}



