async function detectDisease() {
    const fileInput = document.getElementById("imageInput");
    const file = fileInput.files[0];

    const formData = new FormData();
    formData.append("file", file);

    const result = await postData("/api/detect/disease", formData);

    document.getElementById("result").innerHTML = `
        <h2>${result.disease}</h2>
        <p>Confidence: ${result.confidence}</p>
    `;

    Swal.fire("Detection Complete!", "", "success");
}