function hideCode() {
    setTimeout(() => {
        location.replace('/receive?color=' + color);
    }, 500);
}

let form = document.getElementById('form');
form.addEventListener('submit', (e) => {
    e.preventDefault();
    form.submit();
    hideCode();
});

const params = new URLSearchParams(window.location.search);
console.log(params);

if(params.has('code')) {
    const code = params.get('code');
    document.getElementById('codenum').value = parseInt(code);
    form.submit();
    hideCode();
}