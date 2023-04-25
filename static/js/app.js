'use strict';

const state = {
 oldKey: [],
 oldData: [],
 data,
 username,
};

const table = document.querySelector('.data-table');
const tableContent = document.querySelector('.data-table-content');

const loadData = function (old = false) {
 let current;
 if (old) {
  current = state.data;
 } else {
  if (state.oldData.length === 0) return;
  state.oldKey.pop();
  current = state.oldData.pop();
  state.data = current;
 }

 tableContent.innerHTML = '';
 let markup = '';
 Object.keys(current).forEach((key) => {
  let type = current[key].type === 'dir' ? 'dir' : 'file';
  if (type === 'file') {
   if (current[key].type === 'txt') {
    type = 'txt';
   }
  }
  markup += `
    <div class="data-table--item ${type}" data-type="${type}">
      <p class="name">${key}</p>
      <p>${current[key].mtime}</p>
      <p>${current[key].size}</p>
    </div>
  `;
 });
 tableContent.insertAdjacentHTML('beforeend', markup);
};

window.addEventListener('load', loadData);

tableContent.addEventListener('click', async function (e) {
 const item = e.target.closest('div');
 if (item) {
  const key = item.firstElementChild.innerHTML;
  if (item.dataset.type === 'dir') {
   state.oldData.push(state.data);
   state.oldKey.push(key);
   state.data = state.data[key]['data'];
   loadData(key);
  } else if (item.dataset.type === 'txt') {
   console.log();
   const path_param =
    state.oldKey.length === 0
     ? `/readfile/home/${state.username}/${key}`
     : `/readfile/home/${state.username}/${state.oldKey.join('/')}/${key}`;
   const res = await fetch(path_param);
   const data = await res.json();
   console.log(data.data);
  }
 }
});

document.querySelector('.back').addEventListener('click', (e) => {
 loadData(false);
});
