'use strict';

const state = {
 oldKey: [],
 oldData: [data],
 data,
 username,
 depth: 0,
};

const table = document.querySelector('.data-table');
const tableContent = document.querySelector('.data-table-content');

function formatBytes(bytes) {
 const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
 if (bytes === 0) return '0 Bytes';
 const i = Math.floor(Math.log(bytes) / Math.log(1024));
 return parseFloat((bytes / Math.pow(1024, i)).toFixed(2)) + ' ' + sizes[i];
}

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
  if (current[key].mtime)
   markup += `
    <div class="data-table--item ${type}" data-type="${type}">
      <p class="name">${key}</p>
      <p>${current[key].mtime}</p>
      <p>${formatBytes(current[key].size)}</p>
    </div>
  `;
 });
 tableContent.insertAdjacentHTML('beforeend', markup);
 document.querySelector('.nbFiles').innerHTML = current['_nbFiles_'];
 document.querySelector('.nbDirs').innerHTML = current['_nbDirs_'];
 document.querySelector('.totalSize').innerHTML = formatBytes(
  current['_totalSize_']
 );
};

window.addEventListener('load', loadData);

tableContent.addEventListener('click', async function (e) {
 const item = e.target.closest('div');
 if (item) {
  const firstChild = item.firstElementChild;
  const key = item.firstElementChild.innerHTML;
  if (item.dataset.type === 'dir') {
   state.depth += 1;
   state.oldData.push(state.data);
   state.oldKey.push(key);
   state.data = state.data[key]['data'];
   loadData(key);
  } else if (item.dataset.type === 'txt') {
   const res = await fetch(`/search/${key}`);
   const data = await res.json();
   let currDepth;
   if (!state.searched) console.log(data.data[state.depth][1]['content']);
   else {
    let allFiles = Array.from(document.querySelectorAll('.name'));
    let selectedSameFiles = [];
    for (let i = 0; i < allFiles.length; i++) {
     if (firstChild.innerHTML === allFiles[i].innerHTML) {
      selectedSameFiles.push(allFiles[i]);
     }
    }

    for (let i = 0; i < selectedSameFiles.length; i++) {
     if (firstChild === selectedSameFiles[i]) {
      currDepth = i;
     }
    }
    console.log(data.data[currDepth][1]['content']);
   }
  }
 }
});

document.querySelector('.back').addEventListener('click', (e) => {
 state.depth = state.depth === 0 ? 0 : state.depth - 1;
 if (state.searched) {
  state.data = data;
  state.oldData = [data];
  state.searched = false;
  document.getElementById('searchbox').value = '';
  dispatchEvent(new Event('load'));
 } else {
  document.getElementById('searchbox').value = '';
  loadData(false);
 }
});

window.addEventListener('keydown', function (event) {
 if (event.key === 'ArrowLeft') {
  document.querySelector('.back').click();
 }
});

document
 .querySelector('.btn-search')
 .addEventListener('click', async function (e) {
  e.preventDefault();
  const keyword = document.getElementById('searchbox').value;
  if (!keyword) {
   dispatchEvent(new Event('load'));
   return;
  }
  const res = await fetch(`/search/${keyword}`);
  const data = await res.json();
  if (!data) return;
  state.searched = true;
  let markup = '';
  tableContent.innerHTML = '';
  data.data.forEach((current) => {
   let type = current[1].type === 'dir' ? 'dir' : 'file';
   if (type === 'file') {
    if (current[1].type === 'txt') {
     type = 'txt';
    }
   }
   if (current[1].mtime)
    markup += `
    <div class="data-table--item ${type}" data-type="${type}">
      <p class="name">${current[0]}</p>
      <p>${current[1].mtime}</p>
      <p>${formatBytes(current[1].size)}</p>
    </div>
  `;
  });
  tableContent.insertAdjacentHTML('beforeend', markup);
  document.querySelector('.nbFiles').innerHTML = '';
  document.querySelector('.nbDirs').innerHTML = '';
  document.querySelector('.totalSize').innerHTML = '';
 });

document.getElementById('searchbox').addEventListener('input', (e) => {
 document.querySelector('.btn-search').click();
});
