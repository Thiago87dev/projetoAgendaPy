const btnDelete = document.querySelector('[data-js="btn-delete"]');
const btnCreateUpdate = document.querySelector('[data-js="btn-create-update"]');
const formDelete = document.querySelector('[data-js="form-delete"]');
const formCreateUpdate = document.querySelector(
  '[data-js="form-create-update"]'
);

if (btnDelete) {
  btnDelete.addEventListener("click", () => {
    Swal.fire({
      title: "Are you sure?",
      text: "You won't be able to revert this!",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#d33",
      cancelButtonColor: "#3085d6",
      confirmButtonText: "Yes, delete it!",
    }).then((result) => {
      if (result.isConfirmed) {
        Swal.fire({
          title: "Deleted!",
          text: "Contact deleted.",
          icon: "success",
        }).then(() => {
          formDelete.submit();
        });
      }
    });
  });
}

if (btnCreateUpdate) {
  btnCreateUpdate.addEventListener("click", async () => {
    const formData = new FormData(formCreateUpdate);
    const response = await fetch(formCreateUpdate.action, {
      method: "POST",
      body: formData,
      headers: {
        "X-CSRFToken": formCreateUpdate.querySelector(
          "[name=csrfmiddlewaretoken]"
        ).value,
        "X-Requested-With": "XMLHttpRequest",
      },
    });
    const data = await response.json();

    document.querySelectorAll('.error-message').forEach(el => el.remove());

    if (data.status === "success") {
      Swal.fire({
        title: "Success!",
        text: "Contact saved successfully.",
        icon: "success",
      }).then(() => {
        window.location.href = `/contact/${data.contact_id}/`;
      });
    } else {
      for (const [field, errors] of Object.entries(data.errors)) {
        const fieldElement = formCreateUpdate.querySelector(`[name=${field}]`);
        fieldElement.classList.add("input-error")
        if (fieldElement) {
          const errorDiv = document.createElement("div");
          errorDiv.classList.add("error-message");
          errorDiv.style.color = "red";
          errorDiv.innerHTML = errors.join("<br>");
          fieldElement.parentElement.appendChild(errorDiv);
        }
      }

      Swal.fire({
        title: "Error!",
        text: "There was an error saving the contact.",
        icon: "error",
      });
    }
    // Swal.fire({
    //     title: "Done!",
    //     // text: "Contact updated/created successfully!",
    //     icon: "success"
    //   }).then(()=>{
    //     formCreateUpdate.submit();
    // })
  });
}
