let current_url = window.location.href;
const txtArea = document.getElementById("txt-data");
const paganationButtons = document.getElementById("pag");
const menu = document.getElementById('menuBox');
let  icon_m = document.getElementById("menu-toggle_b");
const apiTxtfield = document.getElementById("apikeys");
const search_input = document.getElementById("searchInput");
const loader = document.getElementById("loader");

// all API Calls
async function get_token() {
  try {
    const response = await fetch("/tokens");
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    const data = await response.json();

    return data;
  } catch (error) {
    console.error("Fetch error:", error);
    return null;
  }
}

async function refresh_token_func(data_r, url){
  console.log("401 refreshing token ")
  // const domain_name = 'http://127.0.0.1:5000/';
  try {
    // const response = await fetch(`${domain_name}auth/refresh`, {
    const response = await fetch('/auth/refresh', {
      method: "GET",
      headers: {
        'Authorization': `Bearer ${data_r.refresh_token}`,
        "Content-Type": "application/json"
      }
    });
    const r_token = await response.json();
    if (r_token.message){
      return null;
    }else{
      // data = await get_token()
      // console.log("Function get_token ", data) 
      request(url)
    }
  } catch (error) {
    console.error("Fetch error:", error);
    return null;
  }
}

async function request(url, display=false) {
  loader.classList.remove("hidden")
   // Wait for token to be set
  const data_f = await get_token();
  

  if (display){
    apiTxtfield.style.display = 'block';
    apiTxtfield.innerText = data_f.token;
  }else{
    apiTxtfield.style.display = 'none';
  }
  
  // const domain_name = 'http://127.0.0.1:5000/';

  // if (!url.includes(domain_name)) {
  //   url = `${domain_name}${url}`;
  // }
  try {
    const response = await fetch(url, {
      method: "GET",
      headers: {
        'Authorization': `Bearer ${data_f.token}`,
        "Content-Type": "application/json"
      }
    });
    if (response.status === 401){
      await refresh_token_func(data_f, url)
    }
    const data = await response.json();
    txtArea.value = JSON.stringify(data, null, 4);
    get_msg();
  

  } catch (error) {
    console.error("Fetch failed:", error);
  }

  // Toggle pagination visibility
  paganationButtons.style.display = url.includes("page") ? 'block' : 'none';

  // Toggle menu
  if (menu.style.display === "block") {
    icon_m.classList.toggle('fa-x');
    icon_m.classList.toggle('fa-bars');
    menu.style.display = "none";
  }
  search_input.value = '';
  setTimeout(()=>{
    loader.classList.add("hidden");
  }, 1000)
  

}

function about_func(){
  alert("This is a dummy Api website for dummy products...")
}

async function view_home(){
  await request("/api/product/all?page=1"); 
}

async function view_profile(){
  await request("/auth/whoami", true);

}

function search_product(){
  console.log("Search ", search_input.value);
  request(`/api/product/s=${search_input.value}`);
}

//end all api calls

// Pagnation handlers
let pageNum = 1;
const next_btn = document.getElementById("pag-btnNext");
const prev_btn = document.getElementById("pag-btnPrev");
let current_page = document.getElementById("curpage");

async function pagnation_handler_pre(){
  if (prev_btn){
    if (Number(current_page.innerText) < 7 & Number(current_page.innerText) != 1){
      pageNum--;
      current_page.innerText = pageNum
      await request(`/api/product/all?page=${current_page.innerText}`)
      next_btn.style.visibility = 'visible';
    }
    prev_btn.addEventListener("click", function(){
      if (Number(current_page.innerText) === 1 ){
            prev_btn.style.visibility ='hidden';
          }
    })

  }
}

async function pagnation_handler_next(){
  if (next_btn){
    if (Number(current_page.innerText) > 0 & Number(current_page.innerText) != 6){
      pageNum++;
      current_page.innerText = pageNum
      await request(`/api/product/all?page=${current_page.innerText}`)
      prev_btn.style.visibility = "visible"
    }
    next_btn.addEventListener("click", function(){
      if (Number(current_page.innerText) === 6){
            next_btn.style.visibility="hidden"
      }
    })
  }

}

// end pagnation handlers

function toggleMenu() {
    icon_m.classList.toggle('fa-x');
    icon_m.classList.toggle('fa-bars');
    menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
  }

  window.addEventListener('click', function (e) {
    const menu = document.getElementById('menuBox');
    const button = document.querySelector('.menu-btn');
    if (!menu.contains(e.target) && !button.contains(e.target)) {
      menu.style.display = 'none';
    }
  });

function get_msg(){
  const msg_tag = document.getElementById("viewMessage");
  fetch(`/message`)
  .then(response => response.json())
  .then(data => {
    message = data['message'];
    msg_tag.innerText = message;
  })
}


function loadSidebar(id_, pram){
  const section_tag = document.getElementById(id_);
  let added_item = [];
  fetch(`/load-data?q=${pram}`)
  .then(response => response.json())
  .then(data => {
    for (let dat of data){
      if (!added_item.includes(dat)) {
          let option_tag = document.createElement("option");
          option_tag.value = `/api/product/search_${pram}=${encodeURIComponent(dat)}`;
          option_tag.id = "option_";
          option_tag.name = "opt-text";
          option_tag.textContent = dat;
          section_tag.appendChild(option_tag);
      }
      added_item.push(dat)
    }
  })
}

window.addEventListener("DOMContentLoaded", () => {
    loadSidebar("option 1", "title")
    loadSidebar("option 2", "sku")
    loadSidebar("option 3", "category")
    to_checkValue('/api/product/price?sort=true')
    to_checkValue('/api/product/price?sort=false')
    get_msg();
    loader.classList.add("hidden")
  })

const options = document.querySelectorAll(".section");

options.forEach(option => {
  option.addEventListener('change', async function() {
    if (!current_url.includes('/auth')){
      const selected = option.value;
      if (selected) {
        await request(option.value)
      }}  
  })

})

const radio_btns = document.getElementsByName("priceOpt");

radio_btns.forEach(btn_tag => {
  btn_tag.addEventListener("click", async function(){
    if (btn_tag.checked) {
      await request(btn_tag.value)
    }
  })
})

function to_checkValue(arg){
  let op = document.getElementsByName("priceOpt");
  op.forEach(option => {
    if (current_url.includes(arg) & option.value === arg){
      option.checked = true;
    }
  });
}




