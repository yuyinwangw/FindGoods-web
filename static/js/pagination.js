const Pagination = {
  nowPage: 1,
  totalPage: 15
};

const pagination = document.getElementsByClassName("pagination__group")[0];

function init() {
  Pagination.nowPage = 1;
  if (Pagination.totalPage > 5) {
    over5PageRender();
    over5PageListener();
  } else {
    less5PageRender();
    pageListener();
  }
}
function less5PageRender() {
  let totalPage = Pagination.totalPage;
  let nowPage = Pagination.nowPage;
  let ary = [];
  let num = 1;
  while (num < totalPage + 1) {
    let classList = nowPage === num ? "active" : "";
    ary.push({ val: num, class: classList });
    num++;
  }
  listRender(ary);
}
function pageListener() {
  document.querySelectorAll(".pagination__item").forEach(el => {
    el.addEventListener("click", function() {
      if (el.dataset.val > 0) {
        Pagination.nowPage = parseInt(el.dataset.val);
        less5PageRender();
        pageListener();
      }
    });
  });
}
function over5PageListener() {
  nextBtnSet();
  preBtnSet();
  document.querySelectorAll(".pagination__item").forEach(el => {
    el.addEventListener("click", function() {
      if (el.dataset.val > 0) {
        over5PageChange(el.dataset.val);
      }
    });
  });
}
function over5PageChange(num) {
  Pagination.nowPage = parseInt(num);
  over5PageRender();
  over5PageListener();
}
function over5PageRender() {
  let nowPage = Pagination.nowPage;
  let totalPage = Pagination.totalPage;
  let pageStatus = over5PageJudgePageStatus(nowPage, totalPage);
  let ary = over5PageGenerateData(pageStatus, nowPage, totalPage);
  listRender(ary);
}
function preBtnSet() {
  document
    .getElementsByClassName("pre")[0]
    .addEventListener("click", function() {
      if (this.classList.value.indexOf("unclick") === -1) {
        over5PageChange(Pagination.nowPage - 1);
      }
    });
}
function nextBtnSet() {
  document
    .getElementsByClassName("next")[0]
    .addEventListener("click", function() {
      if (this.classList.value.indexOf("unclick") === -1) {
        over5PageChange(Pagination.nowPage + 1);
      }
    });
}

function over5PageJudgePageStatus(nowPage, totalPage) {
  return nowPage === 1
    ? "first"
    : nowPage <= totalPage / 2
    ? "front"
    : nowPage !== totalPage
    ? "back"
    : "last";
}
function over5PageGenerateData(pageStatus, nowPage, totalPage) {
  const map = {
    first: [
      { val: -2, class: "pre unclick" },
      { val: nowPage, class: "active" },
      { val: nowPage + 1, class: "" },
      { val: nowPage + 2, class: "" },
      { val: -1, class: "unclick" },
      { val: totalPage, class: "" },
      { val: -2, class: "next" }
    ],
    front: [
      { val: -2, class: "pre" },
      { val: nowPage - 1, class: "" },
      { val: nowPage, class: "active" },
      { val: nowPage + 1, class: "" },
      { val: -1, class: "unclick" },
      { val: totalPage, class: "" },
      { val: -2, class: "next" }
    ],
    back: [
      { val: -2, class: "pre" },
      { val: 1, class: "" },
      { val: -1, class: "unclick" },
      { val: nowPage - 1, class: "" },
      { val: nowPage, class: "active" },
      { val: nowPage + 1, class: "" },
      { val: -2, class: "next" }
    ],
    last: [
      { val: -2, class: "pre" },
      { val: 1, class: "" },
      { val: -1, class: "unclick" },
      { val: nowPage - 2, class: "" },
      { val: nowPage - 1, class: "" },
      { val: nowPage, class: "active" },
      { val: -2, class: "next unclick" }
    ]
  };
  return map[pageStatus];
}

function listRender(ary) {
  pagination.innerHTML = "";
  ary.forEach(element => {
    let li = document.createElement("li");
    li.setAttribute("data-val", element.val);
    li.setAttribute("class", "pagination__item " + element.class);
    li.innerText =
      element.val >= 0 ? element.val : element.val === -1 ? "..." : "";
    pagination.appendChild(li);
  });
}

init();
