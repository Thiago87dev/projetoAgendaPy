const btnDelete = document.querySelector('[data-js="btn-delete"]')
const formDelete = document.querySelector('[data-js="form-delete"]')

btnDelete.addEventListener('click', ()=>{
    Swal.fire({
        title: "Are you sure?",
        text: "You won't be able to revert this!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#d33",
        cancelButtonColor: "#3085d6",
        confirmButtonText: "Yes, delete it!"
    }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire({
                title: "Deleted!",
                text: "Contact deleted.",
                icon: "success"
            }).then(()=>{
                formDelete.submit();
            })
           
           
        }
    });
})

