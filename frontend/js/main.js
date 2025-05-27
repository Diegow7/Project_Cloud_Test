const toggleThemeBtn = document.getElementById('toggle-theme');
const body = document.body;

toggleThemeBtn.addEventListener('click', () => {
  body.classList.toggle('dark-mode');
  const icon = toggleThemeBtn.querySelector('i');
  if (body.classList.contains('dark-mode')) {
    icon.classList.replace('fa-moon', 'fa-sun');
  } else {
    icon.classList.replace('fa-sun', 'fa-moon');
  }
});

document.getElementById('query-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const query = document.getElementById('query').value;

  const chatBox = document.getElementById('chat-box');
  const userMessage = `
    <div class="message user">
      <div class="icon"><i class="fa fa-user"></i></div>
      <div class="message-content">${query}</div>
    </div>
  `;
  chatBox.innerHTML += userMessage;

  //Redireccionando al backend de AWS, evitando el local host
  const response = await fetch('http://127.0.0.1:5000/query', {
  //const response = await fetch('http://98.81.245.169:5000/query', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query })
  });
  const result = await response.json();

  const botMessage = `
    <div class="message bot">
      <div class="icon"><i class="fa fa-robot"></i></div>
      <div class="message-content">${result.response}</div>
    </div>
  `;
  chatBox.innerHTML += botMessage;
  chatBox.scrollTop = chatBox.scrollHeight;
  document.getElementById('query').value = '';
});