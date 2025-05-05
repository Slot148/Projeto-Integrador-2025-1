document.addEventListener('DOMContentLoaded', function() {
    const radioButtons = document.querySelectorAll('input[name="tipouser"]');
    const formAluno = document.getElementById('formAluno');
    const formAdm = document.getElementById('formAdm');
    const tipoAluno = document.getElementById('tipoAluno');
    const tipoAdmin = document.getElementById('tipoAdmin');
    
    radioButtons.forEach(radio => {
        radio.addEventListener('change', function() {
          if (this.value === 'aluno') {
            formAluno.classList.remove('none');
            formAdm.classList.add('none');
            tipoAluno.value = 'aluno';
          } else if (this.value === 'administrador') {
            formAluno.classList.add('none');
            formAdm.classList.remove('none');
            tipoAdmin.value = 'administrador';
          }
        });
      });

    const checkedRadio = document.querySelector('input[name="tipouser"]:checked');
    if (checkedRadio) {
      tipoAluno.value = checkedRadio.value;
      tipoAdmin.value = checkedRadio.value;
    }
  });